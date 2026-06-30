import keyboard
import threading
import time
import os
import pyautogui
import requests

import tkinter as tk
import sounddevice as sd
import soundfile as sf
import numpy as np

from transcribe_audio import transcribe
from groq_api import ask_groq_prompt

from tkinter import messagebox

# Config
ASK_GROQ = False

if ASK_GROQ:
    try:
        requests.head("https://www.google.com", timeout=3)
    except (requests.ConnectionError, requests.Timeout):
        ASK_GROQ = False

# Window
root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "magenta")
WIDTH, HEIGHT = 110, 40
root.geometry(f"{WIDTH}x{HEIGHT}+300+300")

# Audio recording globals
MUTED = True
recording_thread = None
recording_data = []
stream = None

# Canvas
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="magenta", highlightthickness=0)

canvas.pack()
def draw_rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r,
        x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

rect_id = draw_rounded_rect(canvas, 3, 3, WIDTH-3, HEIGHT-3, r=25, fill="black", outline="#007BFF", width=3)
canvas.create_text(WIDTH // 2 + 20, HEIGHT // 2, text="🎙️", font=("Segoe UI", 18), fill="white")
slash = canvas.create_line(WIDTH // 2 - 14, HEIGHT // 2 + 10, WIDTH // 2 + 14, HEIGHT // 2 - 10, fill="red", width=3)

# Audio recording functions
def start_recording():
    global recording_data, stream
    recording_data = []
    def callback(indata, frames, time, status):
        recording_data.append(indata.copy())
    stream = sd.InputStream(samplerate=44100, channels=1, callback=callback)
    stream.start()

def stop_recording():
    global stream
    if stream:
        stream.stop()
        stream.close()
        stream = None
    if recording_data:
        data = np.concatenate(recording_data, axis=0)
        os.makedirs("audio", exist_ok=True)
        t = int(time.time())
        sf.write(f"audio/{t}.wav", data, 44100)
        text = transcribe(f"audio/{t}.wav")
        if ASK_GROQ:
            text = ask_groq_prompt(text)
        # print(text)
        pyautogui.write(text)

# Microphone pulsing
PULSE = None

def start_pulse():
    global PULSE
    brightness = ["#00FF66", "#00CC44", "#009933", "#00CC44"]
    def tick(i=0):
        global PULSE
        canvas.itemconfig(rect_id, outline=brightness[i % len(brightness)])
        PULSE = root.after(200, tick, i + 1)
    tick()

def stop_pulse():
    global PULSE
    if PULSE:
        root.after_cancel(PULSE)
        PULSE = None
    canvas.itemconfig(rect_id, outline="#007BFF")

# Window dragging logic
def start_drag(e):
    root.x, root.y = e.x, e.y

def drag_window(e):
    x = root.winfo_x() + (e.x - root.x)
    y = root.winfo_y() + (e.y - root.y)
    root.geometry(f"+{x}+{y}")

def toggle_mute(e=None):
    global MUTED
    MUTED = not MUTED
    canvas.itemconfig(slash, state="normal" if MUTED else "hidden")
    if MUTED:
        stop_pulse()
        threading.Thread(target=stop_recording).start()
    else:
        start_pulse()
        threading.Thread(target=start_recording).start()

keyboard.add_hotkey("ctrl+shift+alt+m", lambda: root.after(0, toggle_mute))

root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", drag_window)
root.bind("<Button-3>", lambda e: root.destroy())  # Right-click to exit

# Quick test
_ = transcribe("test_audio.mp3")

# Give User the Controls
msg_box_text = """Left-click and drag: move the widget around

Right-click: close the widget

Ctrl + Shift + Alt + M: start or stop the microphone"""
messagebox.showinfo("Controls", msg_box_text)

root.mainloop()
