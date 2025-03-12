from src.parser import parse_from_yfinance
from src.analysis import Strategy_MA, Strategy_MACD, Strategy_KD, Strategy_RSI, Strategy_SaR
from src.utils import plot_data


def main():

    # Data preprocessing (Input)
    stock = parse_from_yfinance()

    # Data preview
    #plot_data(stock)

    # Statistical Plot 
    Strategy_MA(stock)
    Strategy_MACD(stock)
    Strategy_KD(stock)
    Strategy_RSI(stock)
    Strategy_SaR(stock)

    print('----------------------End of Program------------------------')
    return


if __name__ == "__main__" :
    main()
