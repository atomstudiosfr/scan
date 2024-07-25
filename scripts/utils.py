import os
import re
import requests
from PIL import Image
from io import BytesIO
from config import config

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

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

def clean_chapters(chapters):
    cleaned_chapters = []
    seen = set()
    for chapter in chapters:
        chapter_number = extract_chapter_number(chapter)
        if chapter_number not in seen:
            seen.add(chapter_number)
            cleaned_chapters.append(chapter)
    return cleaned_chapters
