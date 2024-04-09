import re

def markdown_to_blocks(md):
    rx = r"\n{2,}"
    res = re.split(rx, md)
    for x in res:
        x = x.strip()
    return res
