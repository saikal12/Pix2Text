### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:


Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```
или для пользователей Windows

```
source env/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
```
pip install pix2text

```
мне дополнительно пришлось установить(pydantic, fastapi, python-multipart, uvicorn)


Чтобы запустить сервер на порту 8503 с базовой моделью:

```

p2t serve -l en,ch_sim -H 0.0.0.0 -p 8503
```
Дальше запускаем скрипт

```
 python scripts/try_service.py
```

Этот скрипт отправляет изображение на сервер Pix2Text, чтобы извлечь из него текст, используя API.

#### в output-md-root/imgname.md
Будет храниться ответ от API запроса