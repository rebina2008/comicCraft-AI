def build_comic_layout(image_paths, full_story, outline):
    layout = []
    
    for idx, panel_info in enumerate(outline, start=1):
        img_path = image_paths[idx - 1] if idx - 1 < len(image_paths) else ""
        
        # Story narrative text mapping
        narrative = f"Narrative for Panel {idx}: The story continues for {panel_info.get('title', f'Panel {idx}')}."
        
        layout.append({
            "panel": idx,
            "title": panel_info.get("title", f"Panel {idx}"),
            "image_path": img_path,
            "scene_description": panel_info.get("scene_description", ""),
            "text": narrative
        })

    return layout