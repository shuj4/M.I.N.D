import tkinter as tk
import pyautogui
import threading
import time

MOVE_AMOUNT = 50
canvas_size = 400
center = canvas_size // 2

# Global references
root = None
canvas = None
arrows = {}

def start_cursor_gui():
    global root, canvas, arrows

    print("🟢 Starting Cursor GUI...")  # DEBUG LOG

    root = tk.Tk()
    root.title("Kabhi Up Kabhi Down")

    canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="gray20", highlightthickness=0)
    canvas.pack()

    arrows['UP'] = canvas.create_polygon(
        center, center - 120,
        center - 40, center - 40,
        center + 40, center - 40,
        fill="black", outline=""
    )

    arrows['DOWN'] = canvas.create_polygon(
        center, center + 120,
        center - 40, center + 40,
        center + 40, center + 40,
        fill="black", outline=""
    )

    arrows['LEFT'] = canvas.create_polygon(
        center - 120, center,
        center - 40, center - 40,
        center - 40, center + 40,
        fill="black", outline=""
    )

    arrows['RIGHT'] = canvas.create_polygon(
        center + 120, center,
        center + 40, center - 40,
        center + 40, center + 40,
        fill="black", outline=""
    )

    canvas.create_oval(center - 25, center - 25, center + 25, center + 25, fill="lightgray", outline="")
    canvas.create_oval(center - 10, center - 10, center + 10, center + 10, fill="black", outline="")

    canvas.tag_bind(arrows['UP'], "<Button-1>", lambda e: move_cursor('UP'))
    canvas.tag_bind(arrows['DOWN'], "<Button-1>", lambda e: move_cursor('DOWN'))
    canvas.tag_bind(arrows['LEFT'], "<Button-1>", lambda e: move_cursor('LEFT'))
    canvas.tag_bind(arrows['RIGHT'], "<Button-1>", lambda e: move_cursor('RIGHT'))

    root.mainloop()

def flash_arrow(direction):
    if direction in arrows:
        arrow = arrows[direction]
        canvas.itemconfig(arrow, fill="white")
        canvas.update()
        time.sleep(0.15)
        canvas.itemconfig(arrow, fill="black")
        canvas.update()

def move_cursor(direction):
    print(f"🧠 Triggered move_cursor('{direction}')")  # DEBUG LOG
    x, y = pyautogui.position()
    if direction == 'UP':
        pyautogui.moveTo(x, y - MOVE_AMOUNT)
    elif direction == 'DOWN':
        pyautogui.moveTo(x, y + MOVE_AMOUNT)
    elif direction == 'LEFT':
        pyautogui.moveTo(x - MOVE_AMOUNT, y)
    elif direction == 'RIGHT':
        pyautogui.moveTo(x + MOVE_AMOUNT, y)

    if canvas:
        threading.Thread(target=flash_arrow, args=(direction,), daemon=True).start()
