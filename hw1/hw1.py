import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

def simulate(start_date, end_date, symbols, allocation):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(start_date, end_date, dt_timeofday)
    db =  da.DataAccess('Yahoo')
    keys = ['close']
    data = db.get_data(ldt_timestamps, symbols, keys)

    daily_value = data[0].values
    normalized_value = daily_value / daily_value[0, :]
    daily_sum = np.dot(normalized_value, allocation)
    daily_return = daily_sum.copy()
    tsu.returnize0(daily_return)
    stdev = np.std(daily_return)
    avg = np.average(daily_return)
    sharp_ratio = np.sqrt(252) * avg / stdev

    cum = 1
    for val in daily_return[1:]:
        cum = cum * (1 + val)
    return (stdev, avg, sharp_ratio, cum)

def best_ratio(start_date, end_date, symbols):
    alloc = [None] * len(symbols)
    best_alloc = [None] * len(symbols)
    best = [0.0]

    def prob(idx, alloc, left):
        if idx == len(symbols):
            if left == 0:
                r = simulate(start_date, end_date, symbols, [v / 10.0 for v in alloc])
                cur = r[2]
                if cur > best[0]:
                    best[0] = cur
                    best_alloc[:] = alloc[:]
            return

        for cur_ratio in range(0, left + 1):
            alloc[idx] = cur_ratio
            prob(idx + 1, alloc, left - cur_ratio)

    prob(0, alloc, 10)

    return best_alloc, best[0]


if __name__ == "__main__":
    print "Hello, QSTK"
    # symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
    # dt_start = dt.datetime(2011, 1, 1)
    # dt_end = dt.datetime(2011, 12, 31)
    # allocations = [0.4, 0.4, 0.0, 0.2]
    # print best_ratio(dt_start, dt_end, symbols)
    # print simulate(dt_start, dt_end, symbols, allocations)

    dt_start = dt.datetime(2011, 1, 1)
    dt_end = dt.datetime(2011, 12, 31)
    symbols = ['BRCM', 'ADBE', 'AMD', 'ADI']
    print best_ratio(dt_start, dt_end, symbols)

    # dt_start = dt.datetime(2011, 1, 1)
    # dt_end = dt.datetime(2011, 12, 31)
    # symbols = ['C', 'GS', 'IBM', 'HNZ']
    # print best_ratio(dt_start, dt_end, symbols)
