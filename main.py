import tkinter as tk

# Window
root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "magenta")
WIDTH, HEIGHT = 110, 40
root.geometry(f"{WIDTH}x{HEIGHT}+300+300")
MUTED = True

# Canvas
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="magenta", highlightthickness=0)

canvas.pack()
def draw_rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r,
        x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

draw_rounded_rect(canvas, 3, 3, WIDTH-3, HEIGHT-3, r=25, fill="black", outline="#007BFF", width=3)
canvas.create_text(WIDTH // 2 + 18, HEIGHT // 2, text="🎙️", font=("Segoe UI", 18), fill="white")
slash = canvas.create_line(WIDTH // 2 - 14, HEIGHT // 2 + 10, WIDTH // 2 + 14, HEIGHT // 2 - 10, fill="red", width=3)

# Window dragging logic
def start_drag(e):
    root.x, root.y = e.x, e.y

def drag_window(e):
    x = root.winfo_x() + (e.x - root.x)
    y = root.winfo_y() + (e.y - root.y)
    root.geometry(f"+{x}+{y}")

def toggle_mute(e):
    global MUTED
    MUTED = not MUTED
    canvas.itemconfig(slash, state="hidden" if MUTED else "normal")

root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", drag_window)
root.bind("<Button-2>", toggle_mute)
root.bind("<Button-3>", lambda e: root.destroy())  # Right-click to exit

root.mainloop()
