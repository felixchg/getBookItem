# pip install requests
# pip install BeautifulSoup4
import requests
from bs4 import BeautifulSoup
import json

url = "https://www.sanmin.com.tw/search/index/?ct=ISBN&qu=4710660285384"

response = requests.get(url)

book_info = {
    "Title": "",
    "Author": "",
    "Publisher": "",
    "PublishDate": "",
    "Description": ""
}

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    sproducts = soup.find_all('div', class_='sProduct')

    for sproduct in sproducts:
        title = sproduct.find('h3', class_='Title').find('a')

        title_tmp = title.text.strip()
        book_info["Title"] = title_tmp[2:]

        author_div = sproduct.find('div', class_='Author')

        author_info = author_div.text.strip()
        author_info = author_info.replace('出版社：', '').replace('出版日：', '')

        author_parts = author_info.split('\n')
        if len(author_parts) > 0:
            book_info["Author"] = author_parts[0].strip()
        if len(author_parts) > 1:
            book_info["Publisher"] = author_parts[1].strip()
        if len(author_parts) > 2:
            book_info["PublishDate"] = author_parts[2].strip()

        description_div = sproduct.find('div', class_='Description')
        if description_div is not None:
            book_info["Description"] = description_div.text.strip()

    book_json = json.dumps(book_info, ensure_ascii=False, indent=4)

    print(book_json)

else:
    print("Failed to retrieve data. Status code:", response.status_code)
  
