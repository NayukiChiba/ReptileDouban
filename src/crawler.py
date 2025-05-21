"""
crawler.py
爬虫模块
"""

import random
import time

import requests

import config


class Crawler:
    """
    爬虫类，负责爬取豆瓣电影Top250的数据
    """

    def __init__(self):
        # 使用requests.Session来复用TCP连接，提高效率
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)

    def fetch_page(self, start: int) -> str:
        """
        fetch单页HTML
        Args:
            start: int - 页码对应的start参数值
        Returns:
            str - 页面HTML文本
        """
        params = {"start": start}
        # 重试机制
        last_error: Exception | None = None
        # 总尝试次数 = 1（初始请求） + MAX_RETRIES（重试次数）
        for attempt in range(config.MAX_RETRIES + 1):
            try:
                # 发送GET请求
                resp = self.session.get(
                    config.BASE_URL,
                    params=params,
                    timeout=config.REQUEST_TIMEOUT,
                )
                # 非2xx状态码视为失败
                resp.raise_for_status()
                resp.encoding = resp.apparent_encoding  # 自动检测编码, 避免乱码
                return resp.text
            except requests.RequestException as e:
                last_error = e
                # 如果还有重试机会, 指数退避 + 随机等待
                if attempt < config.MAX_RETRIES:
                    wait_time = config.RETRY_BACKOFF_BASE * (
                        2**attempt
                    ) + random.uniform(
                        config.SLEEP_MIN_SECONDS, config.SLEEP_MAX_SECONDS
                    )
                    time.sleep(wait_time)
                    continue

                # 重试用尽仍失败, 抛出最后一个错误
                raise RuntimeError(
                    f"请求失败: start={start}, retries={config.MAX_RETRIES}"
                ) from last_error

    def crawl(self) -> list[str]:
        """
        爬取所有页面的HTML
        Returns:
            list[str] - 每个元素是一个页面的HTML文本
        """
        pages_html: list[str] = []

        for start in config.START:
            try:
                html = self.fetch_page(start)
                pages_html.append(html)
                # 限速一下, 避免过快请求触发风控
                delay = random.uniform(
                    config.SLEEP_MIN_SECONDS, config.SLEEP_MAX_SECONDS
                )
                time.sleep(delay)  # 请求间随机等待, 模拟人类行为
            except Exception as e:
                print(f"错误: 无法获取start={start}的页面, 错误信息: {e}")
                # 继续爬取下一页, 不让单页失败影响整体爬取
                continue
        return pages_html
