import unittest
import hosts


class TestHosts(unittest.TestCase):
    def test_access_deny(self):
        h = hosts.deny_access_to_site('google.com')

        self.assertTrue(h)

    def test_allow_access(self):
        h = hosts.allow_access_to_site('google.com')

        self.assertTrue(h)

if __name__ == '__main__':
    unittest.main()