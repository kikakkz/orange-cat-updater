import hashlib
import threading
from dbhelper import DBHelper
import requests
import time
from logger import Logger


class UrlUpdater(threading.Thread):
    def __init__(self, url):
        super(UrlUpdater, self).__init__()

        self.url = url.url_location()
        self.url_class = url.url_class()
        self.cur_page = url.books_list_start_page()
        self.books_root_class = url.books_root_class()
        self.books_list_class = url.books_list_class()
        self.books_item_tag = url.books_item_tag()
        self.books_list_maxpage_value_pattern = url.books_list_maxpage_value_pattern()
        self.books_list_maxpage_class = url.books_list_maxpage_class()
        self.books_list_maxpage_div_tag = url.books_list_maxpage_div_tag()
        self.book_root_class = url.book_root_class()
        self.book_info_class = url.book_info_class()
        self.books_gender = url.books_gender()

        self.max_pages = -1

        self.books_table_prefix = url.books_table_prefix()
        self.table_name = self.books_table_prefix + '_books'
        self.db = DBHelper.instance()
        self.books_table_name = self.host_to_books_table_name(self.url)
        self.db.create_host_books_table(self.books_table_name)

    def add_book_mysql(self, book):
        self.db.add_book_to_table(book)

    @classmethod
    def book_chapter_table_name(cls, book):
        sha256 = hashlib.sha256()
        sha256.update((book.get_attr('name') + book.get_attr('author')).encode('utf-8'))
        tbl = sha256.hexdigest()
        return tbl

    @classmethod
    def host_to_books_table_name(cls, host):
        return host.replace('http://', '').replace('https://', '').replace('www.', '').replace('.', '_') + '_books'

    def create_book_chapters(self, book):
        tbl = self.book_chapter_table_name(book)
        success, _ = self.db.create_book_chapters_table(tbl)
        return success

    def add_book_chapters(self, book, chapters):
        # Only add free chapter
        for chapter in chapters:
            if chapter.chapter_vip():
                return

        chapter_table_name = self.book_chapter_table_name(book)
        success, res = self.db.query_book_in_host_books_table(self.books_table_name, chapter_table_name)
        if success is False or 0 == len(res) or 0 == len(res[0]) or chapter_table_name not in res[0]:
            rc = self.create_book_chapters(book)
            if rc is False:
                return

        self.db.add_book_to_host_books_table(self.books_table_name, chapter_table_name)

        for chapter in chapters:
            self.add_book_chapter(book, chapter)
        book.set_attr('with_vip_chapter', False)
        book.set_attr('gender', self.books_gender)

        self.add_book_mysql(book)
        # self.update_book_attr_key(book)

    def add_book_chapter(self, book, chapter):
        tbl = self.book_chapter_table_name(book)
        self.db.add_chapter_to_book(tbl, chapter)

    def update_book_attr_key(self, book):
        key = self.books_table_prefix + '_' + book.book_id()
        self.db.update_book_info_cache(key, book)

    def construct_main_request_url(self):
        return self.url.url_location()

    def parse(self, resp):
        pass

    def run(self):
        while True:
            req_url = self.construct_main_request_url()
            Logger.debug(' > {}' . format(req_url))
            try:
                resp = requests.get(req_url, timeout=3)
                Logger.debug(' < {}[{}]' . format(req_url, resp.status_code))
                if 200 != resp.status_code:
                    return
                self.parse(resp)
                Logger.debug('... {}' . format(req_url))

                if self.cur_page < self.max_pages:
                    self.cur_page += 1
                else:
                    break
            except Exception as e:
                Logger.error(' *** {}[{}]' . format(req_url, e))

            time.sleep(3)

