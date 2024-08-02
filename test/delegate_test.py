import os
import unittest

os.chdir('..')


class MyTestCase(unittest.TestCase):
    def test_mq(self):
        from persistent.delegate import send
        send('mark', {'hello': 1})

    def test_mq_mark(self):
        from persistent.delegate import mark
        from core.comment.utils import Comment
        comment_list = [Comment('a', 1), Comment('b', 2), Comment('c', 3)]
        mark(comment_list)

    def test_marked_set(self):
        from persistent.delegate import marked_set
        print(marked_set())


if __name__ == '__main__':
    unittest.main()
