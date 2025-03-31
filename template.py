import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    'data'
    'src/__init__.py',
    'src/helper.py',
    'src/prompt.py',
    '.env',
    '.gitignore',
    'LICENCE',
    'README.md',
    'requirements.txt',
    'render.yaml',
    'setup.py',
    'template.py',
    'app.py',
    'store_index.py',
    'research/trials.ipynb'
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != '':
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(file=filepath, mode='w') as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} is already exists")

