"""
src 包公共导出入口
只暴露外部会稳定使用的类，隐藏内部实现细节。
"""

from .crawler import Crawler
from .models import Movie
from .parser import Parser
from .service import DoubanTop250Service
from .storage import Storage

__all__ = [
    "Movie",
    "Crawler",
    "Parser",
    "Storage",
    "DoubanTop250Service",
]
