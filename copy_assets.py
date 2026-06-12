import shutil
import os

src_login = r"C:\Users\Likith.N\.gemini\antigravity-ide\brain\6067dd5a-2ea1-4a0b-8801-75dd660b2346\login_background_1780286848893.png"
src_dash = r"C:\Users\Likith.N\.gemini\antigravity-ide\brain\785b0cb5-90e0-46f0-baf0-bade78638b9b\dashboard_background_1780300527259.png"

dest_login = r"C:\Users\Likith.N\.gemini\antigravity\scratch\financial-corruption-app\assets\login_bg.png"
dest_dash = r"C:\Users\Likith.N\.gemini\antigravity\scratch\financial-corruption-app\assets\dashboard_bg.png"

os.makedirs(os.path.dirname(dest_login), exist_ok=True)

if os.path.exists(src_login):
    try:
        shutil.copy(src_login, dest_login)
        print("Successfully copied login background image.")
    except Exception as e:
        print(f"Error copying login image: {e}")

if os.path.exists(src_dash):
    try:
        shutil.copy(src_dash, dest_dash)
        print("Successfully copied dashboard background image.")
    except Exception as e:
        print(f"Error copying dashboard image: {e}")
