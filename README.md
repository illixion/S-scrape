# S-Scrape

Scrape content from ss.com

## Installation

1. Install Python 3
2. Download the Python MySQL adapter from <http://dev.mysql.com/downloads/connector/python/>
3. Open a terminal and `cd` to the s-scrape directory
4. Run `pip3 install -r requirements.txt` to install dependencies

Afterwards, configure the database:

Edit the following lines to use the correct MySQL details:

* Lines 13-16 in `./sscrape/sscrape/pipelines.py`
* Lines 64-67 in `./sscrape/sscrape/middlewares.py`

## Usage

Configure a systemd or cron job to periodically run `./sscrape/scrape_all.py`

Use `proxychains` for proxying requests.
