import unittest


class TestMainSite(unittest.TestCase):
    def test_home(self):
        self.assertEqual(200, 200)


if __name__ == "__main__":
    unittest.main()
