import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math

stocks = pd.read_csv("sp_500_stocks.csv")
stocks


IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'

symbol = 'AAPL'
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url).json()
print(data)


price = data['latestPrice']
market_cap = data['marketCap']


my_columns = ['Ticker', 'Stock Price', 'Market Capitilazation', 'Number of Shares to Buy']
final_dataframe = pd.DataFrame(columns = my_columns)
final_dataframe


# Panda series require series for columns and lines separately + panda series accepts a python list which is = []
final_dataframe.append(
    pd.Series(
        [

        ]
        )

)


final_dataframe = pd.DataFrame(columns = my_columns)
for stock in stocks['Ticker'][:10]:
    api_url = f'https://sandbox.iexapis.com/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url).json()
    final_dataframe = final_dataframe.append(
        pd.Series(
        [
            stock,
            data['latestPrice'],
            data['marketCap'],
            'N/A'
        ],
        index = my_columns),
    ignore_index = True
    )
final_dataframe


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
#    print(symbol_strings[i])
final_dataframe = pd.DataFrame(columns=my_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
            pd.Series(
                [
                    symbol,
                    data[symbol]['quote']['latestPrice'],
                    data[symbol]['quote']['marketCap'],
                    'N/A'

                ],
                index=my_columns),
            ignore_index=True
        )
final_dataframe

# print(data.status_code)   , if this prints 200, then i works properly


portfolio_size = input('Enter the value of your portfolio size:')

try:
    val = float(portfolio_size)


except ValueError:
    print("That's not a number\nPlease try again:")
    protfolio_size = input('Enter the value of your portfolio:')
    val = float(portfolio_size)


position_size = val/len(final_dataframe.index)
for i in range(0, len(final_dataframe.index)):
    final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i, 'Stock Price'])
final_dataframe
# number_of_apple_shares = position_size/500$
# print(math.floor(number_of_apple_shares))



writer = pd.ExcelWriter('Recommended_trades.xlsx', engine = 'xlsxwriter')
final_dataframe.to_excel(writer, 'Recommended Trades', index = False)

background_color = '#0a0a23'
font_color = 'ffffff'
string_format = writer.book.add_format(
    {
        'font_color': font_color,
        'bg_color': background_color,
        'border': 1

    }

)
dollar_format = writer.book.add_format(
    {
        'num_format': '$0,00',
        'font_color': font_color,
        'bg_color': background_color,
        'border': 1

    }

)
integer_format = writer.book.add_format(
    {
        'num_format': '0',
        'font_color': font_color,
        'bg_color': background_color,
        'border': 1

    }

)



#writer.sheets['Recommended Trades'].set_column('A:A', 18, string_format)
#writer.sheets['Recommended Trades'].set_column('B:B', 18, string_format)
#writer.sheets['Recommended Trades'].set_column('C:C', 18, string_format)
#writer.sheets['Recommended Trades'].set_column('D:D', 18, string_format)
#writer.save()
writer.sheets['Recommended Trades'].write('A1', 'Ticker', string_format)
writer.sheets['Recommended Trades'].write('B1', 'Stock Price', dollar_format)
writer.sheets['Recommended Trades'].write('C1', 'Market Capitilization', dollar_format)
writer.sheets['Recommended Trades'].write('D1', 'Number of shares to Buy', integer_format)

column_formats = {
    'A': ['Ticker', string_format],
    'B': ['Stock Price', dollar_format],
    'C': ['Market Cap', dollar_format],
    'D': ['Number of Shares to Buy', integer_format]

}

for column in column_formats.keys():
    writer.sheets['Recommended Trades'].set_column(f'{column}:{column}', 18, column_formats[column][1])


writer.save()




