"""
config.py
配置文件
"""
# 豆瓣top250的url
BASE_URL = "https://movie.douban.com/top250"

# 豆瓣电影一共250条
# 一共10页, 每一页25个电影
TOTAL_ITEMS: int = 250
PAGE_SIZE = 25

# 请求头
HEADERS: dict[str, str] = {
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://movie.douban.com/",
    "Sec-Ch-Ua": "'Not:A-Brand';v='99', 'Google Chrome';v='145', 'Chromium';v='145'",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "'Windows'",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
  }

# 超时时间
REQUEST_TIMEOUT: int = 15

# 重试和限速
MAX_RETRIES: int = 3

# 重试间隔基础值（秒）
# - 可结合指数退避：sleep(RETRY_BACKOFF_BASE * (2 ** retry_idx))
RETRY_BACKOFF_BASE: float = 1.0

# 每页请求之间的随机等待区间（秒）
# - 用于降低请求频率，减少触发风控概率
SLEEP_MIN_SECONDS: float = 1.0
SLEEP_MAX_SECONDS: float = 2.5

# 解析和存储
# HTML解析
PARSER: str = "lxml"
# CSV 编码：utf-8-sig 可让 Windows Excel 打开中文更友好
CSV_ENCODING: str = "utf-8-sig"

# CSV 列顺序（建议固定，便于后续分析）
CSV_FIELDS: list[str] = [
    "rank",        # 排名
    "title",       # 片名
    "isPlayable",  # 是否可播放
    "Director",    # 导演
    "Actor",       # 演员
    "ReleaseYear", # 上映年份
    "Country",     # 国家
    "rating",      # 评分
    "votes",       # 评价人数
    "detail_url",  # 详情页链接
    "quote",       # 短评（可能为空）
]