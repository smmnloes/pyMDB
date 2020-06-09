import unittest

from util.util import ordered_list_contains_number, normalize, clean_nulls


class TestUtil(unittest.TestCase):

    def test_ordered_list_contains_number(self):
        self.assertTrue(ordered_list_contains_number([0, 1, 2, 3], 2))
        self.assertTrue(ordered_list_contains_number([0, 0, 0, 0], 0))
        self.assertFalse(ordered_list_contains_number([0, 1, 2, 3], 4))
        self.assertFalse(ordered_list_contains_number([0, 1, 2, 3], -1))
        self.assertFalse(ordered_list_contains_number([], 1))

    def test_normalize(self):
        self.assertEqual(normalize("Bernd"), "bernd")
        self.assertEqual(normalize("Bèrnd"), "bernd")
        self.assertEqual(normalize("Карменсіта"), "karmensita")

    def test_clean_nulls(self):
        self.assertEqual(clean_nulls(['\\N', 'test', 'test2']), [None, 'test', 'test2'])
