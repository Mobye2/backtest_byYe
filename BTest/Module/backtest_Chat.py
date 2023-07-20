import pandas as pd
import pandas as pd


class Backtest:
    def __init__(self, initial_capital):
        self.initial_capital = initial_capital
        self.portfolio_value = initial_capital
        self.positions = {}
        self.trades = pd.DataFrame(columns=['date', 'stock_id', 'order', 'volume', 'price'])
        self.win_rate = 0

    def execute_trade(self, date, symbol, order, quantity, price):
        if symbol not in self.positions:
            self.positions[symbol] = 0

        if order == 'BUY':
            self.positions[symbol] += quantity
            self.portfolio_value -= quantity * price

        elif order == 'SELL':
            if symbol not in self.positions or quantity > self.positions[symbol] or quantity == 0:
                return False  # Insufficient position to sell

            self.positions[symbol] -= quantity
            self.portfolio_value += quantity * price

        trade = pd.DataFrame([[date, symbol, order, quantity, price]], columns=['date', 'stock_id', 'order', 'volume', 'price'])
        self.trades = pd.concat([self.trades, trade], ignore_index=True)
        return True

    def get_portfolio_value(self):
        return self.portfolio_value

    def get_positions(self):
        return self.positions

    def get_stock_positions(self, symbol):
        return self.positions[symbol]

    def get_trades(self):
        return self.trades

    def calculate_win_rate(self):
        buy_trades = self.trades[self.trades['order'] == 'BUY'].reset_index(drop=True)
        buy_trades['counted'] = False
        sell_trades = self.trades[self.trades['order'] == 'SELL'].reset_index(drop=True)
        total_trades = len(buy_trades)

        if total_trades == 0:
            self.win_rate = 0
            return

        print(buy_trades)
        print(sell_trades)

        win_count = 0
        buy_index = 0
        for index, row in sell_trades.iterrows():
            profit = round(row['price']-buy_trades.at[buy_index, 'price'], 2)*1000
            if profit > 0:
                win_count += 1
            print(row['date'], 'sell at price ', row['price'], 'which buy at', buy_trades.at[buy_index, 'price'], ',profit=', profit, 'wincount=', win_count)
            buy_index += 1
        self.win_rate = round(win_count/len(sell_trades), 2)
        print('winrate=', self.win_rate*100, '%')


# # 建立回測物件
# backtest = Backtest(initial_capital=1000000)

# # 执行交易
# backtest.execute_trade('2022-01-01', 'AAPL', 'BUY', 100, 150.0)
# backtest.execute_trade('2022-01-02', 'AAPL', 'SELL', 50, 155.0)
# backtest.execute_trade('2022-01-03', 'AAPL', 'BUY', 75, 160.0)

# # 取得回測結果
# portfolio_value = backtest.get_portfolio_value()
# positions = backtest.get_positions()
# trades = backtest.get_trades()

# # 列印回測結果
# print("Portfolio Value:", portfolio_value)
# print("Positions:", positions)
# print("Trades:")
# print(trades)


if __name__ == "__main__":
    print('backtest_chat run')
