import tkinter as tk
from tkinter import ttk
import threading
from voice_control import listen_for_command
from gesture_control import GestureControl
from commands import execute_command

class PCControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Control with Voice and Gesture")
        self.root.attributes('-fullscreen', True)  # Full-screen mode
        self.root.configure(bg="#0D1B2A")  # Dark blue background color

        # Custom font
        self.custom_font = ("Helvetica", 16)

        # Main Frame with rounded corners effect
        self.main_frame = tk.Frame(root, bg="#1B263B", bd=2, relief="ridge")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=1100, height=750)

        # Title Label with shadow effect
        self.title_label = tk.Label(
            self.main_frame,
            text="PC Control App",
            font=("Helvetica", 36, "bold"),
            fg="#E0E1DD",  # Light text color
            bg="#1B263B"
        )
        self.title_label.pack(pady=20)

        # Subtitle Label
        self.subtitle_label = tk.Label(
            self.main_frame,
            text="Control your PC with Voice and Gestures",
            font=("Helvetica", 18, "italic"),
            fg="#778DA9",
            bg="#1B263B"
        )
        self.subtitle_label.pack(pady=10)

        # Separator for better sectioning
        self.separator = ttk.Separator(self.main_frame, orient="horizontal")
        self.separator.pack(fill="x", pady=10)

        # Voice Control Section
        self.voice_label = tk.Label(
            self.main_frame,
            text="🎤 Voice Control",
            font=self.custom_font,
            fg="#E0E1DD",
            bg="#1B263B"
        )
        self.voice_label.pack(pady=10)

        self.voice_button = ttk.Button(
            self.main_frame,
            text="Start Voice Control",
            command=self.start_voice_thread,
            style="Custom.TButton"
        )
        self.voice_button.pack(pady=15)

        # Gesture Control Section
        self.gesture_label = tk.Label(
            self.main_frame,
            text="✋ Gesture Control",
            font=self.custom_font,
            fg="#E0E1DD",
            bg="#1B263B"
        )
        self.gesture_label.pack(pady=10)

        self.gesture_button = ttk.Button(
            self.main_frame,
            text="Start Gesture Control",
            command=self.start_gesture_thread,
            style="Custom.TButton"
        )
        self.gesture_button.pack(pady=15)

        # Dummy Content Section with a card-like appearance
        self.dummy_frame = tk.Frame(self.main_frame, bg="#0D1B2A", bd=1, relief="solid")
        self.dummy_frame.pack(pady=20, padx=20, fill="x")

        self.dummy_label = tk.Label(
            self.dummy_frame,
            text="📋 What's up",
            font=self.custom_font,
            fg="#E0E1DD",
            bg="#0D1B2A"
        )
        self.dummy_label.pack(pady=10)

        self.dummy_text = tk.Label(
            self.dummy_frame,
            text="This is PC Controller Using Gesture And Voice",
            font=("Helvetica", 14),
            fg="#778DA9",
            bg="#0D1B2A",
            wraplength=800,
            justify="center"
        )
        self.dummy_text.pack(pady=10)

        # Exit Button
        self.exit_button = ttk.Button(
            self.main_frame,
            text="🚪 Exit",
            command=self.stop_gesture_control,
            style="Custom.TButton"
        )
        self.exit_button.pack(pady=30)

        # Fullscreen Toggle Button
        self.fullscreen_button = ttk.Button(
            self.main_frame,
            text="🔲 Toggle Fullscreen",
            command=self.toggle_fullscreen,
            style="Custom.TButton"
        )
        self.fullscreen_button.pack(pady=10)

        # Footer Label with subtle border
        self.footer_label = tk.Label(
            self.main_frame,
            text="© 2023 PC Control App | Designed by Sarthak",
            font=("Helvetica", 12),
            fg="#778DA9",
            bg="#1B263B",
            relief="ridge",
            bd=1
        )
        self.footer_label.pack(side="bottom", pady=10)

        # Custom Button Style
        self.style = ttk.Style()
        self.style.configure(
            "Custom.TButton",
            font=self.custom_font,
            background="#415A77",
            foreground="#E0E1DD",
            padding=10,
            borderwidth=0,  # Removed border
            relief="flat"  # Flat style for buttons
        )
        self.style.map(
            "Custom.TButton",
            background=[("active", "#778DA9")],
            foreground=[("active", "#E0E1DD")]
        )

        # Gesture Control Instance
        self.gesture_control = GestureControl()

        # Fullscreen State
        self.is_fullscreen = True

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)

    def start_voice_thread(self):
        voice_thread = threading.Thread(target=self.start_voice_command)
        voice_thread.start()

    def start_gesture_thread(self):
        gesture_thread = threading.Thread(target=self.start_gesture_command)
        gesture_thread.start()

    def start_voice_command(self):
        command = listen_for_command()
        if command:
            execute_command(command)

    def start_gesture_command(self):
        self.gesture_control.start()

    def stop_gesture_control(self):
        self.gesture_control.stop()
        self.root.quit()
