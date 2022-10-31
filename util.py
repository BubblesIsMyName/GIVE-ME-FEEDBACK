#%%
import json
import mediapipe as mp # Import mediapipe
from pathlib import Path

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!! Utility functions !!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

settings_path = Path.cwd().joinpath("data","settings.json").as_posix()
def read_settings(settings_path = settings_path):
    file = open(settings_path,"r")
    settings_dict = {}
    settings_dict = json.load(file)
    file.close()
    return settings_dict
