import requests
import os
import time

with open('list.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    parts = line.strip().split('\t')
    if len(parts) == 2:
        isbn = parts[0]
        filename = parts[1]

        url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg?default=false"

        time.sleep(5)

        response = requests.get(url)

        if response.status_code == 200:
            filename_with_extension = f"{filename}.jpg"

            with open(filename_with_extension, 'wb') as image_file:
                image_file.write(response.content)
                print(f"Downloaded {filename_with_extension} from Open Library Covers.")
        else:
            print(f"Failed to download {filename} from Open Library Covers. Status code: {response.status_code}")
    else:
        print("Invalid line format in the list.")
