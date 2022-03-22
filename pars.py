import requests
from bs4 import BeautifulSoup

price_list=[]
link_list=[]

for p in range(1, 26):
    url = f'https://www.olx.ua/nedvizhimost/kvartiry/prodazha-kvartir/kiev/?page={p}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    flats = soup.find_all('tr', class_='wrap')
    for flat in flats:
        price = flat.find('p', class_='price').text
        pr=price
        for i in pr:
            if i.isnumeric() == False:
                pr = pr.replace(i, '')
        if int(pr) <= 2000000:
            link = flat.find('a').get('href')

            url1 = link
            page1 = requests.get(url1)
            soup1 = BeautifulSoup(page1.text, 'lxml')

            info=soup1.find_all('p',class_="css-xl6fe0-Text eu5v0x0")
            for inf in info:
                if 'Количество комнат' in inf.text:
                    rooms=inf.text
                    for j in rooms:
                        if j.isnumeric() == False:
                             rooms = rooms.replace(j, '')
                    if int(rooms)==3:
                        #print(link, price.strip())
                        price_list.append(price.strip())
                        link_list.append(link)
print(price_list)