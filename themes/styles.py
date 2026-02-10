
import json
import os

THEMES = {}

themes_dir = os.path.join(os.path.dirname(__file__), 'json')
if os.path.exists(themes_dir):
    for filename in os.listdir(themes_dir):
        if filename.endswith('.json'):
            theme_name = filename[:-5].capitalize()  # Remove .json and capitalize
            with open(os.path.join(themes_dir, filename), 'r') as f:
                THEMES[theme_name] = json.load(f)

# Manually add Ocean theme with ocean-themed colors
THEMES["Ocean"] = {
    "bg_color": "#001122",
    "border_color": "#004466",
    "title_color": "#00aaff",
    "text_color": "#66ddaa",
    "icon_color": "#2288cc",
    "font_family": "Segoe UI, Ubuntu, Sans-Serif",
    "title_font_size": 20,
    "text_font_size": 14
}
