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
    blocks = []
    for block in markdown.split("\n\n"):
        md_block = block.strip()
        if len(md_block):
            blocks.append(md_block)

    return blocks

def block_to_block_type(block):
    # If it's a header or a code block, we don't need to worry about breaking it by lines
    if re.match(r"#{1,6}\s\S", block):
        return BlockType.HEADING
    if block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    # The other types must be evaluated on a line-by-line basis
    lines = split_block_to_lines(block)
    if is_it_quote(lines):
        return BlockType.QUOTE
    if is_it_ul(lines):
        return BlockType.UL
    if is_it_ol(lines):
        return BlockType.OL

    # and if all else fails
    return BlockType.PARAGRAPH


def split_block_to_lines(block):
    lines = []
    for line in block.split("\n"):
        new_line = line.strip()
        if len(line):
            lines.append(new_line)

    return lines


def is_it_quote(lines):
    for line in lines:
        if line[0] != ">":
            return False
    return True

def is_it_ul(lines):
    for line in lines:
        if line[0:2] != "- ":
            return False
    return True

def is_it_ol(lines):
    for i in range(0, len(lines)):
        if lines[i][0:3] != str(i+1) + ". ":
            return False
    return True