# coding=utf-8

import re
import random
from book import Book
from chapter import Chapter
from logger import Logger
import requests
from bs4 import BeautifulSoup
import time
from urlupdater import UrlUpdater


class HaoshuUrlUpdater(UrlUpdater):
    def __init__(self, url):
        super(HaoshuUrlUpdater, self).__init__(url)

        self.books_page_param = url.books_page_param()
        self.books_list_page = url.books_list_page()
        self.books_list_maxpage_tag_pattern = url.books_list_maxpage_tag_pattern()
        self.book_id_pattern = url.book_id_pattern()
        self.book_info_page = url.book_info_page()
        self.book_info_param = url.book_info_param()
        self.book_chapter_list_page = url.book_chapter_list_page()
        self.book_chapter_list_param = url.book_chapter_list_param()
        self.book_status_class = url.book_status_class()
        self.book_author_class = url.book_author_class()
        self.book_author_name_class = url.book_author_name_class()
        self.book_author_name_tag = url.book_auto_name_tag()
        self.book_cover_class = url.book_cover_class()
        self.book_abbreviation_class = url.book_abbreviation_class()
        self.book_abbreviation_text_class = url.book_abbreviation_text_class()
        self.book_content_detail_class = url.book_content_detail_class()
        self.book_content_last_chapter_title_tag = url.book_content_last_chapter_title_tag()
        self.book_content_last_chapter_update_tag = url.book_content_last_chapter_update_tag()
        self.book_last_update_prefix = url.book_last_update_prefix()
        self.book_chars_cycle_after_name = url.book_chars_cycle_after_name()
        self.book_reads_cycle_after_name = url.book_reads_cycle_after_name()
        self.chapters_root_class = url.chapters_root_class()
        self.chapters_item_class = url.chapters_item_class()
        self.book_title_class = url.book_title_class()
        self.book_title_tag = url.book_title_tag()
        self.book_chapter_id_pattern = url.book_chapter_id_pattern()
        self.book_finished_mark = url.book_finished_mark()
        self.book_class_class = url.book_class_class()
        self.book_class_tag = url.book_class_tag()
        self.book_class_pattern = url.book_class_pattern()

    def get_chapters_table(self, book):
        req_url = self.url + '/' + self.book_chapter_list_page + '?' +\
                  self.book_chapter_list_param + book.book_native_id()
        try:
            Logger.debug(' > {}' . format(req_url))
            resp = requests.get(req_url, timeout=3)
            Logger.debug(' < {}[{}]' . format(req_url, resp.status_code))
        except Exception as e:
            Logger.error(' xxx {}[{}]' . format(req_url, e))
            return False

        parser = BeautifulSoup(resp.content, 'html.parser')
        chapters_root_tags = parser.find_all('div', class_=self.chapters_root_class)

        chapters = []
        chapter_index = 1

        for chapters_tag in chapters_root_tags:
            chapters_item_tags = chapters_tag.find_all(class_=self.chapters_item_class)
            for tag in chapters_item_tags:
                vip = False
                url = None
                title = None
                cid = '0'
                if tag.get('class') is not None and 'vip' in tag.get('class'):
                    vip = True
                if tag.a is not None and tag.a.get('href') is not None:
                    url = tag.a.get('href')
                if tag.a is not None and tag.a.span is not None:
                    title = tag.a.span.get_text(strip=True)
                    pattern = re.compile(self.book_chapter_id_pattern)
                    matches = pattern.findall(title)
                    if 0 < len(matches):
                        cid = str(matches[0])
                    else:
                        Logger.debug(title)
                chapter = Chapter(cid, url, title, vip, chapter_index)
                chapters.append(chapter)
                chapter_index += 1

        self.add_book_chapters(book, chapters)
        return True

    def update_book(self, book):
        req_url = self.url + '/' + self.book_info_page + "?" +\
                  self.book_info_param + book.book_native_id()
        try:
            Logger.debug(' > {}' . format(req_url))
            resp = requests.get(req_url, timeout=3)
            Logger.debug(' < {}[{}]' . format(req_url, resp.status_code))
        except Exception as e:
            Logger.error(' xxx {}[{}]' . format(req_url, e))
            return False

        parser = BeautifulSoup(resp.content, 'html.parser')
        book_root_tags = parser.find_all('div', class_=self.book_root_class)

        book_info_tags = []
        for tag in book_root_tags:
            book_info_tags = tag.find_all(class_=self.book_info_class)
        for tag in book_info_tags:
            status_tags = tag.find_all(class_=self.book_status_class)
            if 0 == len(status_tags):
                continue
            book.set_attr('status', status_tags[0].get_text(strip=True))
            break
        for tag in book_info_tags:
            author_tags = tag.find_all(class_=self.book_author_class)
            for atag in author_tags:
                if atag.img is not None:
                    book.set_attr('author_avatar', atag.img['src'])
                name_tags = atag.find_all(class_=self.book_author_name_class)
                for ntag in name_tags:
                    name = ntag.find_all(self.book_author_name_tag)
                    book.set_attr('author', '无名氏')
                    for n in name:
                        book.set_attr('author', n.get_text(strip=True))
        for tag in book_info_tags:
            cover_tags = tag.find_all(class_=self.book_cover_class)
            for ctag in cover_tags:
                if ctag.img is not None:
                    book.set_attr('cover', ctag.img['src'])
        for tag in book_info_tags:
            abbe_tags = tag.find_all(class_=self.book_abbreviation_class)
            for atag in abbe_tags:
                atext_tags = atag.find_all(class_=self.book_abbreviation_text_class)
                for attag in atext_tags:
                    book.set_attr('abbreviation', attag.get_text(strip=True))

        for tag in book_info_tags:
            detail_tags = tag.find_all(class_=self.book_content_detail_class)
            for dtag in detail_tags:
                ch_title_tags = dtag.find_all(self.book_content_last_chapter_title_tag)
                for chtag in ch_title_tags:
                    book.set_attr('last_chapter', chtag.get_text())
                ch_update_tags = dtag.find_all(self.book_content_last_chapter_update_tag)
                for chtag in ch_update_tags:
                    book.set_attr('last_update', chtag.get_text().replace(self.book_last_update_prefix, ''))
                if dtag.get('href') is not None:
                    book.set_attr('last_chapter_url', dtag['href'])

        for tag in book_info_tags:
            title_tags = tag.find_all(class_=self.book_title_class)
            for ttag in title_tags:
                h_title_tags = ttag.find_all(self.book_title_tag)
                for httag in h_title_tags:
                    book.set_attr('name', httag.get_text(strip=True))

        for tag in book_info_tags:
            class_tags = tag.find_all(class_=self.book_class_class)
            for ctag in class_tags:
                class_p_tags = ctag.find_all(self.book_class_tag)
                for cptag in class_p_tags:
                    text_str = cptag.get_text(strip=True)
                    pattern = re.compile(self.book_class_pattern)
                    matches = pattern.findall(text_str)
                    book.set_attr('class', '其他')
                    if 0 < len(matches):
                        book.set_attr('class', matches[0])

        total_searches = random.randint(10000, 20000)
        book.set_attr('total_searches', '{}' . format(total_searches)),
        total_votes = random.randint(500, 1000)
        book.set_attr('total_votes', '{}' . format(total_votes))
        score = random.randint(10, 100)
        book.set_attr('score', '{}' . format(score))

        return True

    def construct_main_request_url(self):
        return self.url + '/' + self.books_list_page + '?' + self.books_page_param + str(self.cur_page)

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

    def reliable_get_chapters(self, book):
        retries = 3
        while True:
            time.sleep(3)
            rc = self.get_chapters_table(book)
            if rc is True:
                return True
            retries -= 1
            if 0 < retries:
                continue
            return False

    def find_max_pages(self, parser):
        if -1 != self.max_pages:
            return
        maxpage_divs = parser.find_all('div', class_=self.books_list_maxpage_class)
        for div in maxpage_divs:
            tags = div.find_all(self.books_list_maxpage_div_tag)
            for tag in tags:
                tag_str = str(tag)
                pattern = re.compile(self.books_list_maxpage_tag_pattern)
                rc = pattern.findall(tag_str)
                if len(rc) is 0:
                    continue
                pattern = re.compile(self.books_list_maxpage_value_pattern)
                rc = pattern.findall(tag_str)
                if 0 < len(rc):
                    self.max_pages = int(rc[0])

    def parse_book(self, tag):
        tags = tag.find_all('td')
        book = None
        book_cycle = 0
        cur_cycle = 0
        for itag in tags:
            cur_cycle += 1
            pattern = re.compile(self.book_id_pattern)
            tag_str = str(itag)
            rc = pattern.findall(tag_str)
            if 0 < len(rc):
                book = Book(rc[0], self.host_to_books_table_name(self.url))
                book_cycle = cur_cycle
                continue
            if book is not None and cur_cycle == book_cycle + self.book_chars_cycle_after_name:
                chars = itag.get_text(strip=True)
                book.set_attr('total_chars', chars)
                continue
            if book is not None and cur_cycle == book_cycle + self.book_reads_cycle_after_name:
                reads = itag.get_text(strip=True)
                book.set_attr('total_reads', reads)
                continue

        if book is not None:
            rc = self.reliable_update_book(book)
            if rc is False:
                return False
            return self.reliable_get_chapters(book)

    def parse(self, resp):
        parser = BeautifulSoup(resp.content, 'html.parser')

        self.find_max_pages(parser)
        Logger.debug('Total books list pages {},{}' . format(self.max_pages, self.cur_page))

        books_root_tags = parser.find_all('div', class_=self.books_root_class)
        books_list_tags = []
        for tag in books_root_tags:
            books_list_tags = tag.find_all(class_=self.books_list_class)
        for tag in books_list_tags:
            tags = tag.find_all(self.books_item_tag)
            for book_tag in tags:
                self.parse_book(book_tag)
