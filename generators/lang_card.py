import svgwrite
from themes.styles import THEMES

def draw_lang_card(data, theme_name="Default", custom_colors=None):
    """
    Generates the Top Languages Card SVG.
    """
    theme = THEMES.get(theme_name, THEMES["Default"]).copy()
    if custom_colors:
        theme.update(custom_colors)
        
    width = 450 # Resized from 300 to match Stats card
    
    # Dynamic height based on languages (max 5)
    langs = data.get("top_languages", [])
    if not langs:
        langs = [("No Data", 0)]
        
    item_height = 35
    header_height = 40
    height = header_height + (len(langs) * item_height) + 10

    if theme_name == "Glass":
        margin = 25
        height += margin * 2
        
        dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")
        
        # 1. Definitions
        blob_blur = dwg.filter(id="blobBlur", x="-50%", y="-50%", width="200%", height="200%")
        blob_blur.feGaussianBlur(in_="SourceGraphic", stdDeviation=40)
        dwg.defs.add(blob_blur)
        
        text_glow = dwg.filter(id="textGlow")
        text_glow.feGaussianBlur(in_="SourceAlpha", stdDeviation=2, result="blur")
        text_glow.feOffset(in_="blur", dx=0, dy=0, result="offsetBlur")
        text_glow.feFlood(flood_color="#00e5ff", result="glowColor")
        text_glow.feComposite(in_="glowColor", in2="offsetBlur", operator="in", result="coloredBlur")
        text_glow.feMerge(["coloredBlur", "SourceGraphic"])
        dwg.defs.add(text_glow)
        
        bar_grad = dwg.linearGradient(start=(0, 0), end=(1, 0), id="barGrad")
        bar_grad.add_stop_color(0, "#00ffff") # Cyan
        bar_grad.add_stop_color(1, "#ff00ff") # Magenta
        dwg.defs.add(bar_grad)

        glass_grad = dwg.linearGradient(start=(0, 0), end=(1, 1), id="glassGrad")
        glass_grad.add_stop_color(0, "white", opacity=0.15)
        glass_grad.add_stop_color(1, "white", opacity=0.05)
        dwg.defs.add(glass_grad)
        
        border_grad = dwg.linearGradient(start=(0, 0), end=(1, 1), id="borderGrad")
        border_grad.add_stop_color(0, "white", opacity=0.4)
        border_grad.add_stop_color(1, "white", opacity=0.1)
        dwg.defs.add(border_grad)

        # 2. Background
        dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=16, ry=16, fill="#050511"))
        dwg.add(dwg.circle(center=(0, 0), r=120, fill="#ff00ff", filter="url(#blobBlur)", opacity=0.6))
        dwg.add(dwg.circle(center=(width, height), r=140, fill="#00ffff", filter="url(#blobBlur)", opacity=0.5))
        dwg.add(dwg.circle(center=(width*0.8, height*0.3), r=80, fill="#9d4edd", filter="url(#blobBlur)", opacity=0.6))
        
        # 3. Glass Panel
        panel_width = width - margin * 2
        panel_height = height - margin * 2
        
        dwg.add(dwg.rect(insert=(margin, margin), size=(panel_width, panel_height), rx=16, ry=16, fill="#000000", opacity=0.2))
        dwg.add(dwg.rect(insert=(margin, margin), size=(panel_width, panel_height), rx=16, ry=16, 
                         fill="url(#glassGrad)", stroke="url(#borderGrad)", stroke_width=1.5))
        
        # 4. Content
        dwg.add(dwg.text("TOP LANGUAGES", insert=(width/2, margin + 40), 
                         fill="white", font_size=20, font_family="Verdana, sans-serif", font_weight="bold", 
                         text_anchor="middle", letter_spacing=2, filter="url(#textGlow)"))
        
        start_y = margin + 80
        total_usage = sum(count for _, count in langs)
        if total_usage == 0: total_usage = 1
        
        for i, (lang, count) in enumerate(langs):
            y = start_y + (i * 45) # Bigger spacing
            pct = (count / total_usage) * 100
            
            # Label
            dwg.add(dwg.text(lang, insert=(margin + 20, y), fill="white", 
                             font_size=14, font_family="Verdana, sans-serif"))
            
            # Percentage
            dwg.add(dwg.text(f"{pct:.1f}%", insert=(width - margin - 20, y), fill="white", 
                             font_size=14, font_family="Verdana, sans-serif", text_anchor="end"))
            
            # Bar Background
            bar_y = y + 8
            bar_width = width - margin*2 - 40
            dwg.add(dwg.rect(insert=(margin + 20, bar_y), size=(bar_width, 8), rx=4, ry=4, fill="white", opacity=0.1))
            
            # Bar Fill (Gradient)
            fill_width = (pct / 100) * bar_width
            dwg.add(dwg.rect(insert=(margin + 20, bar_y), size=(fill_width, 8), rx=4, ry=4, fill="url(#barGrad)"))

    else:
        # Default Theme
        dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")
        
        # Background
        dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=10, ry=10, 
                         fill=theme["bg_color"], stroke=theme["border_color"], stroke_width=2))
        
        # Title
        dwg.add(dwg.text("Top Languages", insert=(20, 30), 
                         fill=theme["title_color"], font_size=theme["title_font_size"], 
                         font_family=theme["font_family"], font_weight="bold"))
        
        # Content
        start_y = 60
        
        # Calculate total for percentages
        total_usage = sum(count for _, count in langs)
        if total_usage == 0: total_usage = 1
        
        for i, (lang, count) in enumerate(langs):
            y = start_y + (i * item_height)
            pct = (count / total_usage) * 100
            
            # Label
            dwg.add(dwg.text(lang, insert=(20, y), fill=theme["text_color"], 
                             font_size=theme["text_font_size"], font_family=theme["font_family"]))
            
            # Percentage Text
            dwg.add(dwg.text(f"{pct:.1f}%", insert=(width - 20, y), fill=theme["text_color"], 
                             font_size=theme["text_font_size"], font_family=theme["font_family"], text_anchor="end"))
            
            # Progress Bar Background
            bar_y = y + 5
            bar_width = width - 40
            dwg.add(dwg.rect(insert=(20, bar_y), size=(bar_width, 6), rx=3, ry=3, fill=theme["border_color"], opacity=0.3))
            
            # Progress Bar Fill
            fill_width = (pct / 100) * bar_width
            # Use icon_color or title_color for bar fill
            bar_color = theme["title_color"]
            dwg.add(dwg.rect(insert=(20, bar_y), size=(fill_width, 6), rx=3, ry=3, fill=bar_color))
            
    return dwg.tostring()
