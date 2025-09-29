import pyautogui
import time

# --- Settings ---
TARGET_X, TARGET_Y = 217, 138           # Pixel coordinates to monitor
TARGET_COLOR = (78, 100, 118)              # RGB color to detect
TOLERANCE = 15                          # Allowable color variation (0 = exact match)
CHECK_INTERVAL = 0.1                    # Seconds between checks (0.1 = 100ms)

# --- Functions ---
def colors_match(c1, c2, tolerance):
    """Return True if two colors are within tolerance."""
    return all(abs(a - b) <= tolerance for a, b in zip(c1, c2))

def check_pixel(x, y, expected_color, tolerance):
    """Check if the pixel at (x, y) matches the target color."""
    screenshot = pyautogui.screenshot(region=(x, y, 1, 1))  
    pixel_color = screenshot.getpixel((0, 0))
    return colors_match(pixel_color, expected_color, tolerance), pixel_color

def on_match():
    print("✅ Pixel matched! Triggering event...")
    # Example action (press spacebar):
    # pyautogui.press("space")

# --- Watchdog Loop ---
print("🔍 Starting watchdog... Press Ctrl+C to stop.")
try:
    while True:
        matched, current_color = check_pixel(TARGET_X, TARGET_Y, TARGET_COLOR, TOLERANCE)
        if matched:
            on_match()
            # Remove `break` if you want it to keep firing each time it sees the match
            # break  
        # Debug: show what the pixel actually is
        # print("Pixel:", current_color)  
        time.sleep(CHECK_INTERVAL)
except KeyboardInterrupt:
    print("🛑 Watchdog stopped.")
