import os
from fetcher import fetch_stock_data
from reporter import generate_report


def prompt_ticker(label: str) -> str:
    return input(f"{label}: ").strip().upper()


def main():
    print("=== Stock Analysis Tool ===\n")

    while True:
        mode = input("Type 1 for a single stock report, type 2 for a comparison: ").strip()
        if mode in ("1", "2"):
            break
        print("Invalid input. Please type 1 or 2.\n")

    print()

    try:
        if mode == "1":
            ticker = prompt_ticker("Enter ticker symbol")
            print(f"\nFetching data for {ticker}...")
            stock = fetch_stock_data(ticker)
            output_path = "report.html"
            generate_report(stock, output_path=output_path)
        else:
            ticker1 = prompt_ticker("Enter first ticker symbol ")
            ticker2 = prompt_ticker("Enter second ticker symbol")
            print(f"\nFetching data for {ticker1} and {ticker2}...")
            s1 = fetch_stock_data(ticker1)
            s2 = fetch_stock_data(ticker2)
            output_path = "report.html"
            generate_report(s1, s2, output_path=output_path)
    except ValueError as e:
        print(f"\nError: {e}")
        return

    print(f"\nReport saved to: {os.path.abspath(output_path)}")
    print("Open that file in your browser to view the report.")


if __name__ == "__main__":
    main()
