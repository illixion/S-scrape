# S-Scrape

Scrape content from ss.com

## Installation

1. Install Python 3
2. Download the Python MySQL adaptor from <http://dev.mysql.com/downloads/connector/python/>
3. Open a terminal and `cd` to the s-scrape directory
4. Run the following commands:

```shell
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

Afterwards, configure the database:

1. Rename *config.py.dist* to *config.py*
2. Open it in text editor and modify values as desired. Source: where to take RSS feed URLs from, destination: where to put them
3. Import provided mysql_database.sql into your MySQL database

