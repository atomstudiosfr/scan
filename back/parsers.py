import re

from bs4 import BeautifulSoup


def parse_manga_list_page(html, selectors):
    soup = BeautifulSoup(html, 'html.parser')
    manga_links = []
    for link in soup.select(selectors['manga_list_selector']):
        href = link.get('href')
        title = link.get('title')
        if href and title:
            manga_links.append((href, title))
    return manga_links


async def parse_manga_page(html, selectors):
    soup = BeautifulSoup(html, 'html.parser')
    chapters = []
    for chapter in soup.select(selectors['chapter_selector']):
        chapters.append(chapter['href'])
    return chapters


async def parse_manga_details(html, selectors):
    soup = BeautifulSoup(html, 'html.parser')
    description = soup.select_one(selectors['description_selector']).get_text(strip=True)

    # Find the author from the table
    author = 'Unknown'
    info_table = soup.select_one(selectors['author_table_selector'])
    if info_table:
        for row in info_table.select(selectors['author_row_selector']):
            cells = row.find_all('td')
            if len(cells) > 1 and cells[0].get_text(strip=True) == selectors['author_label']:
                author = cells[1].get_text(strip=True)
                break

    # Attempt to find the cover image from meta tags
    cover_url = None
    meta_tag = soup.find('meta', property=selectors['cover_meta_property'])
    if meta_tag and 'content' in meta_tag.attrs:
        cover_url = meta_tag['content']
    else:
        meta_tag = soup.find('meta', property=selectors['cover_meta_secure_property'])
        if meta_tag and 'content' in meta_tag.attrs:
            cover_url = meta_tag['content']

    # Fall back to finding the cover image from bigcover and bigbanner
    if not cover_url:
        cover_div = soup.select_one(selectors['cover_div_selector'])
        if cover_div:
            cover_url = re.search(r"url\('(.+?)'\)", cover_div['style']).group(1)

    return description, author, cover_url


async def parse_chapter_page(html, selectors):
    soup = BeautifulSoup(html, 'html.parser')
    images = []
    for img in soup.select(selectors['image_selector']):
        if 'data-src' in img.attrs:
            images.append(img['data-src'])
    return images
