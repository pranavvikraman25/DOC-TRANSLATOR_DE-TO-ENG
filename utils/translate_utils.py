from deep_translator import GoogleTranslator

def translate_text(text):
    return GoogleTranslator(source="de", target="en").translate(text)
