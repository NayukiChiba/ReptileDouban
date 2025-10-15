from src.service import DoubanTop250Service


def main() -> None:
    service = DoubanTop250Service()
    service.run(save_csv=True, save_json=False)


if __name__ == "__main__":
    main()
