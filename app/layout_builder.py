def build_comic_layout(images, full_story, outline):
    default_titles = [
        "PANEL 1 - INTRODUCTION",
        "PANEL 2 - RISING ACTION",
        "PANEL 3 - CONFRONTATION",
        "PANEL 4 - CLIMAX",
        "PANEL 5 - RESOLUTION"
    ]

    narrations_map = {}

    if full_story:
        blocks = full_story.split("---") if "---" in full_story else full_story.split("\n\n")
        for i, block in enumerate(blocks):
            p_num = str(i + 1)
            clean_block = block.replace(f"Panel {p_num}:", "").replace("**", "").strip()
            if clean_block:
                narrations_map[p_num] = clean_block

    layout = []

    for i in range(5):
        panel_key = str(i + 1)
        out_item = outline[i] if i < len(outline) and isinstance(outline[i], dict) else {}
        
        # 1. Panel Title
        p_title = default_titles[i]

        # 2. Story Narration (Only story for that panel)
        p_desc = out_item.get("scene_description", f"Story narration for panel {i+1}")
        p_narration = narrations_map.get(panel_key, p_desc)

        # 3. Panel Image URL
        img_url = images[i] if i < len(images) and images[i] else f"/static/panels/panel_{i+1}.png"

        layout.append({
            "panel": i + 1,
            "title": p_title,
            "image": img_url,
            "narrative": p_narration
        })

    return layout