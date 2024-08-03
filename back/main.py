import os
import asyncio
from config import config
from utils import fetch_page, save_images, save_image, clean_directory, extract_chapter_number, get_highest_chapter, clean_chapters
from parsers import parse_manga_list_page, parse_manga_page, parse_manga_details, parse_chapter_page
from update_json import update_root_scans_json, update_manga_scans_json


async def get_cleaned_images(chapter_dir):
    # List all files in the directory after cleaning
    return [os.path.join(chapter_dir, f) for f in os.listdir(chapter_dir) if os.path.isfile(os.path.join(chapter_dir, f))]


async def process_chapter(site, manga_dir, chapter_url):
    chapter_number = extract_chapter_number(chapter_url)
    if chapter_number is None:
        return
    chapter_dir = os.path.join(manga_dir, str(chapter_number))
    if site.ignore_existing_chapter and os.path.exists(chapter_dir):
        print(f"Skipping chapter: {chapter_number} of manga: {manga_dir}, already exists")
        return
    chapter_page_html = await fetch_page(chapter_url)
    if chapter_page_html:
        images = await parse_chapter_page(chapter_page_html, site.selectors)
        webp_images = await save_images(images, chapter_dir, site.overwrite)
        clean_directory(chapter_dir)
        cleaned_images = await get_cleaned_images(chapter_dir)
        update_manga_scans_json(site, manga_dir, str(chapter_number), cleaned_images)


async def process_manga(site, manga_url, manga_title):
    manga_dir = os.path.join(site.downloads_dir, manga_title)
    if site.ignore_existing_manga and os.path.exists(manga_dir):
        print(f"Skipping manga: {manga_title}, already exists")
        return
    manga_page_html = await fetch_page(manga_url)
    if manga_page_html:
        description, author, cover_url = await parse_manga_details(manga_page_html, site.selectors)
        if cover_url:
            cover_path = os.path.join(manga_dir, 'cover.webp')
            await save_image(cover_url, cover_path, site.overwrite)
        chapters = await parse_manga_page(manga_page_html, site.selectors)
        chapters = clean_chapters(chapters)
        chapters = [ch for ch in chapters if extract_chapter_number(ch) is not None]
        chapters.sort(key=extract_chapter_number)

        # Process chapters in batches of 10
        for i in range(0, len(chapters), 10):
            batch = chapters[i:i + 10]
            tasks = [process_chapter(site, manga_dir, ch) for ch in batch]
            await asyncio.gather(*tasks)

        # Update root scans.json after processing all chapters
        update_root_scans_json(site, manga_title, description, author, cover_url)


async def main():
    for site in config.sites:
        main_page_html = await fetch_page(site.site_url)
        if main_page_html:
            manga_links = parse_manga_list_page(main_page_html, site.selectors)
            for manga_url, manga_title in manga_links:
                try:
                    await process_manga(site, manga_url, manga_title)  # Ensure mangas are processed sequentially
                except:
                    pass


if __name__ == "__main__":
    asyncio.run(main())
