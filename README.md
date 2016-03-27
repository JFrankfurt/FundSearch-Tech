# Graduation Job Hunt - Tech Funds
A python script to provide a ranking of hedge funds and asset management groups based on holdings of given sectors, stocks, and returns over a benchmark.

### Todo:
1. Automate ticker gathering by sector
2. Implement average return benchmarking

### Usage:
```
'''company list'''
tickerList = ['pstg', 'infn', 'pacb-2', 'vbay', 'xlrn-2', 'ptla-2', 'rkus']

'''geographic constraints'''
statesList = ['CA', 'MA', 'CT', 'NY', 'IL', 'TX']

'''% holding collar'''
percentLow = 1.5
percentHigh = 70

'''instantiate class with list'''
x = FundHunt(tickerList)

'''get info on those companies within constraints'''
y = x.getInfo(percentHigh, percentLow, statesList)

'''export to csv for easy navigation'''
x.exportToCSV(y)
```
