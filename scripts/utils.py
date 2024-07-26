import os
import re
import requests
from PIL import Image

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def convert_to_webp(image_path):
    try:
        image = Image.open(image_path)
        webp_path = os.path.splitext(image_path)[0] + '.webp'
        image.save(webp_path, 'webp')
        os.remove(image_path)
        print(f"Converted {image_path} to {webp_path}")
        return webp_path
    except Exception as e:
        print(f"Error converting {image_path} to WebP: {e}")
        return image_path

def save_images(image_urls, save_dir, overwrite=False):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    webp_images = []
    for url in image_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_name = url.split('/')[-1]
            image_path = os.path.join(save_dir, image_name)
            if os.path.exists(image_path):
                if overwrite:
                    os.remove(image_path)
                else:
                    print(f"Skipping {image_name}, already exists")
                    webp_images.append(image_path)  # Keep the existing image
                    continue
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Saved {image_name}")

            if image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = convert_to_webp(image_path)
            webp_images.append(image_path)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
    return webp_images

def save_image(url, path, overwrite=False):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        response = requests.get(url)
        response.raise_for_status()
        if os.path.exists(path):
            if overwrite:
                os.remove(path)
            else:
                print(f"Skipping cover image, already exists")
                return
        with open(path, 'wb') as f:
            f.write(response.content)
        print(f"Saved cover image: {path}")

        if path.lower().endswith(('.png', '.jpg', '.jpeg')):
            convert_to_webp(path)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

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

def get_highest_chapter(manga_dir):
    chapters = [int(d) for d in os.listdir(manga_dir) if os.path.isdir(os.path.join(manga_dir, d)) and d.isdigit()]
    return max(chapters) if chapters else 0

def clean_chapters(chapters):
    cleaned_chapters = []
    seen = set()
    for chapter in chapters:
        chapter_number = extract_chapter_number(chapter)
        if chapter_number not in seen:
            seen.add(chapter_number)
            cleaned_chapters.append(chapter)
    return cleaned_chapters
