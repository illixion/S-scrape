# S-Scrape

Scrape content from ss.com

This is a legacy branch, do not use this in production. No support is provided for deployments using this codebase.

## Installation

1. Install Python 3
2. Download the Python MySQL adaptor from <http://dev.mysql.com/downloads/connector/python/>
3. Open a terminal and `cd` to the s-scrape directory
4. Run `pip3 install -r requirements.txt` to install dependencies

Afterwards, configure the database:

1. Rename *config.ini.dist* to *config.ini*
2. Open it in text editor and modify values as desired
3. Import the provided mysql_database.sql into your MySQL database
4. If **source** or **destination** config parameters were changed, update the SQL table names accordingly

## Usage

Add your ss.com RSS URLs to the source database. To find the RSS URL, go to <https://www.ss.com/ru/transport/cars/> and you'll see an "RSS" link at the bottom of the page. It will show all ads for the category that you're looking at, so you can choose a manufacturer, copy the RSS link and filter by manufacturer that way.

For example, to get all car ads, use this URL: <https://www.ss.com/ru/transport/cars/rss/>

Run s-scrape.py and it'll automatically start in foreground mode. To quit, press Ctrl+C. It's possible to use a SystemD unit to daemonize S-Scrape.
