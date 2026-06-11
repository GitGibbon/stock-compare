import os
from fetcher import fetch_stock_data
from reporter import generate_report


def main():
    print("=== Stock Comparison Tool ===\n")
    ticker1 = input("Enter first ticker symbol:  ").strip().upper()
    ticker2 = input("Enter second ticker symbol: ").strip().upper()

    print(f"\nFetching data for {ticker1} and {ticker2}...")

    try:
        s1 = fetch_stock_data(ticker1)
        s2 = fetch_stock_data(ticker2)
    except ValueError as e:
        print(f"\nError: {e}")
        return

    output_path = "report.html"
    generate_report(s1, s2, output_path)

    abs_path = os.path.abspath(output_path)
    print(f"\nReport saved to: {abs_path}")
    print("Open that file in your browser to view the comparison.")


if __name__ == "__main__":
    main()
