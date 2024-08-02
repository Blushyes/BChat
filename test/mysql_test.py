import os
import unittest

os.chdir('..')

from core.comment.utils import Comment


class MyTestCase(unittest.TestCase):
    def test_values(self):
        comment_list = [Comment('a', 1), Comment('b', 2), Comment('c', 3)]
        values = str([(f'{cmt.bv}', cmt.id) for cmt in comment_list]).lstrip('[').rstrip(']')
        print(values)

    def test_mark(self):
        from persistent.mysql import mark
        comment_list = [Comment('a', 1), Comment('b', 2), Comment('c', 3)]
        mark(comment_list)

    def test_marked_set(self):
        from persistent.mysql import marked_set
        print(marked_set())

    def test_simple_mysql(self):
        from persistent.simple import marked_set
        from persistent.mysql import mark
        marked = marked_set()
        mark([Comment(bid, cid) for bid, cid in marked])


if __name__ == '__main__':
    unittest.main()
