# S-Scrape

Scrape content from ss.com

## Installation

1. Install Python 3
2. Download the Python MySQL adaptor from <http://dev.mysql.com/downloads/connector/python/>
3. Open a terminal and `cd` to the s-scrape directory
4. Run `pip3 install -r requirements.txt` to install dependencies

Afterwards, configure the database:

1. Rename *config.ini.dist* to *config.ini*
2. Open it in text editor and modify values as desired
3. Import the provided mysql_database.sql into your MySQL database

## Usage

Run s-scrape.py and it'll automatically start in foreground mode. To quit, press Ctrl+C. It's possible to use a SystemD unit to daemonize S-Scrape.
