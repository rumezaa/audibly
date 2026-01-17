import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
import threading

# Color palette matching the website
COLORS = {
    'primary': '#2A3644',      # Dark blue from website
    'secondary': '#40B8AD',    # Teal/blue from website
    'white': '#FFFFFF',
    'gray': '#555555',
    'pink': '#F0E5EB',         # Soft pink/lavender from website
    'bg': '#FFFFFF',
    'bg_alt': '#F8FAFC',       # Light gray background
    'success': '#22c55e',      # Green for success states
    'warning': '#f59e0b',      # Orange for warnings
}

# Global variables for process management
speech_process = None
is_running = False

def run_sign_language():
    print("Running sign language")

def update_status(message, color=None):
    """Update the status label with a message"""
    status_label.config(text=message)
    if color:
        status_label.config(fg=color)
    root.update_idletasks()

def run_speech_to_text():
    """Run the speech to text script and update GUI status"""
    global speech_process, is_running
    
    if is_running:
        return
    
    # Update GUI to show it's starting
    update_status("Starting speech-to-text...", COLORS['warning'])
    btn_speech.config(state='disabled')
    btn_sign.config(state='disabled')
    
    # Get the script path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, 'speech_to_text.py')
    
    def run_script():
        global speech_process, is_running
        try:
            is_running = True
            update_status("Speech-to-text is running...", COLORS['success'])
            
            # Run the script (runs continuously, so don't wait for completion)
            speech_process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give it a moment to start, then check if process is running
            import time
            time.sleep(0.5)  # Brief delay to let process start
            
            if speech_process.poll() is None:
                # Process is running
                update_status("✓ Speech-to-text is active - captions are live!", COLORS['success'])
            else:
                # Process failed to start or exited immediately
                update_status("Error: Failed to start speech-to-text", '#ef4444')
                is_running = False
                speech_process = None
                btn_speech.config(state='normal')
                btn_sign.config(state='normal')
            
            # Monitor process in background
            def monitor_process():
                global speech_process, is_running
                if speech_process:
                    speech_process.wait()  # Wait for process to end
                    # Process ended
                    is_running = False
                    speech_process = None
                    update_status("Speech-to-text stopped", COLORS['gray'])
                    btn_speech.config(state='normal')
                    btn_sign.config(state='normal')
            
            monitor_thread = threading.Thread(target=monitor_process, daemon=True)
            monitor_thread.start()
            
        except Exception as e:
            update_status(f"Error starting speech-to-text: {str(e)}", '#ef4444')
            is_running = False
            speech_process = None
            btn_speech.config(state='normal')
            btn_sign.config(state='normal')
    
    # Run in a separate thread to avoid blocking GUI
    thread = threading.Thread(target=run_script, daemon=True)
    thread.start()

# Create window
root = tk.Tk()
root.title("Audibly")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg=COLORS['bg'])

# Configure style
style = ttk.Style()
style.theme_use('clam')

# Configure button styles
style.configure('Primary.TButton',
    background=COLORS['primary'],
    foreground=COLORS['white'],
    borderwidth=0,
    focuscolor='none',
    font=('Inter', 12, 'bold'),
    padding=(20, 12))

style.map('Primary.TButton',
    background=[('active', COLORS['primary']), ('pressed', '#1e293b')])

style.configure('Outline.TButton',
    background=COLORS['white'],
    foreground=COLORS['primary'],
    borderwidth=2,
    relief='solid',
    focuscolor='none',
    font=('Inter', 12, 'bold'),
    padding=(20, 12))

style.map('Outline.TButton',
    background=[('active', COLORS['bg_alt']), ('pressed', COLORS['bg_alt'])])

# Main container with padding
main_frame = tk.Frame(root, bg=COLORS['bg'], padx=40, pady=40)
main_frame.pack(fill='both', expand=True)

# Badge/Label (matching website style)
badge = tk.Label(
    main_frame,
    text="Eliminating Access Bias in the Workplace",
    font=('Inter', 10, 'bold'),
    bg=COLORS['pink'],
    fg=COLORS['primary'],
    padx=12,
    pady=6,
    relief='flat',
    borderwidth=0
)
badge.pack(pady=(0, 20))

# Title
title_frame = tk.Frame(main_frame, bg=COLORS['bg'])
title_frame.pack(pady=(0, 10))

title_part1 = tk.Label(
    title_frame,
    text="Choose Input",
    font=('Inter', 28, 'bold'),
    bg=COLORS['bg'],
    fg=COLORS['primary']
)
title_part1.pack(side='left')

title_part2 = tk.Label(
    title_frame,
    text=" Mode",
    font=('Inter', 28, 'bold'),
    bg=COLORS['bg'],
    fg=COLORS['secondary']
)
title_part2.pack(side='left')

# Description text
description = tk.Label(
    main_frame,
    text="Select how you'd like to participate in meetings",
    font=('Inter', 12),
    bg=COLORS['bg'],
    fg=COLORS['gray'],
    wraplength=400,
    justify='center'
)
description.pack(pady=(0, 30))

# Button container
button_frame = tk.Frame(main_frame, bg=COLORS['bg'])
button_frame.pack(pady=10)

# Primary button (Sign Language)
btn_sign = ttk.Button(
    button_frame,
    text="Sign Language → Text",
    style='Primary.TButton',
    command=run_sign_language,
    width=28
)
btn_sign.pack(pady=8, fill='x')

# Outline button (Speech to Text)
btn_speech = ttk.Button(
    button_frame,
    text="Speech → Text",
    style='Outline.TButton',
    command=run_speech_to_text,
    width=28
)
btn_speech.pack(pady=8, fill='x')

# Status label
status_label = tk.Label(
    main_frame,
    text="Ready",
    font=('Inter', 11),
    bg=COLORS['bg'],
    fg=COLORS['gray'],
    pady=15
)
status_label.pack(pady=(15, 0))

# Center the window on screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

# Handle window close - cleanup process if running
def on_closing():
    global speech_process, is_running
    if speech_process and is_running:
        try:
            speech_process.terminate()
            speech_process.wait(timeout=2)
        except:
            speech_process.kill()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()