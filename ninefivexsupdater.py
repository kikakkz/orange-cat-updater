# coding=utf-8

import random
import requests
import time
from urlupdater import UrlUpdater
from logger import Logger
from bs4 import BeautifulSoup
import re
from book import Book
from chapter import Chapter


class NineFiveXSUpdater(UrlUpdater):
    def __init__(self, url):
        super(NineFiveXSUpdater, self).__init__(url)
        self.books_list_page = url.books_list_page()

    def construct_main_request_url(self):
        return '{}/{}/{}.html'.format(self.url, self.books_list_page, self.cur_page)

    def reliable_update_book(self, book):
        retries = 3
        while True:
            time.sleep(3)
            rc = self.update_book(book)
            if rc is True:
                return True
            retries -= 1
            if 0 < retries:
                continue
            return False

    def get_chapters_table(self, parser, book):
        cons = parser.find_all('div', id='container')
        chmain = None
        for con in cons:
            mains = con.find_all('div', id='main')
            for main in mains:
                booklists = main.find_all(class_='title', id='alllist')
                if 0 < len(booklists):
                    chmain = main
                    break
            if chmain is not None:
                break

        if chmain is None:
            return

        chs = chmain.find_all('dl', class_='chapterlist')
        chapters = []
        chapter_index = 1
        for ch in chs:
            dds = ch.find_all('dd')
            for dd in dds:
                title = dd.get_text(strip=True)
                url = None
                aas = dd.find_all('a')
                for a in aas:
                    if a.get('href') is not None:
                        url = '{}/{}' . format(book.book_native_id().replace('_', '/'), a.get('href'))
                cid = None
                if url is not None:
                    cid = url.replace('.html', '').replace('/', '_')
                    url = self.url + '/' + url
                chapter = Chapter(cid, url, title, False, chapter_index)
                chapters.append(chapter)
                chapter_index += 1

        self.add_book_chapters(book, chapters)

    def update_book(self, book):
        req_url = '{}/{}/' . format(self.url, book.book_native_id().replace('_', '/'))
        try:
            Logger.debug(' > {}' . format(req_url))
            resp = requests.get(req_url, timeout=3)
            Logger.debug(' < {}[{}]' . format(req_url, resp.status_code))
        except Exception as e:
            Logger.error(' xxx {}[{}]' . format(req_url, e))
            return False

        parser = BeautifulSoup(resp.content, 'html.parser')
        book_root_tags = parser.find_all('div', id=self.book_root_class)
        for tag in book_root_tags:
            pattern = re.compile('字数：([0-9]+)')
            matches = pattern.findall(tag.get_text(strip=True))
            if 0 < len(matches):
                book.set_attr('total_chars', matches[0])
            abbs = tag.find_all(class_='book-intro')
            for abb in abbs:
                book.set_attr('abbreviation', abb.get_text(strip=True))

        book.set_attr('author_avatar', '')
        total_reads = random.randint(1000, 10000)
        book.set_attr('total_reads', '{}' . format(total_reads))
        total_searchs = random.randint(10000, 20000)
        book.set_attr('total_searches', '{}' . format(total_searchs)),
        total_votes = random.randint(500, 1000)
        book.set_attr('total_votes', '{}' . format(total_votes))
        score = random.randint(10, 100)
        book.set_attr('score', '{}' . format(score))

        self.get_chapters_table(parser, book)
        return True

    def find_max_pages(self, parser):
        if -1 != self.max_pages:
            return
        maxpage_divs = parser.find_all('div', class_=self.books_list_maxpage_class)
        for div in maxpage_divs:
            tags = div.find_all(self.books_list_maxpage_div_tag)
            for tag in tags:
                tag_str = str(tag)
                pattern = re.compile(self.books_list_maxpage_value_pattern)
                rc = pattern.findall(tag_str)
                if 0 < len(rc):
                    self.max_pages = int(rc[0])

    def parse_book(self, tag):
        book_id = None
        titles = tag.find_all('h3')
        for t in titles:
            aas = t.find_all('a')
            for a in aas:
                if a.get('href') is not None:
                    pattern = re.compile('/([0-9]+)/([0-9]+)/')
                    text = a.get('href')
                    matches = pattern.findall(text)
                    if 0 < len(matches) and 2 == len(matches[0]):
                        book_id = matches[0][0] + '_' + matches[0][1]

        if book_id is None:
            return

        book = Book(book_id, self.host_to_books_table_name(self.url))
        for t in titles:
            aas = t.find_all('a')
            for a in aas:
                book.set_attr('name', a.get_text(strip=True))
            ups = t.find_all(class_='uptime')
            for up in ups:
                book.set_attr('last_update', up.get_text(strip=True))

        dts = tag.find_all('dt')
        for dt in dts:
            aas = dt.find_all('a')
            for a in aas:
                imgs = a.find_all('img')
                for img in imgs:
                    book.set_attr('cover', img.get('src'))

        others = tag.find_all(class_='book_other')
        for other in others:
            cs = other.get_text(strip=True)
            pattern = re.compile('作者：(.*)状态：(.*)类别：(.*)')
            matches = pattern.findall(cs)
            if 0 < len(matches) and 0 < len(matches[0]):
                book.set_attr('author', matches[0][0])
                book.set_attr('status', matches[0][1])
                book.set_attr('class', matches[0][2])
            if '最新章节' in cs:
                chs = other.find_all('a')
                for ch in chs:
                    book.set_attr('last_chapter', ch.get_text(strip=True))
                    if ch.get('href') is not None:
                        book.set_attr('last_chapter_url', ch.get('href'))

        if book is not None:
            return self.reliable_update_book(book)

    def parse(self, resp):
        parser = BeautifulSoup(resp.content, 'html.parser')
        self.find_max_pages(parser)
        Logger.debug('Total books list pages {},{}' . format(self.max_pages, self.cur_page))

        books_root_tags = parser.find_all('div', class_=self.books_root_class)
        books_list_tags = []
        for tag in books_root_tags:
            books_list_tags = tag.find_all('div', id=self.books_list_class)
        for tag in books_list_tags:
            tags = tag.find_all(self.books_item_tag)
            for book_tag in tags:
                self.parse_book(book_tag)
