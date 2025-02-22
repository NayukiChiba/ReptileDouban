from typing import Optional
from dataclasses import dataclass, field

@dataclass
class Movie:
    rank: int                      # 排名
    title: str                     # 片名
    Director: list[str]            # 导演
    Actor: list[str]               # 演员
    ReleaseYear: str               # 上映年份
    Country: list[str]             # 国家
    rating: float                  # 评分
    votes: int                     # 评价人数
    detail_url: str                # 详情页链接
    quote: Optional[str] = None    # 短评, 可能为空
    isPlayable: bool = False       # 是否可播放

    def to_dict(self) -> dict:
        """把Movie对象转换成字典, 方便序列化和存储"""
        return {
            "rank": self.rank,
            "title": self.title,
            "isPlayable": self.isPlayable,
            "Director": self.Director,
            "Actor": self.Actor,
            "ReleaseYear": self.ReleaseYear,
            "Country": self.Country,
            "rating": self.rating,
            "votes": self.votes,
            "detail_url": self.detail_url,
            "quote": self.quote,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Movie":
        """从字典创建Movie对象的工厂方法"""
        return cls(
            rank=int(data["rank"]),
            title=data["title"],
            isPlayable=data.get("isPlayable", False),
            Director=data["Director"],
            Actor=data["Actor"],
            ReleaseYear=data["ReleaseYear"],
            Country=data["Country"],
            rating=float(data["rating"]),
            votes=int(data["votes"]),
            detail_url=data["detail_url"],
            quote=str(data.get("quote", "")),
        )
    

