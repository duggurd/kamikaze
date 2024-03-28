import json
import feedparser
import datetime

def parse_feed(rss_feed, url):
    feed = []

    for entry in rss_feed["entries"]:
        
        e = {
            "rss_url": "",
            "content_title": "",
            "content_url": "",
            "published": "",
            "author": "",
            "raw": "",
        }
        e["rss_url"] = url
        e["content_title"] = entry["title"]
        e["published"] = entry["published"]
        if entry.get("author") is not None:
            e["author"] = entry["author"]
        e["content_url"] = entry["link"]
        e["raw"] = json.dumps(entry)

        feed.append(e)

    return feed


def scrape_feed(rss_url: str, conn):

    cur = conn.cursor()

    cur.execute("""
        SELECT 
            etag,
            modified_ts 
        FROM rss_status 
        WHERE rss_url = %s
        LIMIT 1;
    """, (rss_url,))
        
    status = cur.fetchone()

    etag = None
    modified = None
    if status is not None:
        if status[0] is not None:
            etag = status[0]
        if status[1] is not None:
            modified = datetime.datetime.fromisoformat(status[1])
    
    rss_feed = feedparser.parse(
        rss_url,
        etag=etag,
        modified=modified
    )
    
    # read rss feed and send to db
    parsed_feed = parse_feed(rss_feed, rss_url)

    cur.executemany("""
        INSERT INTO rss_feed (
            content_url,
            rss_url,
            content_title,
            published,
            author,
            raw
        ) values (
            %(content_url)s,
            %(rss_url)s,
            %(content_title)s,
            %(published)s,
            %(author)s,
            %(raw)s
        )
        ON CONFLICT (content_url) DO NOTHING;
    """, parsed_feed)
    conn.commit()

    # update rss_status in db
    status = {
        "etag": None,
        "modified_ts": None
    }

    if "etag" in rss_feed.keys():
        status["etag"] = rss_feed["etag"]
    elif "updated" in rss_feed.keys():
        status["modified_ts"] = rss_feed["updated"] 
    
    if status["etag"] is not None or status["modified_ts"] is not None:
        cur.execute("""
            UPDATE rss_status SET etag = %s, modified_ts = %s
            WHERE rss_url = %s;
        """, (status["etag"], status["modified_ts"], rss_url,))


def scrape_feeds(conn):
    cur = conn.cursor()

    cur.execute("SELECT rss_url FROM rss_urls;")

    rss_urls = [row[0] for row in  cur.fetchall()]

    for rss_url in rss_urls:
        scrape_feed(rss_url, conn)
