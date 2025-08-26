"""
Handles pose landmark processing, joint angle extraction, and symmetry handling.
"""
import pandas as pd
import numpy as np
import os, json, cv2
from utils.config import ANGLE_CONFIG
from scipy.signal import find_peaks

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine_val = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.arccos(np.clip(cosine_val, -1.0, 1.0))
    return np.degrees(angle)


def export_angle_data(video_name, angles, timestamps, export_path, exercise_type="squat"):
    os.makedirs(export_path, exist_ok=True)

    config = ANGLE_CONFIG[exercise_type]
    sides = config.get("sides", ["left"])
    angle_defs = config["angles"]
    col_names = []
    for side in sides:
        for angle_name in angle_defs:
            col_names.append(f"{angle_name}_{side}")

    df = pd.DataFrame(angles, columns=col_names)
    df.insert(0, "timestamp", timestamps)

    file_path = os.path.join(export_path, f"{video_name}_angles.csv")
    df.to_csv(file_path, index=False)
    print(f"[📁] Exported angle data to: {file_path}")

def summarize_and_enrich_metadata(
    angles_csv_path,
    metadata_path,
    screenshot_path=None,
    threshold=15,
    min_distance=10,
    frame_rate=30
):
    """
    Enrich metadata.json with rep summary, screenshot reference, and motion features.
    """

    df = pd.read_csv(angles_csv_path)
    metadata = json.load(open(metadata_path))

    # Get main angle for rep counting (heuristic: first angle col)
    angle_col = next((col for col in df.columns if '_angle' in col), None)
    if angle_col is None:
        print("❌ No angle column found for rep estimation.")
        return

    signal = df[angle_col].values
    timestamps = df["timestamp"].values if "timestamp" in df.columns else np.arange(len(signal)) / frame_rate

    peaks, _ = find_peaks(signal, prominence=threshold, distance=min_distance)
    troughs, _ = find_peaks(-signal, prominence=threshold, distance=min_distance)
    extrema = np.sort(np.concatenate([peaks, troughs]))

    rep_durations = []
    rep_roms = []
    velocities = []

    for i in range(1, len(extrema)):
        t0, t1 = extrema[i - 1], extrema[i]
        duration = timestamps[t1] - timestamps[t0]
        rom = np.abs(signal[t1] - signal[t0])
        vel = rom / duration if duration > 0 else 0
        rep_durations.append(duration)
        rep_roms.append(rom)
        velocities.append(vel)

    metadata["rep_count"] = len(rep_durations)
    metadata["avg_rep_duration"] = float(np.mean(rep_durations)) if rep_durations else 0
    metadata["avg_rom"] = float(np.mean(rep_roms)) if rep_roms else 0
    metadata["avg_velocity"] = float(np.mean(velocities)) if velocities else 0

    if screenshot_path:
        metadata["annotated_frame"] = str(screenshot_path)

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Enriched metadata: {metadata_path}")

def get_angle_index(angle_name, side, angle_defs, sides):
    """
    Get the index of an angle in the full angle vector.
    Useful for selecting a specific angle time series.

    Returns:
        int: Index of the angle in the full array.
    """
    col_names = [f"{angle}_{s}" for s in sides for angle in angle_defs]
    try:
        return col_names.index(f"{angle_name}_{side}")
    except ValueError:
        return -1
    
def overlay_joint_angles(frame, joints: dict, angles: dict, exercise_type: str, color=(0, 255, 255)):
    """
    Generic overlay for any exercise using joint and angle mappings.

    Args:
        frame (np.ndarray): Image/frame.
        joints (dict): Dictionary of joint coordinates.
        angles (dict): Dictionary of computed angles.
        exercise_type (str): The exercise type (used for label).
        color (tuple): BGR color.
    """
    try:
        font = cv2.FONT_HERSHEY_SIMPLEX

        for joint_name, coord in joints.items():
            joint_key = joint_name.lower()
            if joint_key in angles:
                angle_val = angles[joint_key]
                cv2.putText(
                    frame,
                    f"{joint_key.replace('_', ' ').title()}: {angle_val:.1f}°",
                    tuple(np.array(coord).astype(int)),
                    font,
                    0.5,
                    color,
                    1
                )

        # Draw lines between joints if triplets are available
        triplets = []
        if exercise_type in ANGLE_CONFIG:
            for angle_name, triplet in ANGLE_CONFIG[exercise_type]["angles"].items():
                for side in ANGLE_CONFIG[exercise_type].get("sides", ["left"]):
                    joint_triplet = [f"{j}_{side.upper()}" for j in triplet]
                    if all(j in joints for j in joint_triplet):
                        a, b, c = joints[joint_triplet[0]], joints[joint_triplet[1]], joints[joint_triplet[2]]
                        cv2.line(frame, tuple(np.array(a).astype(int)), tuple(np.array(b).astype(int)), color, 1)
                        cv2.line(frame, tuple(np.array(b).astype(int)), tuple(np.array(c).astype(int)), color, 1)

    except Exception as e:
        print(f"[⚠️] Overlay failed: {e}")


def extract_rep_features(angle_series, timestamps, prominence=15, distance=10, fps=30):
    """
    Extracts rep-level features from a joint angle time-series.

    Args:
        angle_series (np.ndarray): Array of joint angles over time.
        timestamps (np.ndarray): Timestamps per frame.
        prominence (float): Minimum prominence of peaks to detect.
        distance (int): Minimum distance (in frames) between reps.
        fps (float): Frame rate, used for duration calculation.

    Returns:
        Dict[str, float or int]: rep_count, avg_rep_duration, avg_rom, avg_velocity
    """
    if len(angle_series) < 10:
        return {
            "rep_count": 0,
            "avg_rep_duration": 0,
            "avg_rom": 0,
            "avg_velocity": 0
        }

    # --- 1. Detect minima and maxima as reps ---
    peaks, _ = find_peaks(-angle_series, prominence=prominence, distance=distance)
    troughs, _ = find_peaks(angle_series, prominence=prominence, distance=distance)
    extrema = np.sort(np.concatenate([peaks, troughs]))

    if len(extrema) < 2:
        return {
            "rep_count": 0,
            "avg_rep_duration": 0,
            "avg_rom": 0,
            "avg_velocity": 0
        }

    # --- 2. Calculate per-rep durations and ROMs ---
    rep_durations = []
    rep_roms = []
    rep_velocities = []

    for i in range(1, len(extrema)):
        start_idx = extrema[i - 1]
        end_idx = extrema[i]

        duration = timestamps[end_idx] - timestamps[start_idx]
        rom = np.abs(angle_series[end_idx] - angle_series[start_idx])

        # Avoid division by zero
        if duration > 0:
            velocity = rom / duration
        else:
            velocity = 0

        rep_durations.append(duration)
        rep_roms.append(rom)
        rep_velocities.append(velocity)

    return {
        "rep_count": len(rep_durations),
        "avg_rep_duration": float(np.mean(rep_durations)),
        "avg_rom": float(np.mean(rep_roms)),
        "avg_velocity": float(np.mean(rep_velocities))
    }
