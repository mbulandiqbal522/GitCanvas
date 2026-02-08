import svgwrite
from themes.styles import THEMES
from .svg_base import create_svg_base

def draw_stats_card(data, theme_name="Default", show_options=None, custom_colors=None):
    """
    Generates the Main Stats Card SVG.
    data: dict with user stats
    theme_name: string key from THEMES
    show_options: dict with toggles (e.g. {'stars': True, 'prs': False})
    """
    if show_options is None:
        show_options = {"stars": True, "commits": True, "repos": True, "followers": True}

    width = 450
    # Calculate height dynamically based on visible items
    base_height = 50
    item_height = 25
    visible_items = sum(1 for k, v in show_options.items() if v)
    height = base_height + (visible_items * item_height) + 10

    dwg, theme = create_svg_base(theme_name, custom_colors, width, height, f"{data['username']}'s Stats")

    font_family = theme["font_family"]

    # Stats
    start_y = 65
    current_y = start_y
    text_color = theme["text_color"]
    font_size = theme["text_font_size"]
    
    stats_map = [
        ("stars", "Total Stars", f"{data.get('total_stars', 0)}"),
        ("commits", "Total Commits (Year)", f"{data.get('total_commits', 'N/A')}"),
        ("repos", "Public Repos", f"{data.get('public_repos', 0)}"),
        ("followers", "Followers", f"{data.get('followers', 0)}")
    ]
    
    for key, label, value in stats_map:
        if show_options.get(key, True):
            # Icon approximation (Circle)
            dwg.add(dwg.circle(center=(30, current_y - 5), r=4, fill=theme["icon_color"]))
            
            # Label
            dwg.add(dwg.text(f"{label}:", insert=(45, current_y), 
                             fill=text_color, font_size=font_size, font_family=font_family))
            
            # Value (Right aligned roughly)
            dwg.add(dwg.text(f"{value}", insert=(width - 40, current_y), 
                             fill=text_color, font_size=font_size, font_family=font_family, text_anchor="end", font_weight="bold"))
                             
            current_y += item_height
            
    return dwg.tostring()
