import json
import os
import re
from io import BytesIO

import requests
from PIL import Image
from bs4 import BeautifulSoup

# Global configuration
config = {
    'overwrite': False,  # Set to True to overwrite existing images, False to skip downloading if the file already exists
    'base_url': 'https://raw.githubusercontent.com/atomstudiosfr/scan/main/assets/',  # Base URL for the JSON links
    'downloads_dir': '../assets',
    'site_url': 'https://reaper-scans.com/manga/list-mode/',
    'ignore_existing_manga': True,  # Set to True to ignore retrieving a manga if the folder already exists
    'ignore_existing_chapter': True,  # Set to True to ignore retrieving a chapter if the folder already exists
    'check_new_chapters': False  # Set to True to search for new chapters for existing manga
}


def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_manga_list_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    manga_links = []
    for link in soup.select('a.series.tip'):
        manga_links.append((link['href'], link.get_text()))
    return manga_links


def parse_manga_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    chapters = []
    for chapter in soup.select('.eph-num a'):
        chapters.append(chapter['href'])
    return chapters


def parse_manga_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    description = soup.select_one('.entry-content.entry-content-single[itemprop="description"]').get_text(strip=True)

    # Find the author from the table
    author = 'Unknown'
    info_table = soup.select_one('table.infotable')
    if info_table:
        for row in info_table.select('tr'):
            cells = row.find_all('td')
            if len(cells) > 1 and cells[0].get_text(strip=True) == 'Author':
                author = cells[1].get_text(strip=True)
                break

    # Attempt to find the cover image from meta tags
    cover_url = None
    meta_tag = soup.find('meta', property='og:image')
    if meta_tag and 'content' in meta_tag.attrs:
        cover_url = meta_tag['content']
    else:
        meta_tag = soup.find('meta', property='og:image:secure_url')
        if meta_tag and 'content' in meta_tag.attrs:
            cover_url = meta_tag['content']

    # Fall back to finding the cover image from bigcover and bigbanner
    if not cover_url:
        cover_div = soup.select_one('.bigcover .bigbanner')
        if cover_div:
            cover_url = re.search(r"url\('(.+?)'\)", cover_div['style']).group(1)

    return description, author, cover_url


def parse_chapter_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    images = []
    for img in soup.select('img'):
        if 'data-src' in img.attrs:
            images.append(img['data-src'])
    return images


def save_images(image_urls, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for url in image_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_name = os.path.splitext(url.split('/')[-1])[0] + '.webp'
            image_path = os.path.join(save_dir, image_name)
            if os.path.exists(image_path):
                if config['overwrite']:
                    os.remove(image_path)
                else:
                    print(f"Skipping {image_name}, already exists")
                    continue
            img = Image.open(BytesIO(response.content))
            img.save(image_path, 'webp')
            print(f"Saved {image_name}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
        except Exception as e:
            print(f"Error processing {url}: {e}")


def save_image(url, path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        webp_path = os.path.splitext(path)[0] + '.webp'
        img.save(webp_path, 'webp')
        print(f"Saved cover image: {webp_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
    except Exception as e:
        print(f"Error processing {url}: {e}")


def clean_directory(directory):
    pattern = re.compile(r"^(chapter[-_]?\d+|\d+)\..+$", re.IGNORECASE)
    for root, _, files in os.walk(directory):
        for file in files:
            if not pattern.match(file):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Removed {file_path}")


def clean_chapters(chapters):
    cleaned_chapters = []
    seen = set()
    for chapter in chapters:
        chapter_number = extract_chapter_number(chapter)
        if chapter_number not in seen:
            seen.add(chapter_number)
            cleaned_chapters.append(chapter)
    return cleaned_chapters


def update_scans_json(manga_title, description, author, chapter_title, image_urls, cover_url):
    json_path = os.path.join(config['downloads_dir'], 'scans.json')
    data = []

    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}")

    # Check if manga entry already exists
    manga_entry = next((item for item in data if item['title'] == manga_title), None)
    if not manga_entry:
        manga_entry = {
            'title': manga_title,
            'author': author,
            'description': description,
            'cover': f"{config['base_url']}{manga_title}/cover.webp",
            'chapters': []
        }
        data.append(manga_entry)

    # Create a new chapter entry
    chapter_entry = {
        'title': f"Chapter {chapter_title}",
        'pages': [f"{config['base_url']}{manga_title}/{chapter_title}/{os.path.splitext(url.split('/')[-1])[0]}.webp" for url in image_urls]
    }
    manga_entry['chapters'].append(chapter_entry)

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Updated scans.json with {manga_title} - Chapter {chapter_title}")


def extract_chapter_number(chapter_url):
    match = re.search(r'(\d+)(?!.*\d)', chapter_url)
    if match:
        return match.group(1)
    return 'unknown'


def get_highest_chapter(directory):
    highest_chapter = 0
    for name in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, name)):
            chapter_number = extract_chapter_number(name)
            if chapter_number != 'unknown' and int(chapter_number) > highest_chapter:
                highest_chapter = int(chapter_number)
    return highest_chapter


def main():
    main_page_html = fetch_page(config['site_url'])
    if main_page_html:
        manga_links = parse_manga_list_page(main_page_html)
        for manga_url, manga_title in manga_links:
            manga_dir = os.path.join(config['downloads_dir'], manga_title)
            if config['ignore_existing_manga'] and os.path.exists(manga_dir):
                print(f"Skipping manga: {manga_title}, already exists")
                continue

            if config['check_new_chapters'] and os.path.exists(manga_dir):
                highest_chapter = get_highest_chapter(manga_dir)
                next_chapter = highest_chapter + 1
                chapter_url = manga_url + f'/chapter-{next_chapter}/'
                chapter_page_html = fetch_page(chapter_url)
                if chapter_page_html:
                    print(f"Found new chapter: {next_chapter} for manga: {manga_title}")
                    images = parse_chapter_page(chapter_page_html)
                    chapter_dir = os.path.join(manga_dir, str(next_chapter))
                    save_images(images, chapter_dir)
                    description, author, cover_url = parse_manga_details(manga_page_html)
                    update_scans_json(manga_title, description, author, str(next_chapter), images, cover_url)
                    clean_directory(chapter_dir)  # Clean directory after each chapter download
                continue

            print(f"Fetching manga: {manga_title}")
            manga_page_html = fetch_page(manga_url)
            if manga_page_html:
                description, author, cover_url = parse_manga_details(manga_page_html)

                if cover_url:
                    # Save cover image
                    cover_path = os.path.join(manga_dir, 'cover.webp')
                    save_image(cover_url, cover_path)
                    chapters = parse_manga_page(manga_page_html)
                    chapters = clean_chapters(chapters)  # Clean chapters before processing
                    for chapter_url in chapters:
                        chapter_number = extract_chapter_number(chapter_url)  # Extract chapter number
                        chapter_dir = os.path.join(manga_dir, chapter_number)
                        if config['ignore_existing_chapter'] and os.path.exists(chapter_dir):
                            print(f"Skipping chapter: {chapter_number} of manga: {manga_title}, already exists")
                            continue

                        print(f"Fetching chapter: {chapter_url}")
                        chapter_page_html = fetch_page(chapter_url)
                        if chapter_page_html:
                            images = parse_chapter_page(chapter_page_html)
                            save_images(images, chapter_dir)
                            update_scans_json(manga_title, description, author, chapter_number, images, cover_url)
                            clean_directory(chapter_dir)  # Clean directory after each chapter download


if __name__ == "__main__":
    main()
