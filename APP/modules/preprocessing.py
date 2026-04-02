import cv2
import numpy as np

IMG_SIZE = 224

def preprocess_clip(frames_bgr: list) -> np.ndarray:
    clip = []
    for frame in frames_bgr:
        resized = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        clip.append(rgb.astype(np.float32) / 255.0)

    return np.expand_dims(np.array(clip, dtype=np.float32), axis=0)