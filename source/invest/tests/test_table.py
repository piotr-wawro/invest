import unittest

from invest.utilities.table import col_width, print_header, print_name, print_row, print_sep, print_table


class TestTable(unittest.TestCase):

    data = [
        ["a", "bcde", "fg", "hijklmn",],
        ["12", "1", "12345", "1234567",],
    ]

    def test_col_width(self):
        expected = [4, 6, 7, 9]
        result = col_width(self.data)
        self.assertListEqual(expected, result)

    def test_print_sep(self):
        expected = '+-----------------------------+\n'
        result = print_sep(self.data[0], [4, 6, 7, 9])
        self.assertEqual(expected, result)

    def test_print_row(self):
        expected = '| a  | bcde |   fg  | hijklmn |\n'
        result = print_row(self.data[0], [4, 6, 7, 9], 'c')
        self.assertEqual(expected, result)

        expected = '| a  | bcde | fg    | hijklmn |\n'
        result = print_row(self.data[0], [4, 6, 7, 9], 'l')
        self.assertEqual(expected, result)

        expected = '|  a | bcde |    fg | hijklmn |\n'
        result = print_row(self.data[0], [4, 6, 7, 9], 'r')
        self.assertEqual(expected, result)

    def test_print_header(self):
        expected =  '+-----------------------------+\n'
        expected += '| a  | bcde |   fg  | hijklmn |\n'
        result = print_header(self.data[0], [4, 6, 7, 9])
        self.assertEqual(expected, result)

    def test_print_name(self):
        expected =  '+-----------------------------+\n'
        expected += '|          table name         |\n'
        result = print_name(self.data[0], [4, 6, 7, 9], 'table name')
        self.assertEqual(expected, result)

    def test_print_table(self):
        expected =  '+-----------------------------+\n'
        expected += '|          table name         |\n'
        expected += '+-----------------------------+\n'
        expected += '| a  | bcde |   fg  | hijklmn |\n'
        expected += '+-----------------------------+\n'
        expected += '| 12 | 1    | 12345 | 1234567 |\n'
        expected += '+-----------------------------+\n'
        result = print_table(self.data, 'table name')
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
