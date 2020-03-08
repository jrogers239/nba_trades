import urllib3
from bs4 import BeautifulSoup as bs
import pandas as pd
import os.path
import sys
import csv
from pathlib import Path

# Grabs raw web page from basketball reference and converts it into a text file for NLP functionality
class raw_text(object):

    def process_raw_text(self, year):

        url = 'https://www.basketball-reference.com/leagues/NBA_{}_transactions.html'.format(year)
        http = urllib3.PoolManager()
        response = http.request('GET',url)
        soup = bs(response.data,'html.parser')

        transaction_str = ""
        transaction_df = pd.DataFrame()

        rows = soup.find('ul',attrs={'class': 'page_index'})

        for row in rows.find_all('li'):
            dates = row.find_all('span')
            for date in dates:
                cells = row.find_all('p')
                for cell in cells:
                    transaction = [[date.text,cell.text]]

                    transaction_str+=date.text + " "
                    transaction_str+=cell.text + " "
                    # print(date.text,cell.text)
                    df_hold = pd.DataFrame(transaction)
                    transaction_df = transaction_df.append(df_hold)

        return transaction_df, transaction_str

# Saves rawr text file / dataframe from basketball reference (No NLP Yet)
class save_raw_text(object):

    def __init__(self):
        self.path =  Path(__file__).parent.parent.parent

    def csv_txt_raw_text(self, year):
        df, text = raw_text().process_raw_text(year)

        df_path = os.path.join(str(self.path),"data/raw/df_trades_{}.csv".format(year))
        df.to_csv(df_path)

        with open(os.path.join(str(self.path),"data/raw/text_trades_{}.txt".format(year)),'w+') as file:
            file.write(text)
            file.close()
class process_raw_text(object):

    def __init__(self):
        self.path =  Path(__file__).parent.parent.parent


    def normalize_sentences(self, year):

        with open(os.path.join(str(self.path),"data/raw/text_trades_{}.txt".format(year)),'r+') as file:
            text = file.read()
            file.close()
            # Lowercase all words
            text = text.lower()

            # remove commas and periods
            text = text.replace(",","").replace(".","")
            print(text)


process_raw_text().normalize_sentences(2019)
