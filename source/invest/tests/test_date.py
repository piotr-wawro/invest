from datetime import date
import unittest

from invest.utilities.date import first_day_of_months, fraction_of_month, is_same_month, last_day_of_months, months_between


class TestDate(unittest.TestCase):

    def test_months_between(self):
        expected = 9
        result = months_between(date(2000,1,1), date(2000,10,1))
        self.assertEqual(expected, result)

    def test_is_same_month(self):
        expected = True
        result = is_same_month(date(2000,5,17), date(2000,5,12))
        self.assertEqual(expected, result)

        expected = False
        result = is_same_month(date(2000,5,17), date(2000,6,12))
        self.assertEqual(expected, result)

        expected = False
        result = is_same_month(date(2000,5,17), date(2001,5,12))
        self.assertEqual(expected, result)

    def test_fraction_of_month(self):
        expected = 15/31
        result = fraction_of_month(start_date=date(2000,5,17))
        self.assertEqual(expected, result)

        expected = 15/31
        result = fraction_of_month(end_date=date(2000,5,16))
        self.assertEqual(expected, result)

        expected = 6/31
        result = fraction_of_month(start_date=date(2000,5,16), end_date=date(2000,5,22))
        self.assertEqual(expected, result)

        expected = 0/31
        result = fraction_of_month(start_date=date(2000,5,16), end_date=date(2000,5,16))
        self.assertEqual(expected, result)

        with self.assertRaises(Exception):
            result = fraction_of_month(start_date=date(2000,5,16), end_date=date(2000,6,22))

        with self.assertRaises(Exception):
            result = fraction_of_month()

        with self.assertRaises(Exception):
            result = fraction_of_month(start_date=date(2000,5,22), end_date=date(2000,5,16))

    def test_last_day_of_months(self):
        expected = [date(2000,2,29)]
        result = last_day_of_months(date(2000,2,15), date(2000,2,20))
        self.assertListEqual(expected, result)

        expected = [date(2000,1,31), date(2000,2,29), date(2000,3,31), date(2000,4,30)]
        result = last_day_of_months(date(2000,1,15), date(2000,4,15))
        self.assertListEqual(expected, result)

        expected = [date(2001,1,31), date(2001,2,28), date(2001,3,31), date(2001,4,30)]
        result = last_day_of_months(date(2001,1,15), date(2001,4,15))
        self.assertListEqual(expected, result)

        with self.assertRaises(Exception):
            result = fraction_of_month(date(2000,4,15), date(2000,1,15))

    def test_first_day_of_months(self):
        expected = []
        result = first_day_of_months(date(2000,2,15), date(2000,2,20))
        self.assertListEqual(expected, result)

        expected = [date(2000,2,1), date(2000,3,1), date(2000,4,1)]
        result = first_day_of_months(date(2000,1,15), date(2000,4,15))
        self.assertListEqual(expected, result)

        with self.assertRaises(Exception):
            result = first_day_of_months(date(2000,4,15), date(2000,1,15))

if __name__ == '__main__':
    unittest.main()
