import requests
from bs4 import BeautifulSoup
import pandas as pd
import pyperclip
from pymongo import MongoClient
import time
from lxml import etree
import re

def get_zb(link):
    response = requests.get(link[0])
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')  # find the table in the webpage

    data = []
    for row in table.find_all('tr'):  # find each row in the table
        cols = row.find_all('td')  # find each column in the row
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)
    
    return data
def process_data(link):
    # Load the data
    df = pd.DataFrame(get_zb(link))

    # Initialize a city variable with a default value
    current_city = '未知'

    # Define a function to determine the city
    def determine_city(row):
        nonlocal current_city
        try:
            if pd.notnull(row[0]) and pd.isnull(row[1]) and pd.isnull(row[2]) and pd.isnull(row[3]):
               current_city = row[0]
        except (KeyError, IndexError):
            pass
        return current_city



    # Apply the function to each row
    df['城市'] = df.apply(determine_city, axis=1)

    # Remove the rows with city names
    try:
        df = df.dropna(subset=[1, 2, 3], how='all')
    except KeyError as e:
        print(f"An error occurred: {e}")

    # Rename the columns
    df.columns = ['中标时间', '项目名称', '中标金额(万元)', '中标公司', '城市']
    df = df[df['中标金额(万元)'].str.contains('万元')]
    # Drop the first row
    df = df.iloc[1:]
    # Convert "中标金额(人民币)" to numeric
    df['中标金额(万元)'] = df['中标金额(万元)'].str.extract(r'(\d+)').astype(float)

    # Add a temporary year to "中标时间" and convert it to datetime
    df['中标时间'] = str(link[1][:4]) +'年' + df['中标时间']
    df['中标时间'] = pd.to_datetime(df['中标时间'], format='%Y年%m月%d日')
    return df
def to_mongo(df):
    client = MongoClient('localhost', 27017)
    db = client['中标公示']
    collection = db['Landscape']
    collection.insert_many(df.to_dict('records'))
def get_date(url):
    response = requests.get(url)
    root = etree.HTML(response.text)
    activity_name = root.xpath("//h1[@id='activity-name']")[0]
    pattern = r"\d+"
    matches = re.findall(pattern, activity_name.text)
    return matches


if __name__ == "__main__":
    url = pyperclip.paste()
    year,month = get_date(url)
    zbdf = process_data([url,year])
    to_mongo(zbdf)
    print(f'{year}年{month}月数据已存入数据库')