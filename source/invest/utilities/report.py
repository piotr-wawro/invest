from datetime import date

from invest.utilities.cpi import CPI
from invest.datamodel.wallet import Investment, Wallet
from invest.utilities.date import Flag, first_day_of_months
from invest.utilities.table import print_table

def create_report(cpi_path: str, wallet_path: str, date: date) -> str:
    cpi = CPI('data/consumer_price_index_pl.csv')
    wallet = Wallet('data/wallet.json')

    header = [
        ['Asset name', 'Investment cost', 'Expected return']
    ]

    data = []
    long_investment = wallet.investments.long
    long_assets = {x.asset for x in long_investment}
    for asset in long_assets:
        asset_inv = [x for x in long_investment if x.asset == asset]
        inv_cost = investment_cost(asset_inv)
        exp_return = expected_return(asset_inv, cpi, date, date)

        row = [asset, inv_cost, exp_return[0]]
        data.append(row)

    return print_table(header+data, 'Long Investment')

def investment_cost(inv: list[Investment]) -> float:
    return sum([x.price for x in inv if x.quantity > 0])

def expected_return(inv: list[Investment], cpi: CPI, start_date: date|None = None, end_date: date|None = None) -> list[float]:
    """Returns expected net return at the end of every month since investment start."""
    if len(inv) == 0:
        return []
    if start_date and inv[0].date > start_date:
        raise Exception("start_date is before first investment.")

    if start_date is None:
        start_date = min(inv, key=lambda x: x.date).date
    if end_date is None:
        end_date = max(inv, key=lambda x: x.date).date

    inv = sorted(inv, key=lambda x: x.date)
    inv_dates = [d.date for d in inv]
    to_save_dates = [d for d in first_day_of_months(start_date, end_date)]

    key_dates = []
    flags = []
    for d in inv_dates:
        if d in key_dates:
            key_dates.append(d)
            flags.append(Flag.INV|Flag.SKIP)
        elif d in to_save_dates:
            key_dates.append(d)
            flags.append(Flag.INV|Flag.SAVE)
        else:
            key_dates.append(d)
            flags.append(Flag.INV)
    for d in to_save_dates:
        if d not in key_dates:
            key_dates.append(d)
            flags.append(Flag.SAVE)
    flags[0] |= Flag.SKIP
    flags[0] &= ~Flag.SAVE

    key_dates = list(zip(key_dates, flags))
    key_dates = sorted(key_dates)

    def get_inv():
        for i in inv:
            yield i
    inv_gen = get_inv()

    rsl = []
    avg_price = 0
    total = 0
    prev_date = None
    expected = 0
    for d in key_dates:
        date = d[0]
        flags = d[1]

        if not flags&Flag.SKIP:
            expected *= cpi.cumulative_inflation(prev_date, date)

        if flags&Flag.SAVE:
            rsl.append(expected)

        if flags&Flag.INV:
            i = next(inv_gen)

            if i.quantity > 0:
                expected += i.price*i.quantity
                avg_price = (total*avg_price+i.price*i.quantity)/(total+i.quantity)
                total = total+i.quantity
            else:
                expected += expected*i.quantity/total
                total = total+i.quantity

        prev_date = date

    return rsl
