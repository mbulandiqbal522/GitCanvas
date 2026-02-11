import svgwrite
import math
from themes.styles import THEMES
from .svg_base import create_svg_base

def draw_lang_card(data, theme_name="Default", custom_colors=None, excluded_languages=None):
    """
    Generates the Top Languages Card SVG.
    
    Args:
        data: dict with user stats including 'top_languages'
        theme_name: string key from THEMES
        custom_colors: dict with custom color overrides
        excluded_languages: list of language names to exclude (case-insensitive)
    """
    # FIXED: Handle both string theme name and pre-resolved theme dict
    if isinstance(theme_name, dict):
        # Already a theme dictionary (e.g., current_theme_opts from app.py)
        theme = theme_name.copy()
    else:
        # Convert theme_name string to actual theme dictionary
        theme = THEMES.get(theme_name, THEMES["Default"]).copy()
        
    width = 450 # Resized from 300 to match Stats card
    
        # Apply custom colors if provided
        if custom_colors:
            theme.update(custom_colors)

    width = 300
    # Dynamic height based on languages (max 5)
    langs = data.get("top_languages", [])
    
    # Apply exclusion filter if provided
    if excluded_languages and langs:
        # Convert excluded languages to lowercase for case-insensitive matching
        excluded_lower = [lang.lower() for lang in excluded_languages]
        langs = [
            (lang, count) 
            for lang, count in langs 
            if lang.lower() not in excluded_lower
        ]
    
    # Handle empty result after filtering
    if not langs:
        langs = [("No Data", 0)]

    item_height = 35
    header_height = 40
    height = header_height + (len(langs) * item_height) + 10

    if theme_name == "Glass":
        margin = 25
        # Recalculate height: Margin + Header + Items + Item Padding + Margin
        header_height = 80
        item_spacing = 45
        height = margin + header_height + (len(langs) * item_spacing) + margin
        
        dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")
        
        # Theme Variables
        bg_col = theme.get("bg_color", "#050511")
        title_col = theme.get("title_color", "#00e5ff")
        text_col = theme.get("text_color", "#e2e8f0")
        border_col = theme.get("border_color", "white")
        
        # 1. Definitions
        blob_blur = dwg.filter(id="blobBlur", x="-50%", y="-50%", width="200%", height="200%")
        blob_blur.feGaussianBlur(in_="SourceGraphic", stdDeviation=40)
        dwg.defs.add(blob_blur)
        
        # Progress Bar Fill with sine wave animation
        fill_width = (pct / 100) * bar_width
        bar_color = theme["title_color"]
        
        # Create the progress bar fill
        progress_fill = dwg.rect(
            insert=(20, bar_y), 
            size=(0, 6),  # Start with 0 width
            rx=3, 
            ry=3, 
            fill=bar_color
        )
        
        # Add sine wave animation 
        progress_fill.add(dwg.animate(
            attributeName="width",
            values="0;{0}".format(fill_width),
            keyTimes="0;1",
            calcMode="spline",
            keySplines="0.445 0.05 0.55 0.95",  # Sine curve approximation
            dur="1s",
            begin="0s",
            fill="freeze"
        ))
        
        dwg.add(progress_fill)
        
    return dwg.tostring()
