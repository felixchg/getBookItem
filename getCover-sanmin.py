import requests
from bs4 import BeautifulSoup
import os
import time

with open('list.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    parts = line.strip().split('\t')
    if len(parts) == 2:
        isbn = parts[0]
        filename = parts[1]

        time.sleep(5)

        url = f"https://www.sanmin.com.tw/search/index/?ct=ISBN&qu={isbn}"

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            search_layout = soup.find('div', class_='searchLayout')

            if search_layout:
                cover_div = search_layout.find('div', class_='Cover')

                if cover_div:
                    img = cover_div.find('img', class_='lazyload')
                    if img and 'data-src' in img.attrs:
                        data_src = img['data-src']

                        filename_with_extension = f"{filename}.jpg"

                        image_response = requests.get(data_src)
                        if image_response.status_code == 200:
                            with open(filename_with_extension, 'wb') as image_file:
                                image_file.write(image_response.content)
                                print(f"Downloaded {filename_with_extension} from Sanmin.")
                        else:
                            print(f"Failed to download {filename} from Sanmin. Status code: {image_response.status_code}")
                    else:
                        print(f"data-src link not found for {isbn}.")
                else:
                    print(f"Element with class 'Cover' not found for {isbn}.")
            else:
                print(f"Element with class 'searchLayout' not found for {isbn}.")
        else:
            print(f"Failed to retrieve data for {isbn} from Sanmin. Status code: {response.status_code}")
    else:
        print("Invalid line format in the list.")
