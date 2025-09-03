from loguru import logger

from zippy.io import append_text, read_file, write_header
from zippy.tree import build_huffman_tree


def _calculate_character_frequencies(text: str) -> dict:
    character_frequency_table = {}

    for character in text:
        if character in character_frequency_table:
            character_frequency_table[character] += 1
        else:
            character_frequency_table[character] = 1

    return character_frequency_table


def _build_prefix_codes(tree, prefix="", mapping={}):
    if tree.char:
        mapping[tree.char] = prefix
    else:
        # branch to left
        _build_prefix_codes(tree=tree.left, prefix=prefix + "0", mapping=mapping)
        # branch to right
        _build_prefix_codes(tree=tree.right, prefix=prefix + "1", mapping=mapping)

    return mapping


def _encode_text(text, mapping):
    bitstring = text.translate(str.maketrans(mapping))

    padding = (8 - len(bitstring) % 8) % 8
    bitstring += "0" * padding

    encoded_text = int(bitstring, 2).to_bytes(len(bitstring) // 8, byteorder="big")

    return encoded_text


def compress(read_path, write_path=None):
    if write_path is None:
        write_path = read_path + ".zippy"

    logger.info("Reading the text file...")
    text = read_file(read_path)

    logger.info("Calculating character frequencies...")
    character_frequency_table = _calculate_character_frequencies(text=text)

    logger.info("Building the Huffman tree...")
    tree = build_huffman_tree(character_frequency_table=character_frequency_table)

    logger.info("Building the prefix codes...")
    mapping = _build_prefix_codes(tree=tree)

    logger.info("Encoding the text...")
    encoded_text = _encode_text(text=text, mapping=mapping)

    logger.info("Writing prefix code header...")
    write_header(path=write_path, header=str(mapping))

    logger.info("Writing encoded text...")
    append_text(path=write_path, text=encoded_text)

    logger.info("Compression is complete.")


def decompress(read_path, write_path=None):
    pass
