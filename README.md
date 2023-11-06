# League of Legends API Data Collector and Analyzer

**Early Development Stage**

This project is an early-stage data collector for the League of Legends game, designed to gather summoner information using the Riot Games API and store it in a local SQLite database. This README provides an overview of the project so far and instructions for use.

## Table of Contents

- [League of Legends API Data Collector and Analyzer](#league-of-legends-api-data-collector-and-analyzer)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Project Status](#project-status)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## Overview

The League of Legends API Data Collector is a Python-based application that utilizes the Riot Games API to collect summoner data and store it in a local SQLite database. It offers a set of utility functions for managing API keys, creating database connections, performing database operations, and generating API URLs based on different parameters.

## Project Status

**Early Development Stage**: This project is currently in its early stages of development. It provides basic functionality for collecting summoner data from the Riot Games API and storing it locally. Future enhancements and features are planned, such as data analysis and visualization.

## Prerequisites

Before using the League of Legends API Data Collector, ensure you have the following prerequisites in place:

- Python 3.x
- Required Python libraries: `sqlite3` and `requests`
- A valid Riot Games API key
- A local SQLite database file named `data.db` stored under a folder named `db`

## Installation

1. Clone this repository to your local machine.
2. Make sure you have the required Python libraries installed.
3. Store your Riot Games API key in a file named `API.in`.

## Usage

To use the project, import the `utility.py` module into your Python script. You can utilize the provided utility functions to gather and store summoner data. For example:

```python
from utility import *

def main():
    API_KEY = get_api_key("API.in")
    PATH_DB_URL = get_path_db()
    create_summoner_to_id_table(API_KEY, PATH_DB_URL, tier="Master")
```

if you have suggestions, bug reports, or would like to contribute new features, please open an issue or submit a pull request. We appreciate your help in making this project better!

## License

This project is licensed under the [GNU General Public License, version 3.0 (GPL-3.0)](LICENSE) - see the [LICENSE](LICENSE) file for details.

---

Please note that this project is in its early stages, and more features and improvements are planned. Your feedback and contributions are highly encouraged to help advance the project.