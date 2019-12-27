from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt


# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
        ('printlog', False),
    )
    def log(self, txt, dt=None, doprint=False):
        ''' Logging function for this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)
#         bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
#         bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
#                                             subplot=True)
#         bt.indicators.StochasticSlow(self.datas[0])
#         bt.indicators.MACDHisto(self.datas[0])
#         rsi = bt.indicators.RSI(self.datas[0])
#         bt.indicators.SmoothedMovingAverage(rsi, period=10)
#         bt.indicators.ATR(self.datas[0], plot=False)

    def next(self):
#         print('------------------------------------------------')
#         self.log('Close: %.2f' % self.dataclose[0])
#         print("SMA: " , self.sma[0])
#         print("POS", self.position)
#         if self.position:
#             print("lne is :" , len(self), self.bar_executed)

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                '''BUY SIGNAL'''
#                 self.log("Buy Signal: %.2f" % self.dataclose[0])
                self.order = self.buy()
        else :
            if self.dataclose[0] < self.sma[0]:
#                 self.log("SELL Signal: %.2f" % self.dataclose[0])
                self.order = self.sell()
        
            
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status is order.Completed:
            if order.isbuy():
                pass
#                 print("***BUY EXECUTED")
#                 self.log(
#                     'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
#                     (order.executed.price,
#                      order.executed.value,
#                      order.executed.comm))
            else:
                pass
#                 print("!!!SELL EXECUTED")
#                 self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
#                          (order.executed.price,
#                           order.executed.value,
#                           order.executed.comm))
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            pass
#             self.log('Order Canceled/Margin/Rejected')
        self.order = None
        
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

#         self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
#                  (trade.pnl, trade.pnlcomm))
        
    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)
        
if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
#     cerebro.optstrategy(TestStrategy, maperiod=range(10, 31))
    cerebro.optstrategy(TestStrategy, maperiod=range(10,31))
    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../../../as.csv')
    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2017, 1, 1),
        # Do not pass values before this date
        todate=datetime.datetime(2018, 1, 1),
        # Do not pass values after this date
        reverse=False,
        adjvolume=False,
        adjclose=False,
        r=False
    )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    
#     cerebro.addsizer(bt.sizers.FixedSize, stake=2)
#     print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()
#     %matplotlib inline
#     cerebro.plot()
#     print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())