import pytesseract
import requests
import json
import re
import os


def extract_text_with_tesseract(image_fp):
    config = '--psm 6 -l rus'
    russian_text = pytesseract.image_to_string(image_fp, config=config)
    return russian_text


def process_text_with_pix2text():
    url = 'http://0.0.0.0:8503/pix2text'
    data = {
        "file_type": "page",
        "language": "ru",
        "resized_shape": 768,
        "embed_sep": " $,$ ",
        "isolated_sep": "$$\n, \n$$"
    }

    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        return response.json().get('results', [])

    else:
        print(f"Ошибка: {response.status_code}")
        return []


def replace_formulas_in_text(text, formulas):

    embed_sep = re.compile(r"\$,\$")
    isolated_sep = re.compile(r"\$\$\n,\n\$\$")

    replaced_text = embed_sep.sub(lambda _: f"{formulas.pop(0)['text']}" if formulas else '', text)
    replaced_text = isolated_sep.sub(lambda _: f"{formulas.pop(0)['text']}" if formulas else '', replaced_text)

    return replaced_text

def main():
    #image_fp = 'docs/examples/page2.png'
    #image_fp = 'docs/examples/en1.jpg'
    #image_fp = 'docs/examples/mixed.jpg'
    #image_fp = 'docs/examples/math-formula-42.png'
    #image_fp = 'docs/examples/english.jpg'
    #image_fp = 'docs/examples/test-doc.pdf'

    image_fp = 'docs/examples/mathpage.jpg'

    russian_text = extract_text_with_tesseract(image_fp)
    print("Извлеченный текст:", russian_text)

    formulas = process_text_with_pix2text()

    combined_text = f"{russian_text}\n\nФормулы:\n" + '\n'.join([f['text'] for f in formulas])
    image_name = os.path.splitext(os.path.basename(image_fp))[0]
    md_file_name = f"{image_name}.md"
    md_file_path = os.path.join("output", md_file_name)
    os.makedirs("output", exist_ok=True)

    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(combined_text)

    print(f"Результат сохранен в {md_file_path}")
    print("Итоговый текст с формулами:\n", combined_text)


if __name__ == '__main__':
    main()
