from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd
import datetime as dt

url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/TextView.aspx?data=yieldAll"

# download the HTML data and parse
webpage = urlopen(url)
parsed = webpage.read().decode('utf-8')
soup = bs(parsed, 'lxml')

# get data from HTML data table
table_html = soup.find_all("tr", {"class": ["oddrow", "evenrow"]})

# 1 Month TBill Rates DataFrame - empty initially
data_1month_tbill_rates = pd.DataFrame()
date = []
rate = []

for row in table_html:
    full_row = row.find_all("td", {"class": "text_view_data"})
    rate_str = full_row[1].text

    if "N/A" not in rate_str:
        date_str = full_row[0].text
        rate.append(float(rate_str))
        date.append(dt.datetime.strptime(date_str[0:6] + "20" + date_str[6:8], "%m/%d/%Y"))

date = pd.DataFrame({"Date": date})
data_1month_tbill_rates = pd.DataFrame({"TBill-1m": rate})
data_1month_tbill_rates = data_1month_tbill_rates.join(date)
data_1month_tbill_rates = data_1month_tbill_rates.set_index("Date")/100

data_1month_tbill_rates.to_excel("TBill 1m Daily.xlsx")
