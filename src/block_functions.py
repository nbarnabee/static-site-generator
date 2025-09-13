import re
from enum import Enum, unique

@unique
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OL = "ordered_list"
    UL = "unordered_list"


def markdown_to_blocks(markdown):
    return [ block.strip() for block in markdown.split("\n\n") if block.strip() ]


def block_to_block_type(block):
    if re.match(r"^(#{1,6})\s+.+$", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = [ line.strip() for line in block.split("\n") if line.strip()]
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UL
    if is_it_ol(lines):
        return BlockType.OL
    return BlockType.PARAGRAPH

def is_it_ol(lines):
    for i, line in enumerate(lines, start=1):
        if not re.match(rf"^{i}\. .+$", line):
            return False
    return True