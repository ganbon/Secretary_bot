from bs4 import BeautifulSoup
import requests


def scraping(url, file_path):
    responses = requests.get(url)
    soup = BeautifulSoup(responses.content, 'html.parser')
    text_list = soup.get_text().splitlines()
    text_list = list(set(text_list))
    print(text_list)
    text_list = [text.replace('\u3000', '') for text in text_list]
    text = '\n'.join(text_list)
    with open(file_path, 'w', encoding='utf_8') as f:
        f.write(text)


# scraping('https://www3.nhk.or.jp/news/html/20220421/k10013592581000.html','b.txt')
