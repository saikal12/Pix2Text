# coding: utf-8

import requests
import os

def main():
    url = 'http://0.0.0.0:8503/pix2text'

    #image_fp = 'docs/examples/page2.png'
    #image_fp = 'docs/examples/en1.jpg'
    #image_fp = 'docs/examples/mixed.jpg'
    #image_fp = 'docs/examples/math-formula-42.png'
    #image_fp = 'docs/examples/english.jpg'
    #image_fp = 'docs/examples/test-doc.pdf'
    image_fp = 'docs/examples/mathpage.jpg'
    data = {
        "file_type": "page",
        "language": "ru",
        "resized_shape": 768,
        "embed_sep": " $,$ ",
        "isolated_sep": "$$\n, \n$$"
    }
    files = {
        "image": (image_fp, open(image_fp, 'rb'), 'image/jpeg')
    }

    r = requests.post(url, data=data, files=files)

    outs = r.json()['results']
    out_md_dir = r.json()['output_dir']
    if isinstance(outs, str):
        only_text = outs
    else:
        only_text = '\n'.join([out['text'] for out in outs])

    image_name = os.path.splitext(os.path.basename(image_fp))[0]
    md_file_name = f"{image_name}.md"
    md_file_path = os.path.join(out_md_dir, md_file_name)
    with open(md_file_path, 'w') as md_file:
        md_file.write(only_text)

    print(f'Text saved to {md_file_path}')
    print(f'{only_text=}')
    print(f'{out_md_dir=}')



if __name__ == '__main__':
    main()
