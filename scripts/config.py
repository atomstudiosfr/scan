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
