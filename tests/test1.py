import unittest
from main import hi


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(hi(), "Hi")


if __name__ == '__main__':
    unittest.main()
