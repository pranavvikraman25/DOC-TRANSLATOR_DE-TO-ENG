def book_page(image_base64, translated_text):
    return f"""
    <div style="
        max-width:900px;
        margin:auto;
        padding:30px;
        background:#f7f7f7;
        border-radius:12px;
        box-shadow:0 0 20px rgba(0,0,0,0.15);
    ">
        <img src="data:image/png;base64,{image_base64}"
             style="width:100%; border-radius:8px;" />

        <hr style="margin:30px 0"/>

        <div style="
            font-family:Georgia,serif;
            font-size:18px;
            line-height:1.7;
            color:#222;
        ">
            {translated_text.replace(chr(10), "<br>")}
        </div>
    </div>
    """
