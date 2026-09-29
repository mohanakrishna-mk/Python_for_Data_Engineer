import logging

from database import create_tables


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    create_tables()

    print("Expense Manager started")


if __name__ == "__main__":
    main()