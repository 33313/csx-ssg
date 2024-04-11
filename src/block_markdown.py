from enum import Enum
import re


def markdown_to_blocks(md):
    rx = r"\n{2,}"
    res = re.split(rx, md)
    for x in res:
        x = x.strip()
    return res


BlockType = Enum(
    "BlockType",
    ["HEADING", "CODE", "QUOTE", "UNORDERED_LIST", "ORDERED_LIST", "PARAGRAPH"],
)


def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    elif is_code(block):
        return BlockType.CODE
    elif is_quote(block):
        return BlockType.QUOTE
    elif is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


# Helper functions
def is_heading(block):
    return re.search(r"^#{1,6} ", block) is not None


def is_code(block):
    return re.search(r"^`{3}.*`{3}$", block) is not None


def is_quote(block):
    lines = block.split("\n")
    for line in lines:
        if re.search(r"^>", line) is None:
            return False
    return True


def is_unordered_list(block):
    lines = block.split("\n")
    for line in lines:
        if re.search(r"^(\*|\-)", line) is None:
            return False
    return True


def is_ordered_list(block):
    lines = block.split("\n")
    last = 0
    for line in lines:
        search = re.search(r"^[0-9]+\.", line)
        if search is None:
            return False
        num = int(search.group()[:-1])
        if last == 0 and num != 1:
            return False
        elif num != last + 1:
            return False
        else:
            last = num
    return True
