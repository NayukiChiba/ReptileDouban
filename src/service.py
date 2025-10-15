"""
service.py
业务编排层：
1) 调用 crawler 抓取 HTML
2) 调用 parser 解析为 Movie
3) 调用 storage 落盘保存
"""

from __future__ import annotations

from src.crawler import Crawler
from src.parser import Parser
from src.storage import Storage


class DoubanTop250Service:
    """豆瓣 Top250 业务服务类。"""

    def __init__(self) -> None:
        self.crawler = Crawler()
        self.parser = Parser()
        self.storage = Storage()

    def run(self, save_csv: bool = True, save_json: bool = False) -> list:
        """
        执行完整流程：抓取 -> 解析 -> 保存。

        Args:
            save_csv: 是否保存 CSV
            save_json: 是否保存 JSON

        Returns:
            list: 解析得到的 Movie 列表
        """
        # 1) 抓取所有分页 HTML
        pages_html = self.crawler.crawl()

        # 2) 解析为 Movie 对象列表
        movies = self.parser.parse_pages(pages_html)

        # 3) 落盘
        if save_csv:
            csv_path = self.storage.save_csv(movies)
            print(f"CSV 已保存: {csv_path}")

        if save_json:
            json_path = self.storage.save_json(movies)
            print(f"JSON 已保存: {json_path}")

        print(f"完成，共解析 {len(movies)} 条电影数据")
        return movies

    def crawl_and_parse_only(self) -> list:
        """只抓取和解析，不保存文件（调试时常用）。"""
        pages_html = self.crawler.crawl()
        movies = self.parser.parse_pages(pages_html)
        return movies
