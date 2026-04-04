#SUBSTITUIR CARACTERES PRESENTES NO HTML
def _escape_xml(text: str) -> str:
    escapes = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;'
    }
    for char, escaped in escapes.items():
        text = text.replace(char, escaped)
    return text


