import unittest

from invest.datamodel.wallet import Asset
from invest.datamodel.wallet import Wallet
from invest.utilities.cpi import CPI
from invest.utilities.report import expected_return


class TestReport(unittest.TestCase):

    def test_expected_return(self):
        cpi = CPI('./invest/tests/data/test_cpi_3.csv')
        inv = Wallet('./invest/tests/data/test_wallet.json')

        expected = [709100.0, 1215145.5, 981837.56, 989692.26, 992661.34,
                    1394054.0, 1399630.22, 1403829.11, 1413655.91]
        result = expected_return(inv.investments.long, cpi)
        for exp, res in zip(expected, result):
            self.assertAlmostEqual(exp, res, delta=0.005)

if __name__ == '__main__':
    unittest.main()
