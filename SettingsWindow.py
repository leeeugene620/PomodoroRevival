import tkinter as tk
import pygame

class SettingsWindow(tk.Toplevel):
        def __init__(self, master, config, on_close_callback, reset_timer):
            super().__init__(master)
            self.master = master
            self.title("Settings")
            self.config = config
            self.on_close_callback = on_close_callback
            self.reset_timer = reset_timer
            self.protocol("WM_DELETE_WINDOW", self.close_window)
            self.settings_window()

        def settings_window(self):
            from tkinter import filedialog

            # Creating work duration setting
            self.work_duration_entry = self.create_labeled_entry("Work Duration (minutes):", self.config.get_setting('work_time') // 60)

            # Creating break duration setting
            self.break_duration_entry = self.create_labeled_entry("Break Duration (minutes):", self.config.get_setting('break_time') // 60)

            # Creating long break duration setting
            self.long_break_duration_entry = self.create_labeled_entry("Long Break Duration (minutes):", self.config.get_setting('long_break_time') // 60)

            # Creating long break int setting
            self.long_break_int_entry = self.create_labeled_entry("Long Break Interval (Default 8 Work Durations):", self.config.get_setting('long_break_int'))

            # Creating long break int setting
            self.short_break_int_entry = self.create_labeled_entry("Short Break Interval (Default 2 Work Durations):", self.config.get_setting('short_break_int'))

            # Creating volume control
            self.volume_scale = self.create_scale("Volume:", self.config.get_setting('volume') * 100)

            # Creating sound file selection
            self.sound_path_entry = self.create_labeled_entry("Alert Sound:", self.config.get_setting('sound_file_path'), width=50)

            def browse_sound():
                filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                    filetypes=(("audio files", "*.mp3 *.wav"), ("all files", "*.*")))
                if filename:
                    self.sound_path_entry.delete(0, tk.END)
                    self.sound_path_entry.insert(0, filename)

            self.browse_button = tk.Button(self, text="Browse...", command=browse_sound)
            self.browse_button.pack()

            #Reset Sound
            def reset_sound_path(self):
                self.sound_path_entry.delete(0, tk.END)
                self.sound_path_entry.insert(0, "src/sound/timer_alert.mp3")

            self.reset_sound_button = tk.Button(self, text="Reset Sound", command=lambda: reset_sound_path(self))
            self.reset_sound_button.pack()

            # Save Button
            self.save_button = tk.Button(self, text="Save", command=lambda: self.save_settings(self.sound_path_entry.get()))
            self.save_button.pack()

        def save_settings(self, sound_path):
            self.config.set_setting('work_time', int(self.work_duration_entry.get()) * 60)
            self.config.set_setting('break_time', int(self.break_duration_entry.get()) * 60)
            self.config.set_setting('long_break_time', int(self.long_break_duration_entry.get()) * 60)
            self.config.set_setting('long_break_int', int(self.long_break_int_entry.get()))
            self.config.set_setting('short_break_int', int(self.short_break_int_entry.get()))
            self.config.set_setting('volume', self.volume_scale.get() / 100.0)
            pygame.mixer.music.set_volume(self.config.get_setting('volume'))  # Apply new volume immediately
            self.config.set_setting('sound_file_path', sound_path)
            self.config.save_config()  # Save all settings to the config file
            self.reset_timer()
            self.close_window()

        def close_window(self):
            self.on_close_callback()  # Call the passed in callback
            self.destroy()  # Destroy the window

        def create_labeled_entry(self, label, value, width=20):
            tk.Label(self, text=label).pack()
            entry = tk.Entry(self, width=width)
            entry.insert(0, str(value))
            entry.pack()
            return entry
    
        def create_scale(self, label, value):
            tk.Label(self, text=label).pack()
            scale = tk.Scale(self, from_=0, to=100, orient='horizontal')
            scale.set(int(value))
            scale.pack()
            return scale