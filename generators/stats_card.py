import svgwrite
from themes.styles import THEMES

def draw_stats_card(data, theme_name="Default", show_options=None, custom_colors=None):
    """
    Generates the Main Stats Card SVG.
    data: dict with user stats
    theme_name: string key from THEMES
    show_options: dict with toggles (e.g. {'stars': True, 'prs': False})
    """
    if show_options is None:
        show_options = {"stars": True, "commits": True, "repos": True, "followers": True}
        
    theme = THEMES.get(theme_name, THEMES["Default"]).copy()
    if custom_colors:
        theme.update(custom_colors)

    
    width = 450
    # Calculate height dynamically based on visible items
    base_height = 50
    item_height = 25
    visible_items = sum(1 for k, v in show_options.items() if v)
    height = base_height + (visible_items * item_height) + 10
    
    # --- Theme Logic ---
    if theme_name == "Glass":
        # Height adjustment for glass margins
        margin = 25
        height += margin * 2
        
        dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")
        
        # 1. Definitions
        # Blob Blur
        blob_blur = dwg.filter(id="blobBlur", x="-50%", y="-50%", width="200%", height="200%")
        blob_blur.feGaussianBlur(in_="SourceGraphic", stdDeviation=40)
        dwg.defs.add(blob_blur)
        
        # Text Glow
        text_glow = dwg.filter(id="textGlow")
        text_glow.feGaussianBlur(in_="SourceAlpha", stdDeviation=2, result="blur")
        text_glow.feOffset(in_="blur", dx=0, dy=0, result="offsetBlur")
        text_glow.feFlood(flood_color="#00e5ff", result="glowColor")
        text_glow.feComposite(in_="glowColor", in2="offsetBlur", operator="in", result="coloredBlur")
        text_glow.feMerge(["coloredBlur", "SourceGraphic"])
        dwg.defs.add(text_glow)

        # Gradients
        glass_grad = dwg.linearGradient(start=(0, 0), end=(1, 1), id="glassGrad")
        glass_grad.add_stop_color(0, "white", opacity=0.15)
        glass_grad.add_stop_color(1, "white", opacity=0.05)
        dwg.defs.add(glass_grad)
        
        border_grad = dwg.linearGradient(start=(0, 0), end=(1, 1), id="borderGrad")
        border_grad.add_stop_color(0, "white", opacity=0.4)
        border_grad.add_stop_color(1, "white", opacity=0.1)
        dwg.defs.add(border_grad)

        # 2. Background Base
        dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=16, ry=16, fill="#050511"))

        # 3. Neon Blobs
        dwg.add(dwg.circle(center=(0, 0), r=120, fill="#ff00ff", filter="url(#blobBlur)", opacity=0.6))
        dwg.add(dwg.circle(center=(width, height), r=140, fill="#00ffff", filter="url(#blobBlur)", opacity=0.5))
        dwg.add(dwg.circle(center=(width*0.8, height*0.3), r=80, fill="#9d4edd", filter="url(#blobBlur)", opacity=0.6))
        dwg.add(dwg.circle(center=(width*0.2, height*1.1), r=100, fill="#2563eb", filter="url(#blobBlur)", opacity=0.6))

        # 4. Glass Panel
        panel_width = width - margin * 2
        panel_height = height - margin * 2
        
        # Backdrop dim
        dwg.add(dwg.rect(insert=(margin, margin), size=(panel_width, panel_height), rx=16, ry=16, fill="#000000", opacity=0.2))
        
        # Glass Rect
        dwg.add(dwg.rect(
            insert=(margin, margin),
            size=(panel_width, panel_height),
            rx=16,
            ry=16,
            fill="url(#glassGrad)",
            stroke="url(#borderGrad)",
            stroke_width=1.5
        ))
        
        # 5. Content
        
        # Title
        dwg.add(dwg.text(f"{data['username']}'s Stats".upper(), insert=(width/2, margin + 40), 
                         fill="white", font_size=20, font_family="Verdana, sans-serif", font_weight="bold", 
                         text_anchor="middle", letter_spacing=2, filter="url(#textGlow)"))

        # Stats Items
        start_y = margin + 80
        current_y = start_y
        text_color = "#e2e8f0" # Light gray/white
        
        # Logic to handle N/A display for commits
        commit_val = data.get('total_commits', 0)
        display_commits = str(commit_val) if commit_val > 0 else "N/A"

        stats_map = [
            ("stars", "Total Stars", f"{data.get('total_stars', 0)}"),
            ("commits", "Total Commits", display_commits),
            ("repos", "Public Repos", f"{data.get('public_repos', 0)}"),
            ("followers", "Followers", f"{data.get('followers', 0)}")
        ]
        
        for key, label, value in stats_map:
            if show_options.get(key, True):
                # Icon (Neon Dot)
                dwg.add(dwg.circle(center=(margin + 30, current_y - 5), r=4, fill="#00e5ff", filter="url(#blobBlur)", opacity=0.8)) # Glow effect on dot
                dwg.add(dwg.circle(center=(margin + 30, current_y - 5), r=3, fill="#ffffff"))
                
                # Label
                dwg.add(dwg.text(f"{label}:", insert=(margin + 45, current_y), 
                                 fill=text_color, font_size=14, font_family="Verdana, sans-serif"))
                
                # Value
                dwg.add(dwg.text(f"{value}", insert=(width - margin - 40, current_y), 
                                 fill="white", font_size=14, font_family="Verdana, sans-serif", text_anchor="end", font_weight="bold"))
                                 
                current_y += 35 # Increased spacing for glass look

    else:
        # Default / Other Themes
        dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")
        
        # Background
        dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=10, ry=10, 
                         fill=theme["bg_color"], stroke=theme["border_color"], stroke_width=2))
        
        # Title
        font_family = theme["font_family"]
        dwg.add(dwg.text(f"{data['username']}'s Stats", insert=(20, 35), 
                         fill=theme["title_color"], font_size=theme["title_font_size"], font_family=font_family, font_weight="bold"))
        
        # Stats
        start_y = 65
        current_y = start_y
        text_color = theme["text_color"]
        font_size = theme["text_font_size"]
        
        # Logic to handle N/A display for commits
        commit_val = data.get('total_commits', 0)
        display_commits = str(commit_val) if commit_val > 0 else "N/A"

        stats_map = [
            ("stars", "Total Stars", f"{data.get('total_stars', 0)}"),
            ("commits", "Total Commits", display_commits),
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
