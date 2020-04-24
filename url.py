from config import UrlJSON


class Url:
    def __init__(self, url):
        self.url = UrlJSON(url)
        self.chapterStartTag = ''
        self.chapterEndTag = ''

    def url_location(self):
        return self.url.root_url()

    def root_pages(self):
        return self.url.root_pages()

    def books_list_start_page(self):
        return self.url.books_list_start_page()

    def books_root_class(self):
        return self.url.books_root_class()

    def books_list_class(self):
        return self.url.books_list_class()

    def books_page_param(self):
        return self.url.books_page_param()

    def books_list_page(self):
        return self.url.books_list_page()

    def books_list_maxpage_tag_pattern(self):
        return self.url.books_list_maxpage_tag_pattern()

    def books_list_maxpage_value_pattern(self):
        return self.url.books_list_maxpage_value_pattern()

    def books_list_maxpage_class(self):
        return self.url.books_list_maxpage_class()

    def books_list_maxpage_div_tag(self):
        return self.url.books_list_maxpage_div_tag()

    def book_id_pattern(self):
        return self.url.book_id_pattern()

    def book_info_page(self):
        return self.url.book_info_page()

    def book_info_param(self):
        return self.url.book_info_param()

    def book_chapter_list_page(self):
        return self.url.book_chapter_list_page()

    def book_chapter_list_param(self):
        return self.url.book_chapter_list_param()

    def book_root_class(self):
        return self.url.book_root_class()

    def book_info_class(self):
        return self.url.book_info_class()

    def book_status_class(self):
        return self.url.book_status_class()

    def book_author_class(self):
        return self.url.book_author_class()

    def book_author_name_class(self):
        return self.url.book_author_name_class()

    def book_auto_name_tag(self):
        return self.url.book_auto_name_tag()

    def book_cover_class(self):
        return self.url.book_cover_class()

    def book_abbreviation_class(self):
        return self.url.book_abbreviation_class()

    def book_abbreviation_text_class(self):
        return self.url.book_abbreviation_text_class()

    def book_content_detail_class(self):
        return self.url.book_content_detail_class()

    def book_content_last_chapter_title_tag(self):
        return self.url.book_content_last_chapter_title_tag()

    def book_content_last_chapter_update_tag(self):
        return self.url.book_content_last_chapter_update_tag()

    def book_chapter_vip_class(self):
        return self.url.book_chapter_vip_class()

    def book_last_update_prefix(self):
        return self.url.book_last_update_prefix()

    def book_chars_cycle_after_name(self):
        return self.url.book_chars_cycle_after_name()

    def book_reads_cycle_after_name(self):
        return self.url.book_reads_cycle_after_name()

    def chapters_root_class(self):
        return self.url.chapters_root_class()

    def chapters_item_class(self):
        return self.url.chapters_item_class()

    def book_title_class(self):
        return self.url.book_title_class()

    def book_title_tag(self):
        return self.url.book_title_tag()

    def books_table_prefix(self):
        return self.url.books_table_prefix()

    def book_chapter_id_pattern(self):
        return self.url.book_chapter_id_pattern()

    def book_finished_mark(self):
        return self.url.book_finished_mark()

    def url_enable(self):
        return self.url.url_enable()

    def book_class_class(self):
        return self.url.book_class_class()

    def book_class_tag(self):
        return self.url.book_class_tag()

    def book_class_pattern(self):
        return self.url.book_class_pattern()

    def url_class(self):
        return self.url.url_class()

    def books_item_tag(self):
        return self.url.books_item_tag()

    def books_gender(self):
        return self.url.books_gender()
