import re

from bs4 import BeautifulSoup


def parse_manga_list_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    manga_links = []
    for link in soup.select('a.series.tip'):
        manga_links.append((link['href'], link.get_text()))
    return manga_links


def parse_manga_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    chapters = []
    for chapter in soup.select('.eph-num a'):
        chapters.append(chapter['href'])
    return chapters


def parse_manga_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    description = soup.select_one('.entry-content.entry-content-single[itemprop="description"]').get_text(strip=True)

    # Find the author from the table
    author = 'Unknown'
    info_table = soup.select_one('table.infotable')
    if info_table:
        for row in info_table.select('tr'):
            cells = row.find_all('td')
            if len(cells) > 1 and cells[0].get_text(strip=True) == 'Author':
                author = cells[1].get_text(strip=True)
                break

    # Attempt to find the cover image from meta tags
    cover_url = None
    meta_tag = soup.find('meta', property='og:image')
    if meta_tag and 'content' in meta_tag.attrs:
        cover_url = meta_tag['content']
    else:
        meta_tag = soup.find('meta', property='og:image:secure_url')
        if meta_tag and 'content' in meta_tag.attrs:
            cover_url = meta_tag['content']

    # Fall back to finding the cover image from bigcover and bigbanner
    if not cover_url:
        cover_div = soup.select_one('.bigcover .bigbanner')
        if cover_div:
            cover_url = re.search(r"url\('(.+?)'\)", cover_div['style']).group(1)

    return description, author, cover_url


async def parse_chapter_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    images = []
    for img in soup.select('img'):
        if 'data-src' in img.attrs:
            images.append(img['data-src'])
    return images
