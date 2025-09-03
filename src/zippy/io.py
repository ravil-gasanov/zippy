from loguru import logger


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        raise e


def write_header(path, header):
    with open(path, "w") as file:
        file.write(header)


def append_text(path, text):
    try:
        with open(path, "ab") as file:
            file.write(text)
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        raise e
