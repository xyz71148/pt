import json
import unittest
import coverage

cov = coverage.coverage(branch=True)
cov.start()


class TestPt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_connect(self):
        self.assertFalse(False)


if __name__ == '__main__':
    unittest.main()
