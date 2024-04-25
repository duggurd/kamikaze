import dotenv
import psycopg2
import os
from util import connect_db
import requests
from datetime import datetime


def recreate_db(conn, database:str):
    print(f"Rcreating database: {database}")
    cur = conn.cursor()

    cur.execute("DROP DATABASE IF EXISTS %s", (database,))
    conn.commit()
    cur.execite("CREATE DATABASE IF NOT EXISTS %s", (database,))

    conn.commit()
    print(f"Created database: {database}")


def seed_rss_urls(conn):
    print("Creating rss_urls table")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS rss_urls CASCADE;")
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rss_urls (
            rss_url varchar PRIMARY KEY, 
            source varchar, 
            name varchar
        );
    """)

    conn.commit()
    
    urls = [
        {"name": "stock_market",  "source": "investing.com", "rss_url": "https://www.investing.com/rss/news_25.rss"},
        {"name": "stock_opinions",  "source": "investing.com", "rss_url": "https://www.investing.com/rss/stock_Opinion.rss"},
        {"name": "stock_picks",  "source": "investing.com", "rss_url": "https://www.investing.com/rss/stock_stock_picks.rss"},
        {"name": "top_stories",  "source": "feeds.content.dowjones.com", "rss_url": "https://feeds.content.dowjones.io/public/rss/mw_topstories"},
        {"name": "rt_headlines",  "source": "feeds.content.dowjones.com", "rss_url": "https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines"},
        {"name": "breaking_news",  "source": "feeds.marketwatch.com", "rss_url": "http://feeds.marketwatch.com/marketwatch/bulletins"},
        {"name": "market_pulse",  "source": "feeds.content.dowjones.com", "rss_url": "https://feeds.content.dowjones.io/public/rss/mw_marketpulse"},
        {"name": "r/wallstreetbets", "source": "reddit.com", "rss_url": "https://www.reddit.com/r/wallstreetbets/new/.rss"},
        {"name": "r/stocks", "source": "reddit.com", "rss_url": "https://www.reddit.com/r/stocks/new/.rss"},
    ]

    cur.executemany("""
        INSERT INTO rss_urls (
            rss_url,
            name, 
            source
        ) values (
            %(rss_url)s,
            %(name)s, 
            %(source)s
        );
    """, urls)

    conn.commit()

    print("Created rss_urls table")

def seed_rss_status(conn):
    print("Creating rss_status table")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS rss_status;")
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rss_status (
            rss_url varchar UNIQUE, 
            etag varchar, 
            modified_ts timestamp,
            FOREIGN KEY (rss_url) REFERENCES rss_urls (rss_url)
        );
    """)
    conn.commit()

    print("Created rss_status table")

def seed_rss_feed(conn):
    print("Creating rss_feed table")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS rss_feed CASCADE;")
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rss_feed (
            content_url varchar PRIMARY KEY,
            rss_url varchar,
            content_title varchar,
            published_ts timestamp,
            author varchar,
            raw text,
               
            FOREIGN KEY (rss_url) REFERENCES rss_urls (rss_url)
        );
    """)
    conn.commit()

    print("Created rss_feed table")

def seed_transformed_feed(conn):
    print("creating transformed_rss_feed table")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS transformed_rss_feed;")
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transformed_rss_feed (
            content_url varchar UNIQUE,
            clean_content_title VARCHAR,
            FOREIGN KEY (content_url) REFERENCES rss_feed (content_url)
        );
    """)
    conn.commit()
    print("Created transformed_rss_feed")

def seed_sentiment(conn):
    print("creating sentiment table")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS sentiment;")

    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sentiment (
            content_url varchar UNIQUE,
            positive numeric,
            neutral numeric,
            negative numeric,
            published_ts timestamp,
            FOREIGN KEY (content_url) REFERENCES rss_feed (content_url)
        );
    """)

    conn.commit()

    print("created sentiment table")


def seed_tickers(conn):

    print("seeding ticker symbols")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS tickers;")
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickers (
            id int PRIMARY KEY,
            cik_str int,
            ticker varchar,
            title varchar
        );
    """)

    data = requests.get("https://www.sec.gov/files/company_tickers.json", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"}).json()


    res = []
    for key, value in data.items():
        value["id"] = int(key)
        
        res.append(value)

    cur.executemany("""
        INSERT INTO tickers (
            id,
            cik_str,
            ticker,
            title
        ) values (  
            %(id)s,
            %(cik_str)s,
            %(ticker)s,
            %(title)s
        );
        """, res)
    conn.commit()

    print("seeded ticker symbols")



def seed_database():
    conn = connect_db()

    seed_rss_urls(conn)
    seed_rss_status(conn)
    seed_rss_feed(conn)
    seed_transformed_feed(conn)
    seed_sentiment(conn)
    seed_tickers(conn)


# @dag(
#     dag_id="seed_database",
#     schedule=None,
#     start_date=datetime.now()
# )
# def seed_database_dag():
    
#     @task
#     def seed():
#         seed_database()
#     seed()

# if __name__ != "__main__":
#     seed_database_dag()

if __name__ == "__main__":
    seed_database()