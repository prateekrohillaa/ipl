import sys
import codecs
import requests
from bs4 import BeautifulSoup
import pandas as pd

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

BASE_URL = "https://en.wikipedia.org/wiki/2026_Indian_Premier_League"

def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def scrape_points_table(soup):
    tables = soup.find_all("table", class_="wikitable")
    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        if "Pts" in headers and "Team" in headers:
            rows = []
            for row in table.find_all("tr")[1:]:
                cells = [td.get_text(strip=True) for td in row.find_all(["th", "td"])]
                if cells:
                    rows.append(cells[:len(headers)])
            df = pd.DataFrame(rows, columns=headers[:max(len(r) for r in rows)])
            return df
    return pd.DataFrame()

def scrape_batting_stats(soup):
    tables = soup.find_all("table", class_="wikitable")
    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        if "Runs" in headers and "Player" in headers:
            rows = []
            for row in table.find_all("tr")[1:]:
                cells = [td.get_text(strip=True) for td in row.find_all(["th", "td"])]
                if cells:
                    rows.append(cells)
            df = pd.DataFrame(rows, columns=headers[:max(len(r) for r in rows)])
            return df
    return pd.DataFrame()

def scrape_bowling_stats(soup):
    tables = soup.find_all("table", class_="wikitable")
    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        if "Wickets" in headers and "Player" in headers:
            rows = []
            for row in table.find_all("tr")[1:]:
                cells = [td.get_text(strip=True) for td in row.find_all(["th", "td"])]
                if cells:
                    rows.append(cells)
            df = pd.DataFrame(rows, columns=headers[:max(len(r) for r in rows)])
            return df
    return pd.DataFrame()

def generate_dummy_data():
    print("Wikipedia data unavailable. Generating dummy IPL data...")

    points_df = pd.DataFrame({
        "Pos": ["1","2","3","4","5","6","7","8","9","10"],
        "Grp": ["A","B","A","B","A","B","A","B","A","B"],
        "Team": ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Rajasthan Royals","Sunrisers Hyderabad","Delhi Capitals","Punjab Kings","Gujarat Titans","Lucknow Super Giants"],
        "Pld": ["14","14","14","14","14","14","14","14","14","14"],
        "W": ["10","9","8","7","7","6","5","5","4","3"],
        "L": ["4","5","6","7","7","8","9","9","10","11"],
        "NR": ["0","0","0","0","0","0","0","0","0","0"],
        "Pts": ["20","18","16","14","14","12","10","10","8","6"],
        "NRR": ["+0.850","+0.620","+0.340","+0.180","-0.050","-0.120","-0.280","-0.410","-0.550","-0.780"],
        "Qualification": ["Advance to thequalifier 1","Advance to thequalifier 1","Advance to theeliminator","Advance to theeliminator","","","","","",""]
    })

    batting_df = pd.DataFrame({
        "Player": ["Virat Kohli","Rohit Sharma","Shubman Gill","Ruturaj Gaikwad","Sanju Samson","KL Rahul","Suryakumar Yadav","Jos Buttler"],
        "Runs": ["568","512","487","456","423","398","372","345"],
        "Team": ["Royal Challengers Bengaluru","Mumbai Indians","Kolkata Knight Riders","Chennai Super Kings","Rajasthan Royals","Sunrisers Hyderabad","Mumbai Indians","Rajasthan Royals"]
    })

    bowling_df = pd.DataFrame({
        "Player": ["Jasprit Bumrah","Rashid Khan","Mohammed Shami","Trent Boult","Yuzvendra Chahal","Mitchell Starc","Harshal Patel","Kagiso Rabada"],
        "Wickets": ["22","20","18","16","15","14","12","11"],
        "Team": ["Mumbai Indians","Gujarat Titans","Gujarat Titans","Kolkata Knight Riders","Rajasthan Royals","Kolkata Knight Riders","Royal Challengers Bengaluru","Delhi Capitals"]
    })

    return points_df, batting_df, bowling_df

if __name__ == "__main__":
    print("Attempting to scrape IPL data from Wikipedia...")
    try:
        soup = get_soup(BASE_URL)
        points_df = scrape_points_table(soup)
        batting_df = scrape_batting_stats(soup)
        bowling_df = scrape_bowling_stats(soup)

        if points_df.empty or batting_df.empty or bowling_df.empty:
            raise ValueError("Scraped data is incomplete")

        print("Successfully scraped Wikipedia data.")
    except Exception as e:
        print(f"Scraping failed: {e}")
        points_df, batting_df, bowling_df = generate_dummy_data()

    print("\n=== POINTS TABLE ===")
    print(points_df.to_string(index=False))

    print("\n=== TOP BATSMEN ===")
    print(batting_df.to_string(index=False))

    print("\n=== TOP BOWLERS ===")
    print(bowling_df.to_string(index=False))

    points_df.to_csv("points_table_raw.csv", index=False)
    batting_df.to_csv("batting_stats_raw.csv", index=False)
    bowling_df.to_csv("bowling_stats_raw.csv", index=False)

    print("\nSaved: points_table_raw.csv, batting_stats_raw.csv, bowling_stats_raw.csv")
