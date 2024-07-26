import os
import json
from typing import List
from schema import SiteConfig, Manga, Chapter

def update_root_scans_json(site: SiteConfig, manga_title: str, description: str, author: str, cover_url: str):
    json_path = os.path.join(site.downloads_dir, 'scans.json')
    data = {"mangas": []}

    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}")

    # Check if manga entry already exists
    manga_entry = next((item for item in data["mangas"] if item['title'] == manga_title), None)
    if not manga_entry:
        manga_entry = {
            "title": manga_title,
            "author": author,
            "description": description,
            "cover": cover_url
        }
        data["mangas"].append(manga_entry)

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4, default=str)
    print(f"Updated scans.json with {manga_title}")

def update_manga_scans_json(site: SiteConfig, manga_dir: str, chapter_number: str, images: List[str]):
    # Sort images by filename
    images = sorted(images, key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))

    json_path = os.path.join(manga_dir, 'scans.json')
    data = []

    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}")

    # Convert local paths to URLs
    images = [os.path.join(site.base_url.__str__(), os.path.relpath(image, site.downloads_dir)).replace('\\', '/') for image in images]

    # Find the chapter entry if it exists
    chapter_entry = None
    for chapter in data:
        if chapter['number'] == chapter_number:
            chapter_entry = chapter
            break

    if chapter_entry:
        chapter_entry['pages'] = images
    else:
        chapter_entry = Chapter(
            number=chapter_number,
            pages=images
        )
        data.append(chapter_entry.dict())

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4, default=str)
    print(f"Updated scans.json for manga: {os.path.basename(manga_dir)}, chapter: {chapter_number}")
