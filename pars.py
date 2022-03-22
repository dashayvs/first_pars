import requests
from bs4 import BeautifulSoup
import pandas as pd

price_list = []
link_list = []
temp=[]
sorted_price=[]
sorted_link=[]

def get_link_price():

    global price_list, link_list

    for p in range(1, 26):
        url = f'https://www.olx.ua/nedvizhimost/kvartiry/prodazha-kvartir/kiev/?page={p}'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')

        flats = soup.find_all('tr', class_='wrap')
        for flat in flats:
            price = flat.find('p', class_='price').text
            pr = price
            for i in pr:
                if i.isnumeric() == False:
                    pr = pr.replace(i, '')
            if int(pr) <= 2000000:
                link = flat.find('a').get('href')

                url1 = link
                page1 = requests.get(url1)
                soup1 = BeautifulSoup(page1.text, 'lxml')

                info = soup1.find_all('p', class_="css-xl6fe0-Text eu5v0x0")
                for inf in info:
                    if 'Количество комнат' in inf.text:
                        rooms = inf.text
                        for j in rooms:
                            if j.isnumeric() == False:
                                rooms = rooms.replace(j, '')
                        if int(rooms) == 3:
                            temp.append(pr)
                            price_list.append(price.strip())
                            link_list.append(link)

def sort():

    global sorted_price, sorted_link

    temp1 = sorted(temp)
    for i in temp1:
        sorted_price.append(price_list[temp.index(i)])
        sorted_link.append(link_list[temp.index(i)])

def dataframe():
    data=pd.DataFrame({
       'Link':sorted_link,
       'Price':sorted_price
      },index=range(1,len(sorted_price)+1))
    #data.pd.set_option('display.max_colwidth', None)
    #max_len_price=len(max(sorted_price,key=len))
    #max_len_link=len(max(sorted_link,key=len))

    return data

get_link_price()
sort()

writer = pd.ExcelWriter('flats.xlsx')
dataframe().to_excel(writer)
writer.save()
print('DataFrame is written successfully to Excel File.')