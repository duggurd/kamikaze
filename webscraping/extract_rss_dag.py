from airflow.decorators import dag, task
from datetime import datetime
from scrape_rss_feeds import scrape_feed
from util import connect_db
import re

def dyanmic_feed_scrape_task(name):
    @task(task_id=name)
    def scrape(db_conn, rss_url):
        scrape_feed(db_conn, rss_url)
    return scrape

@task
def transform(db_conn):
    cur = db_conn.cursor()

    cur.execute("""
        SELECT content_url, content_title FROM rss_feed AS rf
        WHERE NOT EXISTS (
            SELECT 1
            FROM transformed_rss_feed AS trf
            WHERE trf.content_url = rf.content_url
        );
    """)

    for result_set in cur.fetchmany(1000):
        res = []
        for row in result_set:
            pattern = re.compile(r"[%\?\.,-!/&$£@\]\[\(\)=\+")
            clean_content_title = row[1]
            clean_content_title = re.sub(pattern, "", clean_content_title)

            res.append((row[0], clean_content_title))

        cur.executemany("""
            INSERT INTO transformed_rss_feed (
                content_url, 
                clean_content_title
            ) values(
                %s,
                %s
            )
            ON CONFLICT (content_url) DO NOTHING;
        """, res)

    db_conn.commit()


@dag(
    dag_id="parse_rss_feeds",
    schedule="*/30 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def extract_rss_feeds():
    db_conn = connect_db()

    db_cur = db_conn.cursor()

    db_cur.execute("SELECT rss_url, name FROM rss_urls;")
    
    scrape_tasks = []
    for (rss_url, name) in db_cur.fetchall():
        name = name.replace("/", "_")
        scrape_tasks.append(dyanmic_feed_scrape_task(name)(db_conn, rss_url))
    
    scrape_tasks >> transform(db_conn)

extract_rss_feeds()