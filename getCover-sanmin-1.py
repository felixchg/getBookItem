# pip install requests
# pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup
import string
import random

url = "https://www.sanmin.com.tw/search/index/?ct=ISBN&qu=4710660285384"

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
                filename = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(8))
                filename_with_extension = f"{filename}.jpg"

                image_response = requests.get(data_src)
                if image_response.status_code == 200:
                    with open(filename_with_extension, 'wb') as image_file:
                        image_file.write(image_response.content)
                        print(f"Downloaded {filename_with_extension} from Sanmin.")
                else:
                    print(f"Failed to download image from Sanmin. Status code: {image_response.status_code}")
            else:
                print("data-src not found")
        else:
            print("Element with class 'Cover' not found")
    else:
        print("Element with class 'searchLayout' not found on the page")
else:
    print("Failed to retrieve data. Status code:", response.status_code)
