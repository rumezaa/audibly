# HEADS UP! This might only work on Mac OS.

import cv2
import pyvirtualcam
from pyvirtualcam import PixelFormat

# Open real webcam
cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit(1)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30

# Caption settings
caption_list = [
    "This is some sample text!!!",
    "Caption 2",
    "Another caption",
    "Keep cycling through these",
    "Last caption in the list"
]
caption_position = (50, height - 50)  # Bottom left with padding
font = cv2.FONT_HERSHEY_DUPLEX
font_scale = 1.0
font_color = (255, 255, 255)  # White text
font_thickness = 2
outline_color = (0, 0, 0)  # Black outline
outline_thickness = 4

# Caption cycling settings
frames_per_caption = fps * 3  # Change caption every 3 seconds
frame_count = 0
current_caption_index = 0

def add_caption(frame, text, position, font, scale, color, thickness, outline_color, outline_thickness):
    """Add text caption with outline to frame"""
    x, y = position
    # Draw outline (thicker, darker)
    cv2.putText(frame, text, position, font, scale, outline_color, outline_thickness, cv2.LINE_AA)
    # Draw main text (thinner, brighter)
    cv2.putText(frame, text, position, font, scale, color, thickness, cv2.LINE_AA)
    return frame

with pyvirtualcam.Camera(
    width=width,
    height=height,
    fps=fps,
    fmt=PixelFormat.BGR
) as cam:
    print(f'Virtual camera started: {cam.device}')

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from webcam")
            break

        # Cycle through captions based on frame count
        if frame_count % frames_per_caption == 0:
            current_caption_index = (current_caption_index + 1) % len(caption_list)
        
        # Get current caption text
        current_caption_text = caption_list[current_caption_index]
        
        # Flip, add text, then flip back
        frame = cv2.flip(frame, 1)
        frame = add_caption(frame, current_caption_text, caption_position, font, font_scale, font_color, font_thickness, outline_color, outline_thickness)
        frame = cv2.flip(frame, 1)  # Flip back

        cam.send(frame)
        cam.sleep_until_next_frame()
        frame_count += 1

cap.release()