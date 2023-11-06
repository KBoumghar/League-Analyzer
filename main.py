from utility import *


def main():
    API_KEY = get_api_key("API.in")
    PATH_DB_URL = get_path_db()

    create_summoner_to_id_table(API_KEY, PATH_DB_URL, tier="Master")


if __name__ == "__main__":
    main()
