from queue import Empty
from csv import writer
import requests
from bs4 import BeautifulSoup
from bs4 import element

URL = "https://somon.tj/nedvizhimost/prodazha-kvartir/dushanbe/?page="
page = requests.get(URL+str(1))
soup = BeautifulSoup(page.content,'html.parser')
result = soup.find("ul",class_="number-list")
pages = [int(item.find("a").text) for item in result if item.find("a") is not None and isinstance(item,element.Tag)][-1]

def page_parser(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    result = soup.find("ul",class_="list-simple__output")
    for item in result:
        if isinstance(item,element.Tag):
            meta = item.find("a").text.strip().split(",")
            print(meta)
            if "-" in meta[0]:
                number_of_rooms = int(meta[0].split("-")[0])
            else:
                number_of_rooms = int(meta[0].split(" ")[0])
            if meta[1].split()[0].isnumeric():
                if meta[1].split()[0] == '²':
                    floor = 2
                else:
                    floor = int(meta[1].split()[0])
            else:
                floor = 0
            if len(meta) > 3:
                if meta[2].split()[0].isnumeric():
                    area = float(meta[2].split()[0])
                    if len(meta) == 4:
                        address = meta[3].strip()
                    else:
                        address=""
                else:
                    area = 50
                    if len(meta) == 3:
                        address = meta[2].strip()
                    else:
                        address=""
            else:
                area = 50
                address=""
            # print(number_of_rooms)
            # print(floor)
            # print(area)
            # print(address)
            description = item.find("div",class_="announcement-block__description").text.strip()
            # print(description)
            date = item.find("div",class_="announcement-block__date").text.strip().split(",")[0].strip()
            # print(date)
            price = "".join(item.find("div",class_="announcement-block__price").text.strip().split()[0:-1])
            if 'c' in price:
                price = price[0:price.find('c')]
            
            row = [number_of_rooms,floor,area,address,date,price]
            write_obj.writerow(row)
        
    return
header = ['nuber_of_rooms','floor','area','address','date','price']
with open("estate_data.csv",'a',newline='') as obj:
    write_obj = writer(obj)
    write_obj.writerow(header)
    for i in range(1,pages+1):
        page_parser(URL+str(i))
    obj.close()
