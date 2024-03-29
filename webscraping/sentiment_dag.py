from airflow.decorators import dag, task
from airflow.datasets import Dataset
from datetime import datetime
import requests
from util import connect_db
import psycopg2

db_conn = connect_db()

db_cur = db_conn.cursor()

db_cur.execute("SELECT rss_url, name FROM rss_urls;")

datasets = []
for (rss_url, name) in db_cur.fetchall():
    name = name.replace("/", "_")
    datasets.append(Dataset(uri=rss_url, extra={"name":name}))


@task
def calc_sentiment():
    conn = connect_db()

    cur = conn.cursor()

    # get the most recent update for delta
    cur.execute("""
        SELECT max(published_ts)
        FROM sentiment
        LIMIT 1
    """)

    max_ts = cur.fetchone()[0]

    if max_ts is None:
        cur.execute("""
            SELECT  
                content_url,
                content_title,
                published_ts
            FROM rss_feed
        """)
    else:
        cur.execute("""
            SELECT  
                content_url,
                content_title,
                published_ts
            FROM rss_feed
            WHERE published_ts > %s 
        """, (max_ts,))
    
    sentiment = []
    
    while True:
        result_set = cur.fetchmany(50)
        if result_set == []:
            break

        titles = [row[1] for row in result_set]
        resp = requests.post("http://kamikaze_model:8000/sentiment/batch", json={"text":titles}, timeout=60)

        data = resp.json()

    
        for res, row in zip(data["sentiment"], result_set):
            e = {
                "content_url":"",
                "positive":0,
                "neutral":0,
                "negative":0,
                "published_ts":0
            }

            e["content_url"] = row[0]
            e["positive"] = res[0]
            e["neutral"] = res[1]
            e["negative"] = res[2]
            e["published_ts"] = row[2]

            sentiment.append(e)

    cur.executemany("""
        INSERT INTO sentiment (
            content_url, 
            positive, 
            neutral, 
            negative, 
            published_ts
        ) values (
            %(content_url)s,
            %(positive)s,
            %(neutral)s,
            %(negative)s,
            %(published_ts)s
        )      
        ON CONFLICT (content_url) DO NOTHING;
    """, sentiment)

    conn.commit()


@dag(
    dag_id="get_sentiment",
    schedule=datasets,
    start_date=datetime.now(),
    catchup=False
)
def get_sentiment():
    
    calc_sentiment()

get_sentiment()

