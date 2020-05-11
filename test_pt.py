import unittest
import coverage
import pt.libs.utils as utils
import os
import subprocess

#
# cov = coverage.coverage(branch=True)
# cov.start()


class TestPt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shell(self):
        TEST_ENV = "TEST_ENV_VALUE"
        r = utils.shell_exec_result("export", TEST_ENV=TEST_ENV)
        self.assertTrue(str(r).find(TEST_ENV) > 0)


if __name__ == '__main__':
    unittest.main()
