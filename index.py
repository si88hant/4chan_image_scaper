import requests
from bs4 import BeautifulSoup
import os
import shutil

url = 'https://boards.4channel.org/po/thread/609865'
folder_name = 'christmas origami'

save_dir = os.path.expanduser(f'~/Downloads/4chan_images/{folder_name}')
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    image_links = soup.find_all('a', {'class': 'fileThumb'})
    for i, link in enumerate(image_links):
        image_url = 'https:' + link.get('href')
        image_response = requests.get(image_url, stream=True)
        if image_response.status_code == 200:
            with open(os.path.join(save_dir, f'image_{i}.jpg'), 'wb') as f:
                image_response.raw.decode_content = True
                shutil.copyfileobj(image_response.raw, f)
            print(f'Saved {image_url}')
        else:
            print(f'Error downloading {image_url}: {image_response.status_code}')
else:
    print(f'Error: {response.status_code}')
