import csv
import json
from pathlib import Path

from src import config
from src.models import Movie


class Storage:
    """数据存储类：支持保存 CSV 和 JSON。"""

    def __init__(self):
        config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def save_csv(self, movies: list[Movie], file_path: Path | None = None) -> Path:
        """
        保存电影数据到 CSV。

        Args:
            movies: 电影对象列表
            file_path: 自定义输出路径；为空则使用 config.CSV_FILE_PATH

        Returns:
            Path: 实际保存路径
        """
        path = file_path or config.CSV_FILE_PATH
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", newline="", encoding=config.CSV_ENCODING) as f:
            # 先写一下csv的头
            writer = csv.DictWriter(f, fieldnames=config.CSV_FIELDS)
            writer.writeheader()

            # 现在写一下csv的内容
            for movie in movies:
                # 把movie从Movie对象变成dict对象
                row = movie.to_dict()
                # 只写配置声明中的字段, 避免字段漂移
                normalized_row = {
                    field: row.get(field, "") for field in config.CSV_FIELDS
                }

                # list 字段转成字符串，CSV 更好读
                # 例如 Director: ["A", "B"] -> "A / B"
                for key in ("Director", "Actor", "Country"):
                    value = normalized_row.get(key)
                    if isinstance(value, list):
                        normalized_row[key] = "/".join(map(str, value))

                # quote可能是None, 直接写成空串
                if normalized_row.get("quote") is None:
                    normalized_row["quote"] = ""

                writer.writerow(normalized_row)
        return path

    def save_json(self, movies: list[Movie], file_path: Path | None = None) -> Path:
        """
        保存电影数据到 JSON（调试与二次处理更方便）。

        Args:
            movies: 电影对象列表
            file_path: 自定义输出路径；为空则使用 config.JSON_FILE_PATH

        Returns:
            Path: 实际保存路径
        """
        # 这里要使用 JSON 路径，而不是 CSV 路径
        path = file_path or config.JSON_FILE_PATH
        # mkdir 应该作用于父目录，不能对文件路径本身调用
        path.parent.mkdir(parents=True, exist_ok=True)

        # 把数据从Movie变成dict
        data = [movie.to_dict() for movie in movies]
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return path
