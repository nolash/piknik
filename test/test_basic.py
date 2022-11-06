import unittest

from piknik import (
        Basket,
        Issue,
        )


class TestBasic(unittest.TestCase):

    def test_init(self):
        b = Basket()
        o = Issue('The first issue')
        b.add(o)
        r = b.get(o.id)
        self.assertEqual(r, o)
        pass


if __name__ == '__main__':
    unittest.main()
