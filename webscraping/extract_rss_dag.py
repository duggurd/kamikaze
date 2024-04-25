from airflow.decorators import dag, task
from datetime import datetime
from scrape_rss_feeds import scrape_feed
from util import connect_db
import re
from airflow.datasets import Dataset
import psycopg2
  
def dyanmic_feed_scrape_task(name, dataset):
    @task(task_id=name, outlets=[dataset])
    def scrape(db_conn, rss_url):
        scrape_feed(rss_url, db_conn)
    return scrape

@task
def transform(db_conn):
    print("transforming content")

    cur = db_conn.cursor()

    cur.execute("""
        SELECT 
            content_url, 
            content_title 
        FROM rss_feed AS rf
        WHERE NOT EXISTS (
            SELECT 1
            FROM transformed_rss_feed AS trf
            WHERE trf.content_url = rf.content_url
        );
    """)
    res = []
    
    while True: 
        result_set = cur.fetchmany(100)
        if result_set == []:
            break

        for row in result_set:
            pattern = re.compile(r"[%\?\.,\-!/&$£@\]\[\(\)=\+:]")

            clean_content_title = row[1]
            clean_content_title = re.sub(pattern, "", clean_content_title)

            res.append((row[0], clean_content_title.lower()))

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
    start_date=datetime.now(),
    catchup=False,
)
def extract_rss_feeds():
    db_conn = connect_db()

    db_cur = db_conn.cursor()

    db_cur.execute("SELECT rss_url, name FROM rss_urls;")


    scrape_tasks = []
    # create datasets and tasks
    for (rss_url, name) in db_cur.fetchall():
        name = name.replace("/", "_")
        dataset = Dataset(uri=rss_url, extra={"name":name})
    
        scrape_tasks.append(dyanmic_feed_scrape_task(name, dataset)(db_conn, dataset.uri))
    
    scrape_tasks >> transform(db_conn)

extract_rss_feeds()