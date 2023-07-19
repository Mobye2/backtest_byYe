from Module import basic
from Module import backtest_Chat
from strategies import basic_strategy
import config


def main():
    filename='3037_欣興.csv'
    data=basic.getData(config.Datapath,'price_record',filename)
    # print (data)

    backtest = backtest_Chat.Backtest(initial_capital=1000000)

    for index,row in data.iloc[4:].iterrows():
        if basic_strategy.Cross("5MA","20MA",data,index,5):
            # print (row['date'],data.at[index-1,"close"])
            backtest.execute_trade(row['date'], row['stock_id'], 'BUY', 1000, data.at[index+1,"open"])
        if basic_strategy.Cross("20MA","5MA",data,index,5):
            position = backtest.positions
            while (position[row['stock_id']]>0):
                backtest.execute_trade(row['date'], row['stock_id'], 'SELL', 1000, data.at[index+1,"open"])

    portfolio_value = backtest.get_portfolio_value()
    positions = backtest.get_positions()
    trades = backtest.get_trades()
    backtest.calculate_win_rate()

    # 列印回測結果
    print("Portfolio Value:", portfolio_value)
    print("Positions:", positions)
    print("Trades:")
    print(trades)

if __name__ == '__main__':
    main()