import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
import threading

# Color palette matching the website
COLORS = {
    'primary': '#2d5786',      # Dark blue from website
    'secondary': '#39bcf9',    # Teal/blue from website
    'white': '#FFFFFF',
    'gray': '#555555',
    'pink': '#F0E5EB',         # Soft pink/lavender from website
    'bg': '#FFFFFF',
    'bg_alt': '#F8FAFC',       # Light gray background
    'success': '#22c55e',      # Green for success states
    'warning': '#f59e0b',      # Orange for warnings
}

# Available languages for speech-to-text (must match speech_to_text.py)
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'ru': 'Russian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'pt': 'Portuguese',
    'it': 'Italian',
    'hi': 'Hindi'
}

# Global variables for process management
speech_process = None
asl_process = None
is_running = False
is_asl_running = False
manual_stop = False  # Track if process was stopped manually
manual_asl_stop = False  # Track if ASL process was stopped manually
selected_language = 'en'  # Default language

def update_status(message, color=None):
    """Update the status label with a message"""
    status_label.config(text=message)
    if color:
        status_label.config(fg=color)
    root.update_idletasks()

def update_button_state():
    """Update button text and command based on running state"""
    global is_running, is_asl_running
    if is_running:
        btn_speech.config(text="Stop Speech-to-Text", command=stop_speech_to_text, state='normal')
    else:
        btn_speech.config(text="Speech-to-Text", command=run_speech_to_text, state='normal')

    if is_asl_running:
        btn_sign.config(text="Stop Sign Language-to-Text", command=stop_sign_language, state='normal')
    else:
        btn_sign.config(text="Sign Language-to-Text", command=run_sign_language, state='normal')

def stop_speech_to_text():
    """Stop the running speech to text process"""
    global speech_process, is_running, manual_stop

    if not speech_process or not is_running:
        return

    # Set manual stop flag to prevent monitor_process from updating UI
    manual_stop = True

    # Update GUI to show it's stopping
    update_status("Stopping speech-to-text...", COLORS['warning'])
    btn_speech.config(state='disabled')

    try:
        # Terminate the process gracefully
        speech_process.terminate()
        speech_process.wait(timeout=2)
    except Exception:
        # Force kill if terminate didn't work or process already ended
        try:
            speech_process.kill()
            speech_process.wait()
        except:
            pass  # Process may have already ended
    finally:
        # Reset state
        is_running = False
        speech_process = None
        manual_stop = False

        # Update UI
        update_status("Speech-to-text stopped", COLORS['gray'])
        btn_speech.config(state='normal')
        btn_sign.config(state='normal')
        update_button_state()

def stop_sign_language():
    """Stop the running ASL to text process"""
    global asl_process, is_asl_running, manual_asl_stop

    if not asl_process or not is_asl_running:
        return

    # Set manual stop flag to prevent monitor_process from updating UI
    manual_asl_stop = True

    # Update GUI to show it's stopping
    update_status("Stopping ASL translation...", COLORS['warning'])
    btn_sign.config(state='disabled')

    try:
        # Terminate the process gracefully
        asl_process.terminate()
        asl_process.wait(timeout=2)
    except Exception:
        # Force kill if terminate didn't work or process already ended
        try:
            asl_process.kill()
            asl_process.wait()
        except:
            pass  # Process may have already ended
    finally:
        # Reset state
        is_asl_running = False
        asl_process = None
        manual_asl_stop = False

        # Update UI
        update_status("ASL translation stopped", COLORS['gray'])
        btn_sign.config(state='normal')
        btn_speech.config(state='normal')
        update_button_state()

