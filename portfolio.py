import csv
import json
from datetime import datetime
from pathlib import Path

import yfinance as yf

PORTFOLIO_FILE = "portfolio.json"
SUMMARY_FILE = "portfolio_summary.csv"


def load_portfolio():
    if Path(PORTFOLIO_FILE).exists():
        with open(PORTFOLIO_FILE, "r") as file:
            return json.load(file)
    return {}


def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, "w") as file:
        json.dump(portfolio, file, indent=4)


def add_stock(portfolio):
    symbol = input("Enter stock symbol: ").upper()
    price = float(input("Enter purchase price: "))
    quantity = int(input("Enter quantity: "))

    if symbol in portfolio:
        old = portfolio[symbol]
        total_quantity = old["quantity"] + quantity
        average_price = (
            old["price"] * old["quantity"] + price * quantity
        ) / total_quantity

        portfolio[symbol] = {
            "price": average_price,
            "quantity": total_quantity
        }
    else:
        portfolio[symbol] = {
            "price": price,
            "quantity": quantity
        }

    save_portfolio(portfolio)
    print("Stock added successfully!")


def get_current_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        price = stock.fast_info["lastPrice"]

        if price is not None:
            return float(price)

    except Exception:
        pass

    return float(input(f"Enter current price for {symbol}: "))


def calculate_performance(portfolio):
    total_investment = 0
    total_value = 0
    records = []

    for symbol, details in portfolio.items():

        buy_price = details["price"]
        quantity = details["quantity"]

        current_price = get_current_price(symbol)

        investment = buy_price * quantity
        market_value = current_price * quantity

        profit_loss = market_value - investment
        percentage = (profit_loss / investment) * 100

        total_investment += investment
        total_value += market_value

        print("\nStock:", symbol)
        print("Investment:", round(investment, 2))
        print("Current Value:", round(market_value, 2))
        print("Profit/Loss:", round(profit_loss, 2))
        print("Gain/Loss %:", round(percentage, 2), "%")

        records.append([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            quantity,
            buy_price,
            current_price,
            investment,
            market_value,
            profit_loss,
            percentage
        ])

    total_profit = total_value - total_investment

    print("\n========== PORTFOLIO SUMMARY ==========")
    print("Total Investment:", round(total_investment, 2))
    print("Current Portfolio Value:", round(total_value, 2))
    print("Total Profit/Loss:", round(total_profit, 2))

    if total_investment:
        print("Overall Gain/Loss:",
              round(total_profit / total_investment * 100, 2), "%")

    with open(SUMMARY_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if Path(SUMMARY_FILE).stat().st_size == 0:
            writer.writerow([
                "Date", "Symbol", "Quantity", "Buy Price",
                "Current Price", "Investment", "Market Value",
                "Profit/Loss", "Percentage"
            ])

        writer.writerows(records)

    print("\nData saved to portfolio_summary.csv")


def main():
    portfolio = load_portfolio()

    while True:
        print("\n===== STOCK PORTFOLIO TRACKER =====")
        print("1. Add Stock")
        print("2. View Portfolio Performance")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_stock(portfolio)

        elif choice == "2":
            if portfolio:
                calculate_performance(portfolio)
            else:
                print("Portfolio is empty!")

        elif choice == "3":
            print("Thank you for using Portfolio Tracker!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()