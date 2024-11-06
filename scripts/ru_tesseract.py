import pytesseract
import requests
import json
import re
import os


def extract_text_with_tesseract(image_fp):
    config = '--psm 6 -l rus'
    russian_text = pytesseract.image_to_string(image_fp, config=config)
    return russian_text


def process_image_with_pix2text(image_fp):
    url = 'http://0.0.0.0:8503/pix2text'
    files = {
        "image": (image_fp, open(image_fp, 'rb'), 'image/jpeg')
    }
    data = {
        "file_type": "page",
        "language": "ru",
        "resized_shape": 768,
        "embed_sep": " $,$ ",
        "isolated_sep": "$$\n, \n$$"
    }

    response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"Ошибка: {response.status_code}")
        return []


def replace_text_in_pix2text(p2t_text, tesseract_text):
    """
    Заменяет обычный текст в p2t_text на текст из Tesseract (tesseract_text),
    оставляя формулы и другие элементы.
    """

    # Разделяем текст из Pix2Text на части (формулы и обычный текст)
    parts = re.split(r'(\$\$.*?\$\$|\$.*?\$)', p2t_text)

    # Индекс для замены обычного текста (не формул)
    tesseract_text_parts = tesseract_text.split("\n")
    updated_text = []
    text_idx = 0

    for part in parts:
        if part.startswith("$$") and part.endswith("$$"):
            # Это формула, оставляем её как есть
            updated_text.append(part)
        elif part.startswith("$") and part.endswith("$"):
            # Это формула, оставляем её как есть
            updated_text.append(part)
        else:
            # Это обычный текст, заменяем на текст из Tesseract
            if text_idx < len(tesseract_text_parts):
                updated_text.append(tesseract_text_parts[text_idx])
                text_idx += 1
            else:
                updated_text.append(part)

    return "\n".join(updated_text)


def main():

    image_fp = 'docs/examples/mathpage.jpg'

    russian_text = extract_text_with_tesseract(image_fp)
    #print("Извлеченный текст:", russian_text)

    formulas = process_image_with_pix2text(image_fp)
    combined_text = replace_text_in_pix2text(formulas, russian_text)
    image_name = os.path.splitext(os.path.basename(image_fp))[0]
    md_file_name = f"{image_name}.md"
    md_file_path = os.path.join("output", md_file_name)
    os.makedirs("output2", exist_ok=True)

    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(combined_text)

    print(f"Результат сохранен в {md_file_path}")
    print("Итоговый текст с формулами:\n", combined_text)


if __name__ == '__main__':
    main()
