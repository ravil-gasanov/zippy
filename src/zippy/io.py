from loguru import logger


def read_file(path, mode="r"):
    encoding = "utf-8" if mode == "r" else None
    try:
        with open(path, mode, encoding=encoding) as file:
            return file.read()
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        raise e


def write_file(path, content, mode="w"):
    encoding = "utf-8" if mode == "w" else None
    try:
        with open(path, mode, encoding=encoding) as file:
            file.write(content)
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        raise e
