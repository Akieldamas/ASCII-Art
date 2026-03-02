import cv2
import time
import os
import numpy as np
from playsound3 import playsound
import threading
import sys

more_keys = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]

def frame_to_ascii(pixels):
    if pixels.shape[2] > 3:
        pixels = pixels[:, :, :3]

    brightness_values = [
        (int(r) + int(g) + int(b)) // 3
        for row in pixels
        for r, g, b in row
    ]
    min_pixel = min(brightness_values)
    max_pixel = max(brightness_values)

    ascii_image = ""
    for row in pixels:
        ascii_row = ""
        for pixel in row:
            r, g, b = map(int, pixel)
            brightness = (r + g + b) // 3

            brightness = int((brightness - min_pixel) / (max_pixel - min_pixel) * 255)

            char_index = int(brightness / 255 * (len(more_keys) - 1))
            char = more_keys[char_index]

            ascii_row += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        ascii_image += ascii_row + "\n"
    return ascii_image

def play_audio(file):
    playsound(file)

def main(video_file, audio_file, width=35, height=35, use_color=True):
    vid = cv2.VideoCapture(video_file)
    fps = vid.get(cv2.CAP_PROP_FPS) or 24

    threading.Thread(target=play_audio, args=(audio_file,), daemon=True).start()

    os.system("cls" if os.name == "nt" else "clear")
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        while True:
            ret, frame = vid.read()
            if not ret:
                break

            frame = cv2.resize(frame, (width, height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            ascii_frame = frame_to_ascii(frame)
            sys.stdout.write("\033[H" + ascii_frame)
            sys.stdout.flush()

            time.sleep(0.6 / fps)
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        vid.release()

if __name__ == "__main__":
    main("assets/fish.mp4", "assets/fish.mp4", width=30, height=30, use_color=True)