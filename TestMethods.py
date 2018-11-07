import unittest
import work_log_with_DB
from unittest import mock


class TestMethods(unittest.TestCase):
    def test_show_menu_header(self):
        self.assertEqual(work_log_with_DB.show_menu_header("Test"), 1)

    def test_main_menu(self):
        with mock.patch('builtins.input', return_value='q'):
            self.assertTrue(work_log_with_DB.main_menu())

    def test_main_menu_q(self):
        with mock.patch('builtins.input', return_value='q'):
            self.assertTrue(work_log_with_DB.main_menu() == 'q')

    def test_run_main_menu_a(self):
        with mock.patch('builtins.input', side_effect=['a', 'bob', 'tester',
                                                       '2', 'notes good']):
            self.assertFalse(work_log_with_DB.run_main_menu())

    def test_run_main_menu_l(self):
        with mock.patch('builtins.input', side_effect=['l', 'e', 'n', 'r']):
            self.assertFalse(work_log_with_DB.run_main_menu())

    def test_display_find_menu_e(self):
        with mock.patch('builtins.input', side_effect=['e', 'bob']):
            self.assertTrue(work_log_with_DB.display_find_menu())

    def test_display_find_menu_d(self):
        with mock.patch('builtins.input', side_effect=['d', '11/1/2018']):
            self.assertTrue(work_log_with_DB.display_find_menu())

    def test_display_find_menu_t(self):
        with mock.patch('builtins.input', side_effect=['t', '2']):
            self.assertTrue(work_log_with_DB.display_find_menu())

    def test_display_find_menu_t2(self):
        with mock.patch('builtins.input', side_effect=['t', 'x']):
            self.assertTrue(work_log_with_DB.display_find_menu())

    def test_display_find_menu_s(self):
        with mock.patch('builtins.input', side_effect=['s', 'note']):
            self.assertTrue(work_log_with_DB.display_find_menu())

    def test_display_find_menu_r(self):
        with mock.patch('builtins.input', side_effect=['r']):
            self.assertTrue(work_log_with_DB.display_find_menu())

    def test_display_find_menu_x(self):
        with mock.patch('builtins.input', side_effect=['x', 'r']):
            self.assertTrue(work_log_with_DB.display_find_menu())

    def test_load_work_log_e(self):
        with mock.patch('builtins.input', side_effect=['bob']):
            self.assertTrue(work_log_with_DB.load_work_log("e"))

    def test_load_work_log_d(self):
        with mock.patch('builtins.input', side_effect=['11/1/2018']):
            self.assertFalse(
                type(work_log_with_DB.load_work_log("d"))
                == "peewee.ModelSelect")

    def test_load_work_log_d2(self):
        with mock.patch('builtins.input', side_effect=['11/1/2018 11/2/2018']):
            self.assertTrue(work_log_with_DB.load_work_log("d"))

    def test_load_work_log_d3(self):
        with mock.patch('builtins.input', side_effect=['11/1/2018 5/2/2018']):
            self.assertTrue(work_log_with_DB.load_work_log("d"))

    def test_load_work_log_d3(self):
        with mock.patch('builtins.input', side_effect=['11/1/2018 11/1/2018']):
            self.assertFalse(
                type(work_log_with_DB.load_work_log("d"))
                == "peewee.ModelSelect")

    def test_load_work_log_d4(self):
        with mock.patch('builtins.input', side_effect=['e']):
            self.assertTrue(work_log_with_DB.load_work_log("d"))

    def test_load_work_log_x(self):
        with mock.patch('builtins.input', side_effect=['x']):
            self.assertTrue(work_log_with_DB.load_work_log("x"))

    def test_load_work_log_t(self):
        with mock.patch('builtins.input', side_effect=['2']):
            self.assertTrue(work_log_with_DB.load_work_log("t"))

    def test_load_work_log_s(self):
        with mock.patch('builtins.input', side_effect=['note']):
            self.assertTrue(work_log_with_DB.load_work_log("s"))

    def test_display_entries_s(self):
        with mock.patch('builtins.input', side_effect=['n', 'r']):
            self.assertTrue(work_log_with_DB.display_entries("s"))

    def test_display_entries_s2(self):
        with mock.patch('builtins.input', side_effect=['p']):
            self.assertTrue(work_log_with_DB.display_entries("s") is None)

    def test_display_entries_s3(self):
        with mock.patch('builtins.input', side_effect=['r']):
            self.assertTrue(work_log_with_DB.display_entries("s"))

    def test_display_entries_d(self):
        with mock.patch('builtins.input', side_effect=['d']):
            self.assertFalse(work_log_with_DB.display_entries("d"))

    def test_display_entries_e(self):
        with mock.patch('builtins.input', side_effect=['5/5/2018',
                                                       'b2', '2', '2', 'e']):
            self.assertFalse(work_log_with_DB.display_entries("e"))


if __name__ == "__main__":
    unittest.main()