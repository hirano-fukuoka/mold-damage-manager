import pytesseract
from pdf2image import convert_from_bytes

def parse_pdf(file):
    images = convert_from_bytes(file.read())
    text = pytesseract.image_to_string(images[0], lang="jpn")

    def extract(key):
        for line in text.splitlines():
            if key in line:
                return line.split(":")[-1].strip()
        return ""

    return {
        "usage": int(extract("使用回数").replace("回", "") or 0),
        "part": extract("損傷部位"),
        "damage": extract("損傷内容"),
        "action": extract("処置内容"),
        "result": extract("結果")
    }
