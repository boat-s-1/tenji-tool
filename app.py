import cv2
import numpy as np

BOAT_COLORS = [
    (255,255,255),
    (80,80,80),
    (0,0,255),
    (255,0,0),
    (0,255,255),
    (0,255,0)
]

def create_trajectory_image(video_path, start_times, duration_sec, threshold=25):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    scale = 0.4
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)
    total_frames = int(duration_sec * fps)

    # 軌跡キャンバス
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    caps = []
    prev_frames = []
    positions = [[] for _ in range(6)]

    for t in start_times:
        c = cv2.VideoCapture(video_path)
        if t > 0:
            c.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
        caps.append(c)

        ret, frame = c.read()
        if ret:
            prev_frames.append(cv2.resize(frame, (width, height)))
        else:
            prev_frames.append(None)

    for _ in range(total_frames):
        for i, c in enumerate(caps):
            ret, frame = c.read()
            if not ret or prev_frames[i] is None:
                continue

            frame = cv2.resize(frame, (width, height))

            diff = cv2.absdiff(prev_frames[i], frame)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

            _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

            # 重心取得
            ys, xs = np.where(mask > 0)
            if len(xs) > 50:
                cx = int(np.mean(xs))
                cy = int(np.mean(ys))
                positions[i].append((cx, cy))

            prev_frames[i] = frame

    # 線を描画
    for i in range(6):
        for j in range(1, len(positions[i])):
            cv2.line(canvas, positions[i][j-1], positions[i][j], BOAT_COLORS[i], 2)

    return canvas
