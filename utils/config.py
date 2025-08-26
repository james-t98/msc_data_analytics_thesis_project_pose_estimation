import os

# Base directory for your project
BASE_DIR = "/content/drive/MyDrive/msc_data_analytics_thesis_project_pose_estimation"

# Main folders
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_DIR = os.path.join(DATA_DIR, "input")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
ENGINEERED_DIR = os.path.join(DATA_DIR, "engineered")
EDA_DIR = os.path.join(BASE_DIR, "eda")

MODELS_DIR = os.path.join(BASE_DIR, "models")
LSTM_MODELS_DIR = os.path.join(MODELS_DIR, "lstm_models")
METRICS_DIR = os.path.join(MODELS_DIR, "metrics")

RESULTS_DIR = os.path.join(BASE_DIR, "results")
VISUALIZATIONS_DIR = os.path.join(RESULTS_DIR, "visualizations")

NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")

EXERCISES = ["squat", "bench_press", "pull_ups", "lunges"] # "juggling", "penalty" - a little harder to annotate and get keypoints of view

ANGLE_CONFIG = {
    "squat": {
        "sides": ["left", "right"],
        "angles": {
            "hip_angle": {
                "joints": ["HIP", "KNEE", "ANKLE"],
                "description": "Lower body alignment of hip flexion",
                "type": "joint"
            },
            "knee_angle": {
                "joints": ["SHOULDER", "HIP", "KNEE"],
                "description": "Posture of upper leg during squat depth",
                "type": "joint"
            }
        }
    },
    "bench_press": {
        "sides": ["left", "right"],
        "angles": {
            "elbow_angle": {
                "joints": ["SHOULDER", "ELBOW", "WRIST"],
                "description": "Horizontal elbow flexion under load",
                "type": "joint"
            }
        }
    },
    "juggling": {
        "sides": ["left", "right"],
        "angles": {
            "knee_angle": {
                "joints": ["HIP", "KNEE", "ANKLE"],
                "description": "Knee lift preparation during ball juggling",
                "type": "joint"
            },
            "hip_angle": {
                "joints": ["SHOULDER", "HIP", "KNEE"],
                "description": "Hip control and balance during juggling",
                "type": "joint"
            }
        }
    },
    "penalty": {
        "sides": ["right"],  # assume right is dominant kicking leg
        "angles": {
            "hip_angle": {
                "joints": ["SHOULDER", "HIP", "KNEE"],
                "description": "Kicking leg swing and hip extension for power",
                "type": "joint"
            },
            "knee_angle": {
                "joints": ["HIP", "KNEE", "ANKLE"],
                "description": "Knee drive and follow-through control",
                "type": "joint"
            }
        }
    },
    "pull_ups": {
        "sides": ["left", "right"],
        "angles": {
            "elbow_angle": {
                "joints": ["SHOULDER", "ELBOW", "WRIST"],
                "description": "Elbow flexion during vertical pulling motion",
                "type": "joint"
            },
            "shoulder_angle": {
                "joints": ["HIP", "SHOULDER", "ELBOW"],
                "description": "Shoulder elevation and scapular involvement",
                "type": "joint"
            }
        }
    },
    "lunges": {
        "sides": ["left", "right"],
        "angles": {
            "knee_angle": {
                "joints": ["HIP", "KNEE", "ANKLE"],
                "description": "Knee control and step depth in front leg",
                "type": "joint"
            },
            "hip_angle": {
                "joints": ["SHOULDER", "HIP", "KNEE"],
                "description": "Trunk control and hip flexion during lunge",
                "type": "joint"
            }
        }
    }
}

