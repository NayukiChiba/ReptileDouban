"""
parser.py
负载把爬取到的HTML解析成Movie对象列表
"""

import re

from bs4 import BeautifulSoup

import config
from models import Movie


class Parser:
    """
    页面解析类，负责把爬取到的HTML解析成Movie对象列表
    """

    @staticmethod
    def _safe_text(node, sep: str = "") -> str:
        """
        安全取文本, 如果节点不存在就返回空字符串
        """
        if node is None:
            return ""
        return node.get_text(sep, strip=True)

    @staticmethod
    def _extract_votes(star_text: str) -> int:
        """从类似 '9.7 1234567人评价' 文本中提取评价人数。"""
        m = re.search(r"(\d+)人评价", star_text)
        return int(m.group(1)) if m else 0

    @staticmethod
    def _extract_people_info(
        info_text: str,
    ) -> tuple[list[str], list[str], str, list[str]]:
        """
        从 p 信息中提取 导演/演员/年份/国家。
        对结构变化做了尽量宽松的兜底。
        """

        # 默认值
        directors: list[str] = []
        actors: list[str] = []
        release_year = ""
        countries: list[str] = []

        # 提取“导演/主演”行
        # 常见格式：导演: xxx 主演: yyy
        line1 = info_text

        directors_match = re.search(r"导演:\s*([^\n\r]+?)(?=\s+主演:|$)", line1)

        if directors_match:
            directors = [
                x.strip() for x in directors_match.group(1).split("/") if x.strip()
            ]

        actor_match = re.search(r"主演:\s*([^\n\r]+?)(?=\s+\d{4}|$)", line1)

        if actor_match:
            actors = [x.strip() for x in actor_match.group(1).split("/") if x.strip()]

        # 提取“年份 / 国家 / 类型”中的年份和国家
        # 常见片段：1994 / 美国 / 犯罪 剧情
        year_match = re.search(r"(19\d{2}|20\d{2})", info_text)
        if year_match:
            release_year = year_match.group(1)

        # 按 '/' 切分后，用位置近似法拿国家
        parts = [p.strip() for p in info_text.split("/") if p.strip()]

        if parts:
            # 找到年份所在片段后，下一段通常是国家
            year_idx = -1
            for i, p in enumerate(parts):
                if re.search(r"(19\d{2}|20\d{2})", p):
                    year_idx = i
                    break
            if 0 <= year_idx < len(parts) - 1:
                # 国家可能有多个，以空格分割会误伤，因此先按“·”与逗号再切
                raw_country = parts[year_idx + 1]
                tmp = re.split(r"[、,，·]", raw_country)
                countries = [c.strip() for c in tmp if c.strip()]

        return directors, actors, release_year, countries

    def parse_page(self, html: str) -> list[Movie]:
        """
        解析单页html
        Args:
            html(str): 页面的html文本
        Returns:
            list[Movie]: 该页的电影列表, 25条
        """
        soup = BeautifulSoup(html, config.PARSER)
        items = soup.select("ol.grid_view li")

        movies: list[Movie] = []
        for item in items:
            # 1) 排名
            rank_text = self._safe_text(item.select_one("em"))
            rank = int(rank_text) if rank_text.isdigit() else 0

            # 2) 片名（主片名）
            title = self._safe_text(item.select_one("span.title"))

            # 3) 链接
            link_node = item.select_one("div.pic a")
            detail_url = link_node.get("href", "") if link_node else ""

            # 4) 评分
            rating_text = self._safe_text(item.select_one("span.rating_num"))
            try:
                rating = float(rating_text)
            except ValueError:
                rating = 0.0

            # 5) 评价人数（从 "xxxx人评价" 提取）
            star_text = self._safe_text(item.select_one("div.star"), sep=" ")
            votes = self._extract_votes(star_text)

            # 6) 短评（可能没有）
            quote = self._safe_text(item.select_one("span.inq")) or None

            # 7) 可播放标记（若页面存在可播放标记）
            is_playable = bool(item.select_one("span.playable"))

            # 8) 导演 / 演员 / 年份 / 国家
            #    豆瓣常见结构：
            #    p 标签第一行：导演、主演
            #    p 标签第二行：年份 / 国家 / 类型
            p_node = item.select_one("div.bd p")
            info_text = self._safe_text(p_node, sep=" ")
            director, actor, release_year, country = self._extract_people_info(
                info_text
            )

            movies.append(
                Movie(
                    rank=rank,
                    title=title,
                    Director=director,
                    Actor=actor,
                    ReleaseYear=release_year,
                    Country=country,
                    rating=rating,
                    votes=votes,
                    detail_url=detail_url,
                    quote=quote,
                    isPlayable=is_playable,
                )
            )

        return movies

    def parse_pages(self, pages_html: list[str]) -> list[Movie]:
        """解析多页 HTML 并合并结果。"""
        all_movies: list[Movie] = []
        for html in pages_html:
            all_movies.extend(self.parse_page(html))
        return all_movies
