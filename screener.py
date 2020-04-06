from bs4 import BeautifulSoup
import urllib.request
import os, sys
from colorama import Fore, Back, Style, init
import yfinance as yf


def yahooKeyStats(stock):
    """
        Fetch data from Yahoo Finance.

        Input :
            stock : ticker for which to look for on Yahoo
    """

    try:
        #Get the source code for the stock
        yahoo = urllib.request.urlopen('https://ca.finance.yahoo.com/quote/' + stock + '/key-statistics?p=' + stock).read()
        ticker = yf.Ticker(stock)

        #Extract the Price to Book ratio
        pbr = BeautifulSoup(yahoo.decode().split('Price/Book')[1], 'html.parser').td.text
        #pbr = ticker.info['priceToBook']
        mv50 = BeautifulSoup(yahoo.decode().split('50-Day Moving Average')[1], 'html.parser').td.text
        #mv50 = ticker.info['fiftyDayAverage']
        mv200 = BeautifulSoup(yahoo.decode().split('200-Day Moving Average')[1], 'html.parser').td.text
        #mv200 = ticker.info['twoHundredDayAverage']
        
        if (pbr != "N/A" and float(pbr) < 1):
        #Extract the Price per Earnings to Growth ratio
            PEG5 = BeautifulSoup(yahoo.decode().split('PEG Ratio (5 yr expected)')[1], 'html.parser').td.text
            #PEG5 = ticker.info['pegRatio']
            
            if ((PEG5 != "N/A") and (0 < float(PEG5) < 2)):
        #Extract the Total Debt to Equity ratio
                DE = BeautifulSoup(yahoo.decode().split('Total Debt/Equity')[1], 'html.parser').td.text
                #de_2 = ticker.info[]
                if DE != "N/A":
        #Extract the Trailing Price per Earnings ratio
                    TPE = BeautifulSoup(yahoo.decode().split('Trailing P/E')[1], 'html.parser').td.text
                    #TPE = ticker.info['trailingPE']
                    if (TPE != "N/A" and float(TPE) < 15):
        #Display the information acquired about the stock that meets all the criteria
                        print('____________________________________')
                        print(' ')
                        print(f'{Fore.GREEN}{Style.DIM}' + stock + f'{Style.RESET_ALL}' + ' meets requirements')
                        print('Price/Book :               ', pbr)
                        print('Price/Earnings to Growth : ', PEG5)
                        print('Trailing Price/Earnings :  ', TPE)
                        print('Debt to Equity :           ', DE)
                        print('50-Day Moving Average :    ', mv50)
                        print('200-Day Moving Average :   ', mv200)
                        print('____________________________________\n')
                    else:
                        print(f'{Fore.RED}{Style.DIM}' + stock + f'{Style.RESET_ALL}' + (5-len(stock))*' ' + ' does NOT meet Trailing Price/Earnings requirement')
                else:
                    print(f'{Fore.RED}{Style.DIM}' + stock + f'{Style.RESET_ALL}' + (5-len(stock))*' ' + ' does NOT meet Total Debt/Equity requirement')
            else:
                print(f'{Fore.RED}{Style.DIM}' + stock + f'{Style.RESET_ALL}' + (5-len(stock))*' ' + ' does NOT meet Price/Earnings to Growth requirement')
        else:
            print(f'{Fore.RED}{Style.DIM}' + stock + f'{Style.RESET_ALL}' + (5-len(stock))*' ' + ' does NOT meet Price/Book requirement')

    except Exception as e:
        print('Failed in the main loop', str(e))


def getIndex():
    """
        List the available indexes from the folder "Indexes/"

        Input :
            None
    """

    print('====================================')
    print('Searching which index ?\n')
    for file in os.listdir('Indexes/'):
        print(file.split('.txt')[0], end='    ')
    print('\n')
    index = input()

    if index + '.txt' in os.listdir('Indexes/'):
        print('====================================\n')
        return index + '.txt'
    else:
        print(f'\n{Fore.RED}{Style.DIM}Invalid index{Style.RESET_ALL}\n')
        print('====================================\n')
        sys.exit()


def parseIndex(index):
    """
        Generate the list of tickers from the files in "Indexes/"

        Input :
            index : Selected index to search in (ex. sp500, russell3000, etc.)
    """

    tickers = []

    try:
        readFile = open('Indexes/' + index, "r").read()
        splitFile = readFile.split('\n')
        for eachLine in splitFile:
            splitLine = eachLine.split(' ')
            ticker = splitLine[-1]
            tickers.append(ticker)
        return tickers

    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    init()

    index = getIndex()
    tickers = parseIndex(index)

    print('Reading ' + f'{Fore.GREEN}{Style.DIM}' + index + f'{Style.RESET_ALL}' + ' file\n')

    for ticker in tickers:
        yahooKeyStats(ticker)