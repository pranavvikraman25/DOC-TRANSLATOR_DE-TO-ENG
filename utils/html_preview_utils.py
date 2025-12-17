def book_page(image_base64, translated_text):
    return f"""
    <div style="max-width:900px;margin:auto;padding:30px;
                background:#f7f7f7;border-radius:12px;">
        <img src="data:image/png;base64,{image_base64}" style="width:100%;" />
        <hr/>
        <div style="font-family:Georgia;font-size:18px;line-height:1.7;">
            {translated_text.replace(chr(10), "<br>")}
        </div>
    </div>
    """
