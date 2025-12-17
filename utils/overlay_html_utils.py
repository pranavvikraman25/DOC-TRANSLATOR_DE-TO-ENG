def build_overlay_html(image_base64, ocr_boxes):
    html_boxes = ""

    for box in ocr_boxes:
        html_boxes += f"""
        <div style="
            position:absolute;
            left:{box['x']}px;
            top:{box['y']}px;
            width:{box['w']}px;
            height:{box['h']}px;
            background:rgba(255,255,0,0.35);
            font-size:12px;
            cursor:pointer;
        "
        title="{box['translated']}"
        ></div>
        """

    return f"""
    <div style="position:relative; display:inline-block;">
        <img src="data:image/png;base64,{image_base64}"
             style="width:100%;"/>

        <div style="position:absolute; top:0; left:0;">
            {html_boxes}
        </div>
    </div>

    <p style="font-size:14px; color:#555;">
    🟨 Hover over highlighted areas to see English translation
    </p>
    """
