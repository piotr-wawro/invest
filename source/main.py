from datetime import date

from invest.utilities.report import create_report


report = print(create_report('data/consumer_price_index_pl.csv', 'data/wallet.json', date(2022,7,1)))
print(report)