FEATURE_CONFIG = {
    "squat": {
        "features": {
            "hip_angle": {
                "type": "rom",
                "sides": ["left", "right"],
                "description": "Hip flexion/extension depth"
            },
            "knee_angle": {
                "type": "rom",
                "sides": ["left", "right"],
                "description": "Knee bending depth"
            },
            "hip_angle_velocity": {
                "type": "velocity",
                "sides": ["left", "right"],
                "description": "Speed of hip movement"
            },
            "knee_angle_velocity": {
                "type": "velocity",
                "sides": ["left", "right"],
                "description": "Speed of knee movement"
            }
        }
    },
    "bench_press": {
        "features": {
            "elbow_angle": {
                "type": "rom",
                "sides": ["left", "right"],
                "description": "Arm flexion/extension depth"
            },
            "elbow_angle_velocity": {
                "type": "velocity",
                "sides": ["left", "right"],
                "description": "Speed of press movement"
            }
        }
    },
    "pull_ups": {
        "features": {
            "elbow_angle": {
                "type": "rom",
                "sides": ["left", "right"],
                "description": "Pull depth range"
            },
            "elbow_angle_velocity": {
                "type": "velocity",
                "sides": ["left", "right"],
                "description": "Pulling explosiveness"
            }
        }
    },
    "lunges": {
        "features": {
            "knee_angle": {
                "type": "rom",
                "sides": ["left", "right"],
                "description": "Front knee bending range"
            },
            "knee_angle_velocity": {
                "type": "velocity",
                "sides": ["left", "right"],
                "description": "Lunge tempo and control"
            }
        }
    },
    "penalty": {
        "features": {
            "hip_angle": {
                "type": "rom",
                "sides": ["right"],  # assume dominant leg for now
                "description": "Leg swing range"
            },
            "hip_angle_velocity": {
                "type": "velocity",
                "sides": ["right"],
                "description": "Kicking power indicator"
            }
        }
    },
    "juggling": {
        "features": {
            "knee_angle": {
                "type": "rom",
                "sides": ["left", "right"],
                "description": "Touch preparation range"
            },
            "knee_angle_velocity": {
                "type": "velocity",
                "sides": ["left", "right"],
                "description": "Foot tempo control"
            }
        }
    }
}

LABELS = [
    "nose", "left eye inner", "left eye", "left eye outer",
    "right eye inner", "right eye", "right eye outer", "left ear",
    "right ear", "mouth left", "mouth right", "left shoulder",
    "right shoulder", "left elbow", "right elbow", "left wrist",
    "right wrist", "left pinky", "right pinky", "left index",
    "right index", "left thumb", "right thumb", "left hip",
    "right hip", "left knee", "right knee", "left ankle",
    "right ankle", "left heel", "right heel", "left foot index",
    "right foot index"
]

COLORS = [
    "#FF6347", "#FF6347", "#FF6347", "#FF6347",
    "#FF6347", "#FF1493", "#00FF00", "#FF1493",
    "#00FF00", "#FF1493", "#00FF00", "#FFD700",
    "#00BFFF", "#FFD700", "#00BFFF", "#FFD700",
    "#00BFFF", "#800080", "#ADFF2F", "#FF4500",
    "#1E90FF", "#DA70D6", "#7FFF00", "#FF69B4",
    "#8A2BE2", "#00CED1", "#DC143C", "#FF8C00",
    "#32CD32", "#FF00FF", "#4169E1", "#FFB6C1",
    "#20B2AA"
]

POSE_LANDMARKS = {
    "NOSE": 0, "LEFT_EYE_INNER": 1, "LEFT_EYE": 2, "LEFT_EYE_OUTER": 3,
    "RIGHT_EYE_INNER": 4, "RIGHT_EYE": 5, "RIGHT_EYE_OUTER": 6, "LEFT_EAR": 7,
    "RIGHT_EAR": 8, "MOUTH_LEFT": 9, "MOUTH_RIGHT": 10, "LEFT_SHOULDER": 11,
    "RIGHT_SHOULDER": 12, "LEFT_ELBOW": 13, "RIGHT_ELBOW": 14, "LEFT_WRIST": 15,
    "RIGHT_WRIST": 16, "LEFT_PINKY": 17, "RIGHT_PINKY": 18, "LEFT_INDEX": 19,
    "RIGHT_INDEX": 20, "LEFT_THUMB": 21, "RIGHT_THUMB": 22, "LEFT_HIP": 23,
    "RIGHT_HIP": 24, "LEFT_KNEE": 25, "RIGHT_KNEE": 26, "LEFT_ANKLE": 27,
    "RIGHT_ANKLE": 28, "LEFT_HEEL": 29, "RIGHT_HEEL": 30, "LEFT_FOOT_INDEX": 31,
    "RIGHT_FOOT_INDEX": 32
}

def ensure_directories():
    for path in [INPUT_DIR, PROCESSED_DIR, ENGINEERED_DIR, 
                 LSTM_MODELS_DIR, METRICS_DIR, VISUALIZATIONS_DIR]:
        os.makedirs(path, exist_ok=True)