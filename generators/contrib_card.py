import svgwrite
import random
from themes.styles import THEMES

def draw_contrib_card(data, theme_name="Default", custom_colors=None):
    """
    Generates the Contribution Graph Card SVG.
    Supports 'Snake', 'Space', 'Marvel' visualization logic.
    """
    theme = THEMES.get(theme_name, THEMES["Default"]).copy()
    if custom_colors:
        theme.update(custom_colors)
    
    # Fake contribution data for visualization if not fully populated
    # In a real scenario, data['contributions'] would have the last ~15-30 days or weeks
    # For MVP we simulate a strip of activity
    
    # Allow a slightly larger playground for Gaming / Snake
    if theme_name == "Gaming":
        width = 560
        height = 180
    else:
        width = 500
        height = 150
    dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")
    
    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=10, ry=10, 
                     fill=theme["bg_color"], stroke=theme["border_color"], stroke_width=2))
    
    # Title
    title = f"{data['username']}'s Contributions"
    dwg.add(dwg.text(title, insert=(20, 30), 
                     fill=theme["title_color"], font_size=theme["title_font_size"], 
                     font_family=theme["font_family"], font_weight="bold"))
    
    # Theme Specific Logic
    
    # Theme Specific Logic
    if theme_name == "Gaming":

        # Snake / Gaming Theme Refactor
        # Continuous Zig-Zag Path (GitHub-like grid but continuous)
        
        contributions = data.get("contributions", []) or []
        contributions = contributions[-196:] # Last 28 weeks approx
        
        tile_size = 12
        gap = 2
        cols = 28
        rows = 7
        
        start_x = 20
        start_y = 55
        
        # Retro Score
        dwg.add(dwg.text(f"SCORE: {data.get('total_commits', '0')}", insert=(width - 150, 30), 
                         fill=theme["text_color"], font_family="Courier New", font_size=14, font_weight="bold"))

        # --- 1. Coordinate Mapping (Zig-Zag) ---
        snake_path = [] # List of (x, y, data)
        
        # Create full grid of 196 slots (fill missing days with 0 count if needed)
        # We need exactly cols*rows points for a perfect grid
        total_slots = cols * rows
        padded_contribs = contributions + [{"count": 0}] * (total_slots - len(contributions))
        
        for idx, day in enumerate(padded_contribs):
            if idx >= total_slots: break
            
            col = idx // rows
            row_in_col = idx % rows
            
            # Zig-Zag Logic
            if col % 2 == 1:
                # Odd columns: Bottom -> Top
                row = (rows - 1) - row_in_col
            else:
                # Even columns: Top -> Bottom
                row = row_in_col
                
            x = start_x + col * (tile_size + gap)
            y = start_y + row * (tile_size + gap)
            
            snake_path.append({
                "x": x, 
                "y": y, 
                "count": day.get("count", 0), 
                "date": day.get("date", ""),
                "idx": idx,
                "col": col,
                "row": row
            })

        # --- 2. Identify Food (High Commits) ---
        # Get threshold for "Food"
        counts = [p["count"] for p in snake_path]
        max_count = max(counts) if counts else 0
        food_threshold = max(2, max_count * 0.6) # Top 40% intensity or at least 2 commits
        
        food_indices = {p["idx"] for p in snake_path if p["count"] >= food_threshold}
        
        # --- 3. Draw Background Grid (Faint tracks) ---
        for p in snake_path:
            dwg.add(dwg.rect(insert=(p["x"], p["y"]), size=(tile_size, tile_size), 
                             fill="#1e293b", rx=2, ry=2))
        
        # --- 4. Draw Snake Body ---
        # Gradient Colors
        c_tail = (13, 59, 13)    # #0d3b0d (Dark Green)
        c_head = (124, 255, 0)   # #7CFF00 (Neon Green)
        
        # Build connected segments
        # We draw a rect for each day.
        # To look like a "snake", we just draw them. 
        # Since they are adjacent in list, they form a line.
        
        for i, p in enumerate(snake_path):
            # Gradient
            t = i / max(1, len(snake_path) - 1)
            r = int(c_tail[0] * (1-t) + c_head[0] * t)
            g = int(c_tail[1] * (1-t) + c_head[1] * t)
            b = int(c_tail[2] * (1-t) + c_head[2] * t)
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Draw segment
            # If it's a food spot, maybe make it bulge? Or just standard segment.
            # User guideline: "High-commit days are treated as 'food' targets"
            # We'll draw food ON TOP later.
            
            dwg.add(dwg.rect(
                insert=(p["x"], p["y"]), 
                size=(tile_size, tile_size), 
                fill=color, 
                rx=3, ry=3,
                stroke="#020617", stroke_width=1
            ))
            
            # Connectors (to hide gaps between tiles and make it look continuous)
            if i < len(snake_path) - 1:
                next_p = snake_path[i+1]
                # Determine direction
                dx = next_p["x"] - p["x"]
                dy = next_p["y"] - p["y"]
                
                # Fill the gap
                if dx != 0: # Moving Right
                    dwg.add(dwg.rect(insert=(p["x"] + tile_size/2, p["y"] + 2), size=(tile_size, tile_size - 4), fill=color))
                elif dy > 0: # Moving Down
                    dwg.add(dwg.rect(insert=(p["x"] + 2, p["y"] + tile_size/2), size=(tile_size - 4, tile_size), fill=color))
                elif dy < 0: # Moving Up
                    dwg.add(dwg.rect(insert=(p["x"] + 2, next_p["y"] + tile_size/2), size=(tile_size - 4, tile_size), fill=color))

        # --- 5. Draw Food (Apples) ---
        for i, p in enumerate(snake_path):
            if i in food_indices:
                cx = p["x"] + tile_size/2
                cy = p["y"] + tile_size/2
                # Apple
                dwg.add(dwg.circle(center=(cx, cy), r=4, fill="#ff1744")) # Bright Red
                # Leaf
                dwg.add(dwg.rect(insert=(cx - 1, cy - 5), size=(2, 3), fill="#7CFF00"))
        
        # --- 6. Draw Head ---
        head = snake_path[-1] 
        hx, hy = head["x"], head["y"]
        
        # Head Shape (Slightly larger)
        dwg.add(dwg.rect(insert=(hx-1, hy-1), size=(tile_size+2, tile_size+2), 
                         fill="#7CFF00", rx=3, ry=3, stroke="white", stroke_width=1))
        
        # Glow
        head_glow = dwg.filter(id="headGlow")
        head_glow.feGaussianBlur(in_="SourceAlpha", stdDeviation=3)
        head_glow.feFlood(flood_color="#7CFF00")
        head_glow.feComposite(operator="in", in2="SourceGraphic")
        dwg.defs.add(head_glow)
        dwg.add(dwg.rect(insert=(hx-2, hy-2), size=(tile_size+4, tile_size+4), 
                         fill="#7CFF00", opacity=0.4, filter="url(#headGlow)"))
                         
        # Eyes
        # Determine direction based on last move?
        # Last column is index 27 (Odd -> Up) or 26 (Even -> Down)?
        # 196 days = 28 cols (0-27). Col 27 is Odd -> Bottom-Up.
        # So head is pointing Up.
        # Eyes at top.
        
        last_col = head["col"]
        if last_col % 2 == 1: # Moving Up
            # Eyes at top
            eyey = hy + 3
        else: # Moving Down
            # Eyes at bottom
            eyey = hy + tile_size - 5
            
        dwg.add(dwg.rect(insert=(hx + 2, eyey), size=(3, 3), fill="black"))
        dwg.add(dwg.rect(insert=(hx + tile_size - 5, eyey), size=(3, 3), fill="black"))

    elif theme_name == "Space":
        # Spaceship logic
        # Commits are stars.
        
        # Draw random stars
        for _ in range(30):
            sx = random.randint(20, width-20)
            sy = random.randint(50, height-20)
            r = random.uniform(1, 3)
            dwg.add(dwg.circle(center=(sx, sy), r=r, fill="white", opacity=random.uniform(0.5, 1.0)))
            
        # Draw Spaceship (Simple triangle)
        ship_x = width - 60
        ship_y = height / 2 + 10
        
        # Flame
        dwg.add(dwg.path(d=f"M {ship_x-10} {ship_y} L {ship_x-20} {ship_y-5} L {ship_x-20} {ship_y+5} Z", fill="orange"))
        # Body
        dwg.add(dwg.path(d=f"M {ship_x} {ship_y} L {ship_x-15} {ship_y-8} L {ship_x-15} {ship_y+8} Z", fill="#00a8ff"))
        
        # Beam eating a star?
        dwg.add(dwg.line(start=(ship_x, ship_y), end=(width, ship_y), stroke="#00a8ff", stroke_width=2, stroke_dasharray="4,2"))

    elif theme_name == "Marvel":
        # Infinity Stones
        stones = ["#FFD700", "#FF0000", "#0000FF", "#800080", "#008000", "#FFA500"] # Mind, Reality, Space, Power, Time, Soul
        
        # Draw slots
        cx = width / 2
        cy = height / 2 + 10
        
        # Gauntlet hints? Or just the stones glowing
        for i, color in enumerate(stones):
            sx = 60 + i * 60
            sy = cy
            
            # Glow
            dwg.add(dwg.circle(center=(sx, sy), r=15, fill=color, opacity=0.3))
            # Stone
            dwg.add(dwg.circle(center=(sx, sy), r=8, fill=color, stroke="white", stroke_width=1))
            
            # Label below
            dwg.add(dwg.text(f"Stone {i+1}", insert=(sx, sy+30), fill="white", font_size=10, text_anchor="middle"))
            
        dwg.add(dwg.text("SNAP!", insert=(width-80, cy), fill=theme["title_color"], font_size=24, font_weight="bold", font_family="Impact"))

    elif theme_name == "Glass":
        # Neon Liquid Glassmorphism Theme
        
        # Theme Variables
        bg_col = theme.get("bg_color", "#050511")
        title_col = theme.get("title_color", "#00e5ff")
        text_col = theme.get("text_color", "#e0e0e0")
        border_col = theme.get("border_color", "white")
        
        # --- 1. Definining Filters & Gradients ---
        
        # Blur filter for background blobs
        blob_blur = dwg.filter(id="blobBlur", x="-50%", y="-50%", width="200%", height="200%")
        blob_blur.feGaussianBlur(in_="SourceGraphic", stdDeviation=40)
        dwg.defs.add(blob_blur)
        
        # Glow filter for text
        text_glow = dwg.filter(id="textGlow")
        text_glow.feGaussianBlur(in_="SourceAlpha", stdDeviation=2, result="blur")
        text_glow.feOffset(in_="blur", dx=0, dy=0, result="offsetBlur")
        text_glow.feFlood(flood_color=title_col, result="glowColor") # Dynamic Glow
        text_glow.feComposite(in_="glowColor", in2="offsetBlur", operator="in", result="coloredBlur")
        
        # Merge glow with original text
        text_glow.feMerge(["coloredBlur", "SourceGraphic"])
        
        dwg.defs.add(text_glow)

        # Glass Panel Gradient (Subtle diagonal)
        glass_grad = dwg.linearGradient(start=(0, 0), end=(1, 1), id="glassGrad")
        glass_grad.add_stop_color(0, "white", opacity=0.15)
        glass_grad.add_stop_color(1, "white", opacity=0.05)
        dwg.defs.add(glass_grad)
        
        # Border Gradient
        border_grad = dwg.linearGradient(start=(0, 0), end=(1, 1), id="borderGrad")
        border_grad.add_stop_color(0, border_col, opacity=0.4)
        border_grad.add_stop_color(1, border_col, opacity=0.1)
        dwg.defs.add(border_grad)

        # --- 2. Background Base ---
        dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=16, ry=16, fill=bg_col)) # Dynamic background

        # --- 3. Neon Blobs (The "Liquid") ---
        # Magenta/Pink Blob (Top Left)
        dwg.add(dwg.circle(center=(0, 0), r=120, fill="#ff00ff", filter="url(#blobBlur)", opacity=0.6))
        
        # Cyan/Blue Blob (Bottom Right)
        dwg.add(dwg.circle(center=(width, height), r=140, fill="#00ffff", filter="url(#blobBlur)", opacity=0.5))
        
        # Purple Blob (Middle Right)
        dwg.add(dwg.circle(center=(width*0.8, height*0.3), r=80, fill=title_col, filter="url(#blobBlur)", opacity=0.6))
         
        # Deep Blue Blob (Bottom Left)
        dwg.add(dwg.circle(center=(width*0.2, height*1.1), r=100, fill="#2563eb", filter="url(#blobBlur)", opacity=0.6))


        # --- 4. The Glass Panel ---
        margin = 25
        panel_width = width - margin * 2
        panel_height = height - margin * 2
        
        # Initial Backdrop blur simulation (Darken overlay)
        dwg.add(dwg.rect(insert=(margin, margin), size=(panel_width, panel_height), rx=16, ry=16, fill="#000000", opacity=0.2))

        # The Glass Rect
        dwg.add(
            dwg.rect(
                insert=(margin, margin),
                size=(panel_width, panel_height),
                rx=16,
                ry=16,
                fill="url(#glassGrad)",
                stroke="url(#borderGrad)",
                stroke_width=1.5
            )
        )

        # --- 5. Content ---
        
        # Title (Styled like "GLASSMORPHISM" in reference)
        dwg.add(
            dwg.text(
                title.upper(),
                insert=(width/2, margin + 40),
                fill="white",
                font_size=20,
                font_family="Verdana, sans-serif",
                font_weight="bold",
                text_anchor="middle",
                letter_spacing=4,
                filter="url(#textGlow)" # Add neon glow to text
            )
        )
        
        # Subtitle
        dwg.add(
            dwg.text(
                "NEON LIQUID",
                insert=(width/2, margin + 60),
                fill=text_col,
                font_size=10,
                font_family="Verdana, sans-serif",
                letter_spacing=2,
                text_anchor="middle",
                opacity=0.8
            )
        )

        # --- 6. Contributions Grid (Bubbles) ---
        # Grid settings
        contributions = data.get("contributions", [])[-119:] # Fit less days for cleaner look (~17 weeks)
        cols = 17 
        rows = 7
        
        grid_width = cols * 20
        grid_height = rows * 20
        start_x = (width - grid_width) / 2 + 10 # Center the grid
        start_y = margin + 80
        
        for i, day in enumerate(contributions):
            col = i // rows
            row = i % rows
            
            cx = start_x + col * 22
            cy = start_y + row * 22
            
            count = day.get("count", 0)
            
            # Bubble aesthetic
            r = 6
            bg_opacity = 0.1
            fill = "#ffffff"
            stroke = "none"
            
            if count > 0:
                bg_opacity = 0.8
                # Gradient of intensity
                if count < 3:
                     fill = "#00ffff" # Cyan
                     r = 6.5
                elif count < 6:
                     fill = title_col # Use Title Color for mid-range (Dynamic)
                     r = 7.5
                else:
                     fill = "#ff0099" # Pink
                     r = 8.5
                
                # Glow effect for active cells
                # Simple duplicate for glow
                dwg.add(dwg.circle(center=(cx, cy), r=r+2, fill=fill, opacity=0.3, filter="url(#blobBlur)"))

            dwg.add(dwg.circle(center=(cx, cy), r=r, fill=fill, fill_opacity=bg_opacity))
    else:
        # Default Grid (Github Style)
        # Just simple squares
        box_size = 12
        gap = 3
        start_x = 20
        start_y = 60
        
        count = 0
        for col in range(25): # 25 weeks horizontal
            for row in range(5): # 5 days vertical
                x = start_x + col * (box_size + gap)
                y = start_y + row * (box_size + gap)
                
                # Random "green" level
                level = random.choice([0, 1, 2, 3, 4])
                colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
                
                # Use theme override if set
                # For default we stick to standard GH colors unless customized logic is deeper
                # But let's respect the theme accent
                fill = colors[level]
                if level > 0:
                     # Mix with theme accent roughly?
                     # For now just keep standard GH style for "Default"
                     pass
                     
                dwg.add(dwg.rect(insert=(x, y), size=(box_size, box_size), fill=fill, rx=2, ry=2))
                
    return dwg.tostring()
