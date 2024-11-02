import tkinter as tk
from tkinter import messagebox, ttk
import time
import pygame
import threading
from ConfigManager import ConfigManager
from SettingsWindow import SettingsWindow


class PomodoroTimer:
    # App Setup
    def __init__(self, master):
        self.master = master
        master.title("Pomodoro Timer")
        self.config = ConfigManager()

        # init sound player
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.config.get_setting('volume'))  # Default volume set to 50%
        self.sound_file_path = self.config.get_setting('sound_file_path')


        # Long break vs Short break based off of cycles, after 8 cycles
        self.state = False
        self.work_time = self.config.get_setting('work_time')
        self.break_time = self.config.get_setting('break_time')
        self.long_break_time = self.config.get_setting('long_break_time')
        self.current_time = self.work_time
        self.cycle = 0
        self.long_break_int = self.config.get_setting('long_break_int')
        self.short_break_int = self.config.get_setting('short_break_int')
        self.settings_window_instance = None

        self.init_ui()

    def init_ui(self):
        self.display = tk.Label(self.master, text=self.time_format(self.current_time), font=('Helvetica', 48), bg="white")
        self.display.pack()
        
        self.progress = ttk.Progressbar(self.master, orient="horizontal", length=300, mode="determinate", maximum=self.work_time)
        self.progress.pack()

        self.start_button = tk.Button(self.master, text="Start", command=self.start_timer, width=10, height=2)
        self.start_button.pack()

        self.pause_button = tk.Button(self.master, text="Pause", command=self.pause_timer, width=10, height=2)
        self.pause_button.pack()

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_timer, width=10, height=2)
        self.reset_button.pack()

        self.settings_button = tk.Button(self.master, text="Settings", command=self.open_settings_window, width=10, height=2)
        self.settings_button.pack()

    def update_timer(self):
        if self.state:
            if self.current_time > 0:
                self.current_time -= 1
                self.display.config(text=self.time_format(self.current_time))
                self.progress['value'] = self.work_time - self.current_time
                self.master.after(1000, self.update_timer)
            else:
                print("I GOT HERE")
                self.play_sound()
                self.state = False
                self.cycle += 1
                self.progress['value'] = 0
                self.manage_sessions()

    # App Settings
    def time_format(self, seconds):
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    def start_timer(self):
        if not self.state:
            self.state = True
            self.update_timer()

    def pause_timer(self):
        self.state = False

    def reset_timer(self):
        self.state = False
        self.cycle = 0
        self.current_time = self.work_time
        self.display.config(text=self.time_format(self.current_time))
        self.progress['value'] = 0
        self.progress['maximum'] = self.work_time

    # Helper Functions
    def play_sound(self):
        pygame.mixer.music.load(self.config.get_setting('sound_file_path'))
        pygame.mixer.music.play()
    
    def manage_sessions(self):
        if self.cycle % self.long_break_int == 0:
            self.current_time = self.long_break_time
            self.progress['maximum'] = self.long_break_time
        elif self.cycle % self.short_break_int == 0:
            self.current_time = self.break_time
            self.progress['maximum'] = self.break_time
        else:
            self.current_time = self.work_time
            self.progress['maximum'] = self.work_time
        
        session_type = "Break" if self.cycle % 2 == 0 else "Work"
        if session_type == "Break":
            messagebox.showinfo("Time's up!", f"Time for a {session_type}!")
        elif session_type == "Work" and self.cycle > 0:
            messagebox.showinfo("Time's up!", f"Time to get back to {session_type}!")
        elif session_type == "Work":
            messagebox.showinfo("Time's up!", f"Time to {session_type}!")
        
        # Update the button to reflect the next action
        button_text = "Start Work" if session_type == "Work" else "Start Break"
        self.start_button.config(text=button_text, command=self.start_timer)

    def open_settings_window(self):
        if self.settings_window_instance is not None and self.settings_window_instance.winfo_exists():
            # If the settings window is already open, bring it to the front
            self.settings_window_instance.lift()
        else:
            # Otherwise, create a new settings window and track the instance
            self.settings_window_instance = SettingsWindow(self.master, self.config, self.on_settings_window_close, self.reset_timer)
            
    def on_settings_window_close(self):
        self.settings_window_instance = None
        
    # Extra Features
    
    


root = tk.Tk()
app = PomodoroTimer(root)
root.mainloop()
