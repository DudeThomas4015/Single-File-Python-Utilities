import pyautogui
from PIL import ImageGrab
import tkinter as tk
from tkinter import messagebox
from pynput import mouse
import pyperclip  # for clipboard access

# Storage for saved colors
saved_colors = []
current_index = -1
frozen = False

def get_pixel_color(x, y):
    img = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    return img.getpixel((0, 0))

def update_color():
    global frozen
    if not frozen:
        x, y = pyautogui.position()
        color = get_pixel_color(x, y)
        hex_color = "#%02x%02x%02x" % color

        # Update live preview
        color_box.config(bg=hex_color)
        rgb_label.config(text=f"RGB: {color}")
        hex_label.config(text=f"HEX: {hex_color.upper()}")
        pos_label.config(text=f"Position: ({x}, {y})")

    root.after(50, update_color)

def freeze_color(x, y, button, pressed):
    """Toggle freeze/save on middle click."""
    global frozen, current_index
    if pressed and button == mouse.Button.middle:
        if frozen:
            # Unfreeze
            frozen = False
        else:
            # Freeze and save
            pos = (x, y)
            color = get_pixel_color(*pos)
            hex_color = "#%02x%02x%02x" % color

            saved_colors.append((color, hex_color.upper(), pos))
            current_index = len(saved_colors) - 1
            frozen = True
            display_saved()

def display_saved():
    """Display the saved color at current_index."""
    global current_index
    if 0 <= current_index < len(saved_colors):
        color, hex_color, pos = saved_colors[current_index]
        color_box.config(bg=hex_color)
        rgb_label.config(text=f"RGB: {color}")
        hex_label.config(text=f"HEX: {hex_color}")
        pos_label.config(text=f"Position: {pos}")

def show_prev():
    global current_index
    if current_index > 0:
        current_index -= 1
        display_saved()

def show_next():
    global current_index
    if current_index < len(saved_colors) - 1:
        current_index += 1
        display_saved()

def copy_code():
    """Copy current color/position in desired format to clipboard."""
    if 0 <= current_index < len(saved_colors):
        color, _, pos = saved_colors[current_index]
        code_str = f'"x": {pos[0]}, "y": {pos[1]}, "color": {color}, "tol": 20'
        pyperclip.copy(code_str)
        messagebox.showinfo("Copied", f"Copied to clipboard:\n{code_str}")

# Setup tkinter GUI
root = tk.Tk()
root.title("Color Picker with History")
root.geometry("300x250")
root.resizable(False, False)

color_box = tk.Label(root, width=20, height=4, bg="black")
color_box.pack(pady=5)

rgb_label = tk.Label(root, text="RGB: (0,0,0)")
rgb_label.pack()

hex_label = tk.Label(root, text="HEX: #000000")
hex_label.pack()

pos_label = tk.Label(root, text="Position: (0,0)")
pos_label.pack()

# Navigation buttons
frame = tk.Frame(root)
frame.pack(pady=5)

prev_button = tk.Button(frame, text="◀ Back", command=show_prev)
prev_button.pack(side="left", padx=5)

next_button = tk.Button(frame, text="Forward ▶", command=show_next)
next_button.pack(side="left", padx=5)

copy_button = tk.Button(root, text="Copy Code", command=copy_code)
copy_button.pack(pady=5)

# Start global mouse listener
listener = mouse.Listener(on_click=freeze_color)
listener.start()

# Start updating
update_color()
root.mainloop()
