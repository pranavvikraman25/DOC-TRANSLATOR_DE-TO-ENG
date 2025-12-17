def build_overlay_html(image_base64, ocr_boxes):
    overlays = ""
    for box in ocr_boxes:
        overlays += f"""
        <div style="
            position:absolute;
            left:{box['x']}px;
            top:{box['y']}px;
            width:{box['w']}px;
            height:{box['h']}px;
            background:rgba(255,255,0,0.35);
            cursor:pointer;
        " title="{box['translated']}"></div>
        """

    return f"""
    <div style="position:relative;">
        <img src="data:image/png;base64,{image_base64}" style="width:100%;" />
        <div style="position:absolute;top:0;left:0;">
            {overlays}
        </div>
    </div>
    <p>🟨 Hover highlighted areas for English translation</p>
    """

