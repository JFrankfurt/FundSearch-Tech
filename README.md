# Graduation Job Hunt - Tech Focused  Funds
A python script that outputs a csv of institutional holders of a given list of securities, how many of the list securities those institutions hold, and the cumulative percentage of the institution's portfolio those securities make up.

### Potential Improvements:
1. Automate ticker gathering (by sector - Reuters?)
2. Implement average return benchmarking
3. Use matplotlib to skip the CSV and provide direct graphical feedback
4. Rewrite asynchronously (takes ages to run right now)

### Usage:
```
'''company list'''
tickerList = ['pstg', 'infn', 'crm', 'vbay', 'sq', 'team', 'rkus']

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
