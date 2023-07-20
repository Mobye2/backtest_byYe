from Module import basic
from Module import backtest_Chat
from strategies import basic_strategy
import config


def main():
    filename = '3037_欣興.csv'
    data = basic.getData(config.Datapath, 'price_record', filename)
    # print (data)

    backtest = backtest_Chat.Backtest(initial_capital=1000000)

    for index, row in data.iloc[4:].iterrows():
        strategy_combination = [basic_strategy.Cross(data, index, "5MA", "20MA",  5), basic_strategy.volume_explode(data, index, 2)]

        if all(strategy_combination):
            # print (row['date'],data.at[index-1,"close"])
            backtest.execute_trade(row['date'], row['stock_id'], 'BUY', 1000, data.at[index+1, "open"])
        if basic_strategy.Cross(data, index, "20MA", "5MA",  5):
            position = backtest.positions
            if not position:
                continue
            while (position[row['stock_id']] > 0):
                backtest.execute_trade(row['date'], row['stock_id'], 'SELL', 1000, data.at[index+1, "open"])

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
