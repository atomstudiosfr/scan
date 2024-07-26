import json
import os

from config import config


def update_root_scans_json(manga_title, description, author, cover_url):
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
            'cover': f"{config['base_url']}{manga_title}/cover.webp"
        }
        data.append(manga_entry)

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Updated root scans.json with {manga_title}")


def update_manga_scans_json(manga_dir, chapter_number, images):
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
    images = [os.path.join(config['base_url'], os.path.relpath(image, config['downloads_dir'])).replace('\\', '/') for image in images]

    # Find the chapter entry if it exists
    chapter_entry = None
    for chapter in data:
        if chapter['chapter'] == chapter_number:
            chapter_entry = chapter
            break

    if chapter_entry:
        chapter_entry['pages'] = images
    else:
        chapter_entry = {
            'chapter': chapter_number,
            'pages': images
        }
        data.append(chapter_entry)

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Updated scans.json for manga: {os.path.basename(manga_dir)}, chapter: {chapter_number}")