def run_sign_language():
    """Run the ASL to text script and update GUI status"""
    global asl_process, is_asl_running, manual_asl_stop, is_running

    if is_asl_running:
        return

    # Don't allow both to run at the same time
    if is_running:
        update_status("Please stop speech-to-text first", COLORS['warning'])
        return

    # Reset manual stop flag
    manual_asl_stop = False

    # Update GUI to show it's starting
    update_status("Starting ASL translation...", COLORS['warning'])
    btn_sign.config(state='disabled')
    btn_speech.config(state='disabled')

    # Get the script path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, 'asl.py')
    
    # Verify script exists
    if not os.path.exists(script_path):
        update_status(f"Error: asl.py not found at {script_path}", '#ef4444')
        btn_sign.config(state='normal')
        btn_speech.config(state='normal')
        return

    def run_script():
        global asl_process, is_asl_running
        try:
            is_asl_running = True
            update_status("ASL translation is starting...", COLORS['success'])

            # Run the script (runs continuously, so don't wait for completion)
            # Set cwd to script_dir so relative paths in asl.py work correctly
            asl_process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=script_dir
            )

            # Give it a moment to start, then check if process is running
            import time
            time.sleep(0.5)  # Brief delay to let process start

            if asl_process.poll() is None:
                # Process is running
                update_status("✓ ASL translation is active - virtual camera is live!", COLORS['success'])
                # Update button to show stop option
                update_button_state()
            else:
                # Process failed to start or exited immediately
                # Read error output to show what went wrong
                try:
                    stdout, stderr = asl_process.communicate(timeout=1)
                    error_msg = stderr.strip() if stderr else stdout.strip() if stdout else "Unknown error"
                    
                    # Print to console (terminal where main.py was launched)
                    print("\n" + "="*60)
                    print("ASL Translation Failed to Start:")
                    print("="*60)
                    if stderr:
                        print("STDERR:", stderr)
                    if stdout:
                        print("STDOUT:", stdout)
                    print("="*60 + "\n")
                    
                    # Truncate long error messages for GUI
                    if len(error_msg) > 120:
                        error_msg = error_msg[:120] + "..."
                    update_status(f"Error: {error_msg}", '#ef4444')
                except:
                    update_status("Error: Failed to start ASL translation (see terminal)", '#ef4444')
                is_asl_running = False
                asl_process = None
                btn_sign.config(state='normal')
                btn_speech.config(state='normal')
                update_button_state()

            # Monitor process in background
            def monitor_process():
                global asl_process, is_asl_running, manual_asl_stop
                if asl_process:
                    asl_process.wait()  # Wait for process to end
                    # Only update UI if process ended naturally (not manually stopped)
                    if not manual_asl_stop:
                        # Check return code - if non-zero, there was an error
                        if asl_process.returncode != 0:
                            # Try to read error output
                            try:
                                # Read any remaining output
                                stdout, stderr = asl_process.communicate(timeout=0.5)
                                error_msg = stderr.strip() if stderr else stdout.strip() if stdout else "Unknown error"
                                
                                # Print to console (terminal where main.py was launched)
                                print("\n" + "="*60)
                                print("ASL Translation Error:")
                                print("="*60)
                                if stderr:
                                    print("STDERR:", stderr)
                                if stdout:
                                    print("STDOUT:", stdout)
                                print("="*60 + "\n")
                                
                                # Show error in GUI (truncate if too long)
                                if len(error_msg) > 120:
                                    error_msg = error_msg[:120] + "..."
                                update_status(f"Error: {error_msg}", '#ef4444')
                            except:
                                update_status("ASL translation stopped with an error (see terminal)", '#ef4444')
                        else:
                            update_status("ASL translation stopped", COLORS['gray'])
                        is_asl_running = False
                        asl_process = None
                        btn_sign.config(state='normal')
                        btn_speech.config(state='normal')
                        update_button_state()

            monitor_thread = threading.Thread(target=monitor_process, daemon=True)
            monitor_thread.start()

        except Exception as e:
            update_status(f"Error starting ASL translation: {str(e)}", '#ef4444')
            is_asl_running = False
            asl_process = None
            btn_sign.config(state='normal')
            btn_speech.config(state='normal')
            update_button_state()

    # Run in a separate thread to avoid blocking GUI
    thread = threading.Thread(target=run_script, daemon=True)
    thread.start()

