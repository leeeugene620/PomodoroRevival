import json
import os

class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.default_config = {
            "sound_file_path": "src/sound/timer_alert.mp3",
            "volume": 0.5,
            "work_time": 1500,  # 25 minutes
            "break_time": 300,  # 5 minutes
            "long_break_time": 900,  # 15 minutes
            "long_break_int": 8, # How many work sessions before a long break
            "short_break_int": 2 # How many work sessions before a short break
        }
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as file:
                return json.load(file)
        else:
            return self.default_config

    def save_config(self):
        with open(self.config_path, 'w') as file:
            json.dump(self.config, file, indent=4)

    def get_setting(self, key):
        return self.config.get(key, self.default_config.get(key))

    def set_setting(self, key, value):
        self.config[key] = value
        self.save_config()