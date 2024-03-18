import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Tag

from scan.backend.worker.schema import Book, Provider, Chapter


def get_all_books(url: str) -> list[Book]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', class_='series')
    return [Book(name=link.text, href=link.get('href'), provider=Provider.ASURA_TOON) for link in links if link.text]


def get_chapter_number(chapter_tag: Tag):
    try:
        return float(''.join(filter(str.isdigit, chapter_tag.select_one('a').get('href').split('-')[-1])))
    except:
        return float(chapter_tag.select_one('a').select_one('span').contents[0].split(' ')[1])


def get_book_data(book: Book) -> Book:
    response = requests.get(book.href)
    soup = BeautifulSoup(response.text, 'html.parser')
    chapters_data = soup.find('div', id='chapterlist').select('li')
    book.chapters = [Chapter(href=chapter.select_one('a').get('href'),
                             number=get_chapter_number(chapter)) for chapter in chapters_data]
    book.last_updated = soup.find('time', itemprop='dateModified').get('datetime')
    return book


def create_folder(book: Book, chapter: Chapter) -> None:
    Path(f"data/{book.get_book_name_formatted()}/{chapter.number}").mkdir(parents=True, exist_ok=True)


def is_folder_exists(book: Book, chapter: Chapter) -> bool:
    return Path(f"data/{book.get_book_name_formatted()}/{chapter.number}").is_dir()


def is_folder_not_empty(book: Book, chapter: Chapter) -> bool:
    return len(os.listdir(f"data/{book.get_book_name_formatted()}/{chapter.number}")) > 0


def download_book(book: Book) -> None:
    if not book.chapters:
        return

    for chapter in book.chapters:
        if is_folder_exists(book, chapter) and is_folder_not_empty(book, chapter):
            continue
        create_folder(book, chapter)
        response = requests.get(chapter.href)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find('div', id='readerarea').select('img')
        for image in images:
            img_data = requests.get(image.get('src')).content
            image_format = image.get('src').split('.')[-1]
            with open(f"data/{book.get_book_name_formatted()}/{chapter.number}/{images.index(image)}.{image_format}", 'wb') as handler:
                handler.write(img_data)
            chapter.images.append(image.get('src'))


url = "https://asuratoon.com/manga/list-mode/"
books = get_all_books(url)
first_complete_book = get_book_data(books[120])
download_book(first_complete_book)

