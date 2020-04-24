import hashlib

from mysqlcli import MysqlCli
from rediscli import RedisCli
import json


class DBHelper:
    instance_ = None

    def __init__(self):
        self.mysql = MysqlCli.instance()
        self.redis = RedisCli.instance()
        self.create_book_table()

    @classmethod
    def initialize(cls):
        if DBHelper.instance_ is None:
            DBHelper.instance_ = DBHelper()

    @classmethod
    def instance(cls):
        return DBHelper.instance_

    def create_book_table(self):
        sql = 'create table if not exists `books_table` ('
        sql += 'id char(32),'
        sql += 'name char(64) not null,'
        sql += 'abbreviation text(512) not null,'
        sql += 'author char(16) not null,'
        sql += 'cover text(512) not null,'
        sql += 'author_avatar text(512) not null,'
        sql += 'finished boolean,'
        sql += 'total_reads int,'
        sql += 'total_chars int,'
        sql += 'last_update_time char(32),'
        sql += 'class char(16),'
        sql += 'total_searches int,'
        sql += 'total_votes int,'
        sql += 'last_chapter_title char(64),'
        sql += 'last_chapter_url text(512),'
        sql += 'with_vip_chapter boolean,'
        sql += 'gender char(16),'
        sql += 'score int,'
        sql += 'primary key (name, author)'
        sql += ') row_format=dynamic charset=utf8'
        return self.mysql.exec(sql)

    def add_book_to_table(self, book, book_finished_mark='完结'):
        sql = 'insert into `books_table` ('
        sql += 'id, name, abbreviation, author, cover, author_avatar, finished, '
        sql += 'total_reads, total_chars, last_update_time, class, total_searches, '
        sql += 'total_votes, last_chapter_title, last_chapter_url, with_vip_chapter, '
        sql += 'gender, score) values ('
        sql += '\'' + book.book_id() + '\',\'' + book.get_attr('name') + '\','
        sql += '\'' + book.get_attr('abbreviation') + '\',\'' + book.get_attr('author') + '\','
        sql += '\'' + book.get_attr('cover') + '\',\'' + book.get_attr('author_avatar') + '\','
        sql += '\'' + str(int((book_finished_mark in book.get_attr('status')))) + '\','
        sql += '\'' + book.get_attr('total_reads') + '\',\'' + book.get_attr('total_chars') + '\','
        sql += '\'' + book.get_attr('last_update') + '\',\'' + book.get_attr('class') + '\','
        sql += '\'' + book.get_attr('total_searches') + '\', \'' + book.get_attr('total_votes') + '\','
        sql += '\'' + book.get_attr('last_chapter') + '\',\'' + book.get_attr('last_chapter_url') + '\','
        sql += '\'' + str(int(book.get_attr('with_vip_chapter'))) + '\',\'' + book.get_attr('gender') + '\','
        sql += '\'' + str(book.get_attr('score')) + '\')'
        return self.mysql.exec(sql)

    def create_host_books_table(self, table_name):
        sql = 'create table if not exists `' + table_name + '` ('
        sql += 'book_hash char(128), primary key (book_hash)'
        sql += ') charset=utf8'
        return self.mysql.exec(sql)

    def add_book_to_host_books_table(self, table_name, book_hash):
        sql = 'insert into `' + table_name + '` ('
        sql += 'book_hash'
        sql += ') values ('
        sql += '\'' + book_hash + '\''
        sql += ')'
        return self.mysql.exec(sql)

    def query_book_in_host_books_table(self, table_name, book_hash):
        sql = 'select book_hash from `' + table_name + '` where book_hash=\'' + book_hash + '\''
        return self.mysql.exec(sql)

    def create_book_chapters_table(self, table_name):
        sql = 'create table if not exists `' + table_name + '` ('
        sql += 'native_id int,'
        sql += 'id char(255),'
        sql += 'title char(128),'
        sql += 'url text(512),'
        sql += 'vip boolean,'
        sql += 'primary key (native_id)'
        sql += ') charset=utf8'
        return self.mysql.exec(sql)

    def add_chapter_to_book(self, table_name, chapter):
        sql = 'insert into `' + table_name + '` ('
        sql += 'id, url, title, vip, native_id'
        sql += ') values ('
        sql += '\'' + chapter.chapter_title() + '\',\'' + chapter.chapter_url() + '\','
        sql += '\'' + chapter.chapter_title() + '\',\'' + str(int(chapter.chapter_vip())) + '\','
        sql += str(chapter.chapter_index()) + ')'
        return self.mysql.exec(sql)

    def update_book_info_cache(self, key, book, book_finished_mark='完结'):
        val = {
            'finished': book_finished_mark in book.get_attr('status'),
            'total_chars': book.get_attr('total_chars'),
            'total_reads': book.get_attr('total_reads'),
            'last_update': book.get_attr('last_update'),
            'last_chapter': book.get_attr('last_chapter'),
            'last_chapter_url': book.get_attr('last_chapter_url')
        }
        self.redis.set(key, json.dumps(val))

