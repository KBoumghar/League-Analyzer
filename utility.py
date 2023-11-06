"""
Author: Karim Boumghar
Date: 5 November 2023

Description:
This module, named "utility.py," provides a collection of utility functions and data structures for working with the Riot Games API data and SQLite databases. These functions allow users to manage API keys, create database connections, perform database operations, and generate API URLs based on region and tier.

Please note that this module assumes the use of a personal API key from Riot Games.

Table of Contents:
1. Global Variables
2. API Key Management
3. Database Operations
4. URL Generation

1. Global Variables:
- DB_URL (str): The path to the SQLite database file.
- region_dict (dict): A dictionary that maps region codes to their respective API URLs.
- division_dict (dict): A dictionary that maps division codes to their corresponding Roman numerals.
- tier_set (set): A set containing valid League of Legends tiers.
- REQUESTS_COUNTER (int): A global variable that tracks the number of requests made to Riot's API.

2. API Key Management:
- get_api_key(file_name: str) -> str:
  Retrieves the Riot Games API key from a file and returns it as a string.

- get_path_db() -> str:
  Returns the full path to the SQLite database used for data storage.

3. Database Operations:
- create_connection(path_to_db: str) -> sqlite3.Connection:
  Creates and returns a connection to the SQLite database. It handles database connectivity.

- create_summonerID_table(connection: sqlite3.Connection) -> str:
  Creates the "summonerID" table in the database to store summoner information.
  Args:
  - connection (sqlite3.Connection): The active database connection.
  Returns:
  - str: The name of the table created, which is "summonerID."

- insert_into_table(path_to_db: str, table_name: str, data: list) -> None:
  Inserts a list of data into a specified database table.
  Args:
  - path_to_db (str): The path to the SQLite database.
  - table_name (str): The name of the table to insert data into.
  - data (list): A list of values to be inserted into the table, following its schema.

4. URL Generation:
- region_to_url(region: str) -> str:
  Converts a region code to its corresponding API URL for Riot Games API requests.

- tier_to_url(tier: str, division="", page: str = "1") -> str:
  Generates a URL for Riot Games API requests based on the specified tier, division, and page.
  Args:
  - tier (str): The desired tier (e.g., "Master").
  - division (str): The division within the tier (e.g., "I").
  - page (str): The page number for paginated API requests.
  Returns:
  - str: The generated API URL.

- create_tier_url(region="NA", tier="Master") -> str:
  Combines the API URL for a specific region and tier to create a complete API URL.
  Args:
  - region (str): The desired region code (e.g., "NA").
  - tier (str): The desired tier (e.g., "Master").
  Returns:
  - str: The complete API URL for the given region and tier.

- create_puuid_url(summonerId: str, region="NA") -> str:
  Generates an API URL to retrieve summoner information for a specific summoner ID.
  Args:
  - summonerId (str): The summoner's unique identifier.
  - region (str): The desired region code (e.g., "NA").
  Returns:
  - str: The API URL for retrieving summoner information.

Usage:
- Import this module to access the provided utility functions for handling Riot Games API data and SQLite databases.

Note:
- Ensure that you have a valid Riot Games API key and an existing SQLite database (data.db) under a "db" folder before using these functions.
- The rate limits used in the code logic assume that you use a personal API key from Riot's.

References:
- SQLite Tutorial: https://www.sqlitetutorial.net/sqlite-python/creating-tables/
"""


import sqlite3
from sqlite3 import Error
import os
import requests


DB_URL = "db/data.db"
REQUESTS_COUNTER = 0

region_dict = {
    "NA": "https://na1.api.riotgames.com",
    "EUW": "https://euw1.api.riotgames.com",
    "EUN": "https://eun1.api.riotgames.com",
    "BR": "https://br1.api.riotgames.com",
    "JP": "https://jp1.api.riotgames.com",
    "KR": "https://kr.api.riotgames.com",
    "LA": "https://la1.api.riotgames.com",
    "OC": "https://oc1.api.riotgames.com",
    "TR": "https://tr1.api.riotgames.com",
    "RU": "https://ru.api.riotgames.com",
    "PH": "https://ph2.api.riotgames.com",
    "SG": "https://sg2.api.riotgames.com",
    "TH": "https://th2.api.riotgames.com",
    "TW": "https://tw2.api.riotgames.com",
    "VN": "https://vn2.api.riotgames.com",
}

division_dict = {"1": "I", "2": "II", "3": "III", "4": "IV", "": ""}

tier_set = set(
    [
        "iron",
        "bronze",
        "silver",
        "gold",
        "platinum",
        "diamond",
        "master",
        "grandmaster",
        "challenger",
    ]
)


def get_api_key(file_name: str) -> str:
    with open(file_name, "r") as f:
        return f.readline().strip()


def get_path_db() -> str:
    return os.path.join(os.getcwd(), DB_URL)


def region_to_url(region: str) -> str:
    if region in region_dict:
        return region_dict[region]

    else:
        raise ValueError("The region is invalid")


