from datetime import date
from math import nan
import unittest

from invest.utilities.cpi import CPI


class TestCPI(unittest.TestCase):

    def test_read_csv(self):
        expected = [
            [2001.0,100.8,100.1,100.5,100.8,101.1,99.9,99.7,99.7,100.3,100.4,100.1,100.2],
            [2000.0,101.8,100.9,nan,100.4,100.7,nan,100.7,99.7,nan,100.8,100.4,100.2]
        ]
        result = CPI._read_csv('./invest/tests/data/test_cpi_1.csv')
        self.assertListEqual(expected, result)

    def test_get_end(self):
        expected = date(2008,12,1)
        result = CPI._get_end([
            [2008.0,100.7,100.4,100.4,100.4,100.8,100.2,100.0,99.6,100.3,100.4,100.2,99.9],
            [2004.0,100.4,100.1,100.3,100.8,101.0,100.9,99.9,99.6,100.3,100.6,100.3,100.1]
        ])
        self.assertEqual(expected, result)

        expected = date(2004,11,1)
        result = CPI._get_end([[2004.0,100.4,100.1,100.3,100.8,101.0,100.9,99.9,99.6,100.3,100.6,100.3,nan]])
        self.assertEqual(expected, result)

        expected = date(2004,9,1)
        result = CPI._get_end([[2004.0,100.8,101.0,100.9,99.9,99.6,100.3,100.6,100.3,100.1,nan,nan,nan]])
        self.assertEqual(expected, result)

        expected = date(2004,1,1)
        result = CPI._get_end([[2004.0,100.1,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan]])
        self.assertEqual(expected, result)

    def test_get_start(self):
        expected = date(2004,1,1)
        result = CPI._get_start([
            [2008.0,100.7,100.4,100.4,100.4,100.8,100.2,100.0,99.6,100.3,100.4,100.2,99.9],
            [2004.0,100.4,100.1,100.3,100.8,101.0,100.9,99.9,99.6,100.3,100.6,100.3,100.1]
        ])
        self.assertEqual(expected, result)

        expected = date(2004,2,1)
        result = CPI._get_start([[2004.0,nan,100.1,100.3,100.8,101.0,100.9,99.9,99.6,100.3,100.6,100.3,100.1]])
        self.assertEqual(expected, result)

        expected = date(2004,4,1)
        result = CPI._get_start([[2004.0,nan,nan,nan,100.8,101.0,100.9,99.9,99.6,100.3,100.6,100.3,100.1]])
        self.assertEqual(expected, result)

        expected = date(2004,12,1)
        result = CPI._get_start([[2004.0,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,100.1]])
        self.assertEqual(expected, result)

    def test_get_cpi(self):
        expected = [1.001,1.007,1.004,1.004,1.004,1.008,1.002,1.000,0.996,1.003,1.004,1.002,0.999]
        result = CPI._get_cpi([
            [2008,100.7,100.4,100.4,100.4,100.8,100.2,100.0,99.6,100.3,100.4,100.2,99.9],
            [2004,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,100.1]
        ])
        for exp, res in zip(expected, result):
            self.assertAlmostEqual(exp, res)

    def test_date_to_idx(self):
        cpi = CPI('./invest/tests/data/test_cpi_2.csv')
        expected = 30
        result = cpi._date_to_idx(date(2002,7,1))
        self.assertEqual(expected, result)

    def test_cumulative_inflation(self):
        cpi = CPI('./invest/tests/data/test_cpi_2.csv')

        # Linear increment of cpi
        expected = 1+(1.011-1)*0/31
        result = cpi.cumulative_inflation(date(2001,5,1), date(2001,5,1))
        self.assertAlmostEqual(expected, result)

        expected = 1+(1.011-1)*4/31
        result = cpi.cumulative_inflation(date(2001,5,16), date(2001,5,20))
        self.assertAlmostEqual(expected, result)

        expected = 1+(1.011-1)*30/31
        result = cpi.cumulative_inflation(date(2001,5,1), date(2001,5,31))
        self.assertAlmostEqual(expected, result)

        expected = 1+(1.011-1)*31/31
        result = cpi.cumulative_inflation(date(2001,5,1), date(2001,6,1))
        self.assertAlmostEqual(expected, result)

        expected = 1+(0.995-1)*3/31
        result = cpi.cumulative_inflation(date(2002,7,22), date(2002,7,25))
        self.assertAlmostEqual(expected, result)

        # Multiple months same year
        expected = 1.008*1.007*0.997*1.010*1.008*1.004
        result = cpi.cumulative_inflation(date(2000,6,1), date(2000,12,1))
        self.assertAlmostEqual(expected, result)

        expected = (1+(1.008-1)*21/30)*1.007*0.997*1.010*1.008*1.004
        result = cpi.cumulative_inflation(date(2000,6,10), date(2000,12,1))
        self.assertAlmostEqual(expected, result)

        expected = 1.008*1.007*0.997*1.010*1.008*(1+(1.004-1)*24/30)
        result = cpi.cumulative_inflation(date(2000,6,1), date(2000,11,25))
        self.assertAlmostEqual(expected, result)

        expected = (1+(1.008-1)*16/30)*1.007*0.997*1.010*1.008*(1+(1.004-1)*19/30)
        result = cpi.cumulative_inflation(date(2000,6,15), date(2000,11,20))
        self.assertAlmostEqual(expected, result)

        # Multiple months different years
        expected = 1.008*1.007*0.997*1.010*1.008*1.004*1.002*1.008*1.001*1.005*1.008
        result = cpi.cumulative_inflation(date(2000,6,1), date(2001,5,1))
        self.assertAlmostEqual(expected, result)

        expected = (1+(1.008-1)*17/30)*1.007*0.997*1.010*1.008*1.004*1.002*1.008*1.001*1.005*(1+(1.008-1)*21/30)
        result = cpi.cumulative_inflation(date(2000,6,14), date(2001,4,22))
        self.assertAlmostEqual(expected, result)

        # Only one date
        expected = 1+(1.008-1)*22/31
        result = cpi.cumulative_inflation(start_date=date(2001,1,10))
        self.assertAlmostEqual(expected, result)

        expected = 1+(1.008-1)*9/31
        result = cpi.cumulative_inflation(end_date=date(2001,1,10))
        self.assertAlmostEqual(expected, result)

    def test_inflation(self):
        cpi = CPI('./invest/tests/data/test_cpi_2.csv')
        expected = 0.995
        result = cpi.inflation(date(2002,7,3))
        self.assertAlmostEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
