import os
from typing import List
from core.schema import Manga, Chapter

def get_manga_list(directory: str) -> List[Manga]:
    manga_list = []
    for manga_name in os.listdir(directory):
        manga_path = os.path.join(directory, manga_name)
        if os.path.isdir(manga_path):
            cover = os.path.join('assets', 'scans', manga_name, 'cover.jpg')
            chapters = []
            for chapter_name in os.listdir(manga_path):
                chapter_path = os.path.join(manga_path, chapter_name)
                if os.path.isdir(chapter_path):
                    pages = [
                        os.path.join('assets', 'scans', manga_name, chapter_name, page)
                        for page in os.listdir(chapter_path)
                    ]
                    chapters.append(Chapter(title=chapter_name, pages=pages))
            manga_list.append(Manga(
                title=manga_name,
                author='Unknown',  # Replace with actual author if available
                description='',  # Replace with actual description if available
                cover=cover,
                chapters=chapters
            ))
    return manga_list

class ScanController:

    @staticmethod
    def get_scans() -> List[Manga]:
        manga_directory = os.path.join(os.getcwd(), 'assets', 'scans')
        return get_manga_list(manga_directory)