def tier_to_url(tier: str, division="", page="1") -> str:
    tier = tier.lower()
    is_top_league = tier == "master" or tier == "grandmaster" or tier == "challenger"

    if division not in division_dict:
        raise ValueError("Division is invalid")
    else:
        division = division_dict[division]

    if tier not in tier_set:
        raise ValueError("Tier is invalid")

    if is_top_league and division != "":
        raise ValueError(f"You cannot have tier {tier} with a division")

    if is_top_league:
        return f"/lol/league/v4/{tier}leagues/by-queue/RANKED_SOLO_5x5"

    return f"/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page={page}"


def create_connection(path_to_db: str) -> sqlite3.Connection:
    try:
        connection = sqlite3.connect(path_to_db)
        print("Connection to database succesful !")

    except Error as e:
        raise ValueError(f"Error connecting to database :\n{e}")

    return connection


# Source : https://www.sqlitetutorial.net/sqlite-python/creating-tables/
def create_summonerID_table(connection: sqlite3.Connection) -> str:
    statement = """CREATE TABLE IF NOT EXISTS summonerID (
                                    puuid text PRIMARY KEY NOT NULL,
                                    summoner_id text NOT NULL,
                                    account_id text NOT NULL,
                                    summoner_name text NOT NULL,
                                    region text NOT NULL
                                );"""
    try:
        cursor = connection.cursor()
        cursor.execute(statement)
        connection.commit()
        connection.close()  # Making sure we close the connection
        print("Succesfully created summonerID table and committed")
        return "summonerID"
    except Exception as e:
        print(e)
        print("Now exiting")
        exit()


def insert_into_table(path_to_db: str, table_name: str, data: list) -> None:
    try:
        connection = sqlite3.connect(path_to_db)
        print("Connection to database succesful !")

    except Error as e:
        print(f"Error connecting to database :\n{e}")
        print(f"Exiting")
        exit()

    tmp = "?, " * len(data[0])
    value_string = "(" + tmp[:-2] + ")"
    cursor = connection.cursor()
    try:
        cursor.executemany(f"INSERT INTO {table_name} VALUES{value_string}", data)
    except Error as e:
        print(f"Error insert into database :\n{e}")
        connection.close()
        print(f"Closed connection, exiting")
        exit()

    connection.commit()
    connection.close()
    print(f"Succesfully added elements to {table_name}")


def create_tier_url(region="NA", tier="Master") -> str:
    try:
        region_url = region_to_url(region)
        tier_url = tier_to_url(tier)
    except ValueError as v:
        print(v)
        exit()

    return region_url + tier_url


def create_puuid_url(summonerId: str, region="NA") -> str:
    try:
        region_url = region_to_url(region)
        summoner_url = f"/lol/summoner/v4/summoners/{summonerId}"
    except ValueError as v:
        print(v)
        exit()

    return region_url + summoner_url


def create_summoner_to_id_table(
    API_KEY: str, PATH_DB: str, region="NA", tier="Master"
) -> None:
    request_url = create_tier_url(region, tier)
    headers = {"X-Riot-Token": f"{API_KEY}"}

    try:
        response = requests.get(request_url, headers=headers)
    except requests.ConnectionError:
        print("Failed to connect to Riot's API, check your internet or Riot's status")
        exit()

    if response.status_code != 200:
        print(
            f"Request status code : {response.status_code}, message : {response.reason} terminating now"
        )
        exit()

    response_dict = response.json()

    accounts_data = response_dict["entries"]

    try:
        connection = create_connection(PATH_DB)
    except ValueError as v:
        print(v)
        print("Now exiting")
        exit()

    table_name = create_summonerID_table(connection)
    formatted_data = []

    for account in accounts_data:
        summonerId = account["summonerId"]
        summonerName = account["summonerName"]

        puuid, account_id = get_id_summoner(summonerId, API_KEY, region)

        formatted_data.append((puuid, summonerId, account_id, summonerName, region))

    insert_into_table(PATH_DB, table_name, formatted_data)


def get_id_summoner(summonerId: str, API_KEY, region="NA"):
    global REQUESTS_COUNTER
    import time

    request_url = create_puuid_url(summonerId, region=region)
    headers = {"X-Riot-Token": f"{API_KEY}"}

    try:
        response = requests.get(request_url, headers=headers)
    except requests.ConnectionError:
        print("Failed to connect to Riot's API, check your internet or Riot's status")
        exit()

    # Logic for api rate limits
    if response.status_code == 429:
        wait_time = int(response.headers["Retry-After"]) + 1
        print(f"Rate limit hit, need to wait for : {wait_time}")
        time.sleep(wait_time)
        print(f"Sleeping finished, restarting requests!")

        return get_id_summoner(summonerId, API_KEY, region=region)

    if response.status_code != 200:
        print(
            f"Request status code : {response.status_code}, message : {response.reason} terminating now"
        )
        exit()

    response_dict = response.json()

    REQUESTS_COUNTER += 1

    return (response_dict["puuid"], response_dict["accountId"])
