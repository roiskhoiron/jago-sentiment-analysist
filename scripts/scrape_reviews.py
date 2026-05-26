import csv
import time
from google_play_scraper import reviews_all, Sort

APP_ID = "com.jago.android"
OUTPUT_FILE = "data/raw/reviews.csv"
TARGET_COUNT = 10000
LANG = "id"
COUNTRY = "id"

def main():
    print(f"Scraping reviews for {APP_ID}...")
    result = reviews_all(
        APP_ID,
        sleep_milliseconds=1000,
        lang=LANG,
        country=COUNTRY,
        sort=Sort.NEWEST,
    )
    print(f"Fetched {len(result)} reviews total")

    id_filter = set()
    unique = []
    for r in result:
        if r["reviewId"] not in id_filter:
            id_filter.add(r["reviewId"])
            unique.append(r)

    print(f"Unique reviews: {len(unique)}")
    sample = unique[:TARGET_COUNT]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "reviewId", "content", "score", "at", "userName"
        ])
        writer.writeheader()
        for r in sample:
            writer.writerow({
                "reviewId": r["reviewId"],
                "content": r["content"],
                "score": r["score"],
                "at": r["at"].isoformat() if hasattr(r["at"], "isoformat") else r["at"],
                "userName": r["userName"],
            })

    print(f"Saved {len(sample)} reviews to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