def run_speech_to_text():
    """Run the speech to text script and update GUI status"""
    global speech_process, is_running, manual_stop, is_asl_running

    if is_running:
        return

    # Don't allow both to run at the same time
    if is_asl_running:
        update_status("Please stop ASL translation first", COLORS['warning'])
        return

    # Reset manual stop flag
    manual_stop = False

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
            lang_name = LANGUAGES.get(selected_language, 'English')
            update_status(f"Speech-to-text is running ({lang_name})...", COLORS['success'])

            # Run the script with language argument
            speech_process = subprocess.Popen(
                [sys.executable, script_path, '--language', selected_language],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Give it a moment to start, then check if process is running
            import time
            time.sleep(0.5)  # Brief delay to let process start

            if speech_process.poll() is None:
                # Process is running
                lang_name = LANGUAGES.get(selected_language, 'English')
                update_status(f"✓ Speech-to-text ({lang_name}) - captions are live!", COLORS['success'])
                # Update button to show stop option
                update_button_state()
            else:
                # Process failed to start or exited immediately
                update_status("Error: Failed to start speech-to-text", '#ef4444')
                is_running = False
                speech_process = None
                btn_speech.config(state='normal')
                btn_sign.config(state='normal')
                update_button_state()

            # Monitor process in background
            def monitor_process():
                global speech_process, is_running, manual_stop
                if speech_process:
                    speech_process.wait()  # Wait for process to end
                    # Only update UI if process ended naturally (not manually stopped)
                    if not manual_stop:
                        is_running = False
                        speech_process = None
                        update_status("Speech-to-text stopped", COLORS['gray'])
                        btn_speech.config(state='normal')
                        btn_sign.config(state='normal')
                        update_button_state()

            monitor_thread = threading.Thread(target=monitor_process, daemon=True)
            monitor_thread.start()

        except Exception as e:
            update_status(f"Error starting speech-to-text: {str(e)}", '#ef4444')
            is_running = False
            speech_process = None
            btn_speech.config(state='normal')
            btn_sign.config(state='normal')
            update_button_state()
    
    # Run in a separate thread to avoid blocking GUI
    thread = threading.Thread(target=run_script, daemon=True)
    thread.start()

# Create window
root = tk.Tk()
root.title("Audibly")
root.geometry("500x400")
root.resizable(True, True)  # Allow resizing
root.configure(bg=COLORS['bg'])

# Fullscreen state
is_fullscreen = False

def toggle_fullscreen(event=None):
    """Toggle fullscreen mode"""
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes('-fullscreen', is_fullscreen)
    return "break"

def exit_fullscreen(event=None):
    """Exit fullscreen mode"""
    global is_fullscreen
    if is_fullscreen:
        is_fullscreen = False
        root.attributes('-fullscreen', False)
    return "break"

# Bind F11 to toggle fullscreen and Escape to exit fullscreen
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', exit_fullscreen)

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

# Title
title_frame = tk.Frame(main_frame, bg=COLORS['bg'])
title_frame.pack(pady=(0, 10))

title_part1 = tk.Label(
    title_frame,
    text="Audibly",
    font=('Inter', 28, 'bold'),
    bg=COLORS['bg'],
    fg=COLORS['primary']
)
title_part1.pack(side='left')

# Description text
description = tk.Label(
    main_frame,
    text="Select how you'd like to participate your meeting.",
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
    text="Sign Language-to-Text",
    style='Primary.TButton',
    command=run_sign_language,
    width=28
)
btn_sign.pack(pady=8, fill='x')

# Speech-to-Text section with language selector
speech_frame = tk.Frame(button_frame, bg=COLORS['bg'])
speech_frame.pack(pady=8, fill='x')

# Language selector label and dropdown
lang_selector_frame = tk.Frame(speech_frame, bg=COLORS['bg'])
lang_selector_frame.pack(fill='x', pady=(0, 5))

lang_label = tk.Label(
    lang_selector_frame,
    text="Language:",
    font=('Inter', 10),
    bg=COLORS['bg'],
    fg=COLORS['gray']
)
lang_label.pack(side='left', padx=(0, 8))

# Create language options for dropdown
language_options = [f"{name} ({code})" for code, name in LANGUAGES.items()]
language_var = tk.StringVar(value="English (en)")

def on_language_change(event=None):
    global selected_language
    # Extract language code from selection like "English (en)"
    selection = language_var.get()
    code = selection.split('(')[-1].rstrip(')')
    selected_language = code

lang_dropdown = ttk.Combobox(
    lang_selector_frame,
    textvariable=language_var,
    values=language_options,
    state='readonly',
    width=20,
    font=('Inter', 10)
)
lang_dropdown.pack(side='left', fill='x', expand=True)
lang_dropdown.bind('<<ComboboxSelected>>', on_language_change)

# Outline button (Speech to Text)
btn_speech = ttk.Button(
    speech_frame,
    text="Speech-to-Text",
    style='Outline.TButton',
    command=run_speech_to_text,
    width=28
)
btn_speech.pack(fill='x')

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

# Initialize button states
update_button_state()

# Center the window on screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

# Handle window close - cleanup process if running
def on_closing():
    global speech_process, asl_process, is_running, is_asl_running, manual_stop, manual_asl_stop
    if speech_process and is_running:
        manual_stop = True  # Prevent monitor_process from updating UI
        try:
            speech_process.terminate()
            speech_process.wait(timeout=2)
        except:
            try:
                speech_process.kill()
            except:
                pass
    if asl_process and is_asl_running:
        manual_asl_stop = True  # Prevent monitor_process from updating UI
        try:
            asl_process.terminate()
            asl_process.wait(timeout=2)
        except:
            try:
                asl_process.kill()
            except:
                pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()