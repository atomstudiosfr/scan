import os
from config import config
from utils import fetch_page, save_images, save_image, clean_directory, extract_chapter_number, get_highest_chapter, clean_chapters
from parsers import parse_manga_list_page, parse_manga_page, parse_manga_details, parse_chapter_page
from update_json import update_root_scans_json, update_manga_scans_json

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
                    update_manga_scans_json(manga_dir, str(next_chapter), images)
                    clean_directory(chapter_dir)  # Clean directory after each chapter download
                continue

            print(f"Fetching manga: {manga_title}")
            manga_page_html = fetch_page(manga_url)
            if manga_page_html:
                description, author, cover_url = parse_manga_details(manga_page_html)

                # Update root scans.json before processing chapters
                update_root_scans_json(manga_title, description, author, cover_url)

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
                        update_manga_scans_json(manga_dir, chapter_number, images)
                        clean_directory(chapter_dir)  # Clean directory after each chapter download

if __name__ == "__main__":
    main()
