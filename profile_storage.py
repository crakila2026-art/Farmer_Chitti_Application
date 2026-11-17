
import json
import os

PROFILE_FILE = "data/farmer_profiles.json"

def save_profile(profile):

    os.makedirs("data", exist_ok=True)

    profiles = []

    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r", encoding="utf-8") as file:
            profiles = json.load(file)

    profiles.append(profile)

    with open(PROFILE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            profiles,
            file,
            indent=4,
            ensure_ascii=False
        )

def load_profiles():

    if not os.path.exists(PROFILE_FILE):
        return []

    with open(PROFILE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
