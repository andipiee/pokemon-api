import logging
from db_setup import DatabaseManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    db_manager = DatabaseManager()


if __name__ == "__main__":
    main()