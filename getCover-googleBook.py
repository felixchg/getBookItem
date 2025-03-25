import requests
import os
import time

with open('list.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    parts = line.strip().split('\t')
    if len(parts) == 2:
        isbn = parts[0]
        base_filename = parts[1]

        time.sleep(5)

        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()
            items = json_data.get("items", [])

            if items:
                item = items[0]
                volume_info = item.get("volumeInfo", {})
                image_links = volume_info.get("imageLinks", {})
                small_thumbnail = image_links.get("thumbnail", "")

                if small_thumbnail:
                    filename = f"{base_filename}.jpg"

                    image_response = requests.get(small_thumbnail)
                    if image_response.status_code == 200:
                        with open(filename, 'wb') as image_file:
                            image_file.write(image_response.content)
                            print(f"Downloaded {filename} with smallThumbnail.")
                    else:
                        print(f"Failed to download {filename}.")
                else:
                    print(f"No smallThumbnail found for {isbn}.")
            else:
                print(f"No results found for {isbn}.")
        else:
            print(f"Failed to retrieve data for {isbn}. Status code: {response.status_code}")
    else:
        print("Invalid line format in the list.")
