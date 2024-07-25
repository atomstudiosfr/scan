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


def update_manga_scans_json(manga_dir, chapter_title, image_urls):
    json_path = os.path.join(manga_dir, 'scans.json')
    data = {'chapters': []}

    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}")

    # Create a new chapter entry
    chapter_entry = {
        'title': f"Chapter {chapter_title}",
        'pages': [f"{config['base_url']}{os.path.basename(manga_dir)}/{chapter_title}/{os.path.splitext(url.split('/')[-1])[0]}.webp" for
                  url in image_urls]
    }
    data['chapters'].append(chapter_entry)

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Updated scans.json in {manga_dir} with Chapter {chapter_title}")
