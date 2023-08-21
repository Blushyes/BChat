import os

from config import log
from core.comments import Comment

SIMPLE_MARKED_FILENAME = 'markedfile'
SIMPLE_MARKED_SPLIT = '-'


def mark(comment_list: list[Comment]):
    if len(comment_list) == 0:
        return
    with open(SIMPLE_MARKED_FILENAME, 'a') as f:
        for cmt in comment_list:
            f.write(f'{cmt.bv}{SIMPLE_MARKED_SPLIT}{cmt.id}\n')


def marked_set():
    marked = set()
    if os.path.exists(SIMPLE_MARKED_FILENAME):
        with open(SIMPLE_MARKED_FILENAME, 'r') as f:
            for line in f:
                line = line.strip()
                log.debug(f'line {line}')
                if SIMPLE_MARKED_SPLIT not in line:
                    continue
                marked_bv, marked_id = line.split(SIMPLE_MARKED_SPLIT)
                marked.add((marked_bv, int(marked_id)))
    else:
        with open(SIMPLE_MARKED_FILENAME, 'w') as f:
            f.write('')
    return marked
