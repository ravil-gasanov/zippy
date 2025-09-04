import ast

from loguru import logger

from zippy.io import read_file, write_file
from zippy.tree import build_huffman_tree

HEADER_LEN_BYTES = 4
ENCODING = "utf-8"


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

    return encoded_text, padding


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
    encoded_text, padding = _encode_text(text=text, mapping=mapping)

    logger.info("Writing prefix code header...")
    header = bytes(str(mapping), encoding=ENCODING)
    header_len = int(len(header)).to_bytes(
        HEADER_LEN_BYTES,
        byteorder="big",
        signed=False,
    )
    padding = padding.to_bytes(
        HEADER_LEN_BYTES,
        byteorder="big",
        signed=False,
    )

    write_file(path=write_path, content=header_len, mode="wb")
    write_file(path=write_path, content=padding, mode="ab")
    write_file(path=write_path, content=header, mode="ab")

    logger.info("Writing encoded text...")
    write_file(path=write_path, content=encoded_text, mode="ab")

    logger.info("Compression is complete.")


# region decompress


def decompose_binary(binary):
    start, end = 0, HEADER_LEN_BYTES

    header_len = int.from_bytes(
        binary[start:end],
        byteorder="big",
        signed=False,
    )

    start = end
    end += HEADER_LEN_BYTES

    padding = int.from_bytes(
        binary[start:end],
        byteorder="big",
        signed=False,
    )

    start = end
    end += header_len
    header = binary[start:end].decode(encoding=ENCODING)
    mapping = ast.literal_eval(header)

    start = end
    content = binary[start:]

    return mapping, padding, content


def decode(mapping, padding, encoded_text):
    # inverse the mapping
    mapping = {v: k for k, v in mapping.items()}

    total_bits = len(encoded_text) * 8
    bitstring = str(bin(int.from_bytes(encoded_text, byteorder="big")))[2:]
    bitstring = bitstring.zfill(total_bits)

    if padding:
        bitstring = bitstring[:-padding]

    full_char = ""
    decoded_text = ""

    for char in bitstring:
        full_char += char

        if full_char in mapping:
            decoded_text += mapping[full_char]
            full_char = ""

    return decoded_text


def decompress(read_path, write_path=None):
    if write_path is None:
        write_path = read_path + "-decompressed.txt"

    logger.info("Reading the binary file...")
    binary = read_file(path=read_path, mode="rb")

    logger.info("Extract mapping and encoded text from the binary content...")
    mapping, padding, encoded_text = decompose_binary(binary=binary)

    logger.info("Decoding text...")
    decoded_text = decode(
        mapping=mapping,
        padding=padding,
        encoded_text=encoded_text,
    )

    logger.info("Writing decompressed text file")
    write_file(write_path, content=decoded_text)
