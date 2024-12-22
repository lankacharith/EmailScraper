import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import os
from urllib.parse import urljoin, urlparse
from utils import validate_email, validate_email_with_hunter
from config import RATE_LIMIT

class EmailScraper:
    def __init__(self, rate_limit=RATE_LIMIT):
        self.rate_limit = rate_limit
        self.results = {}

    def fetch_website(self, url):
        try:
            headers = {"User-Agent": "EmailScraperBot/1.0 (+http://example.com)"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_emails(self, content, base_url):
        emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content))
        return {email for email in emails if validate_email_with_hunter(email)}

    def scrape_website(self, url):
        content = self.fetch_website(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            emails = self.extract_emails(soup.get_text(), url)
            self.results[url] = list(emails)
            print(f"Found {len(emails)} emails on {url}: {', '.join(emails)}")
        else:
            print(f"No emails found on {url}.")

    def save_to_csv(self, output_file="output/scraped_emails.csv"):
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        data = []
        for site, emails in self.results.items():
            for email in emails:
                data.append({"Website": site, "Email": email})

        # Save the data to a CSV file
        import pandas as pd
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")

if __name__ == "__main__":
    scraper = EmailScraper()

    while True:
        user_input = input("\nEnter a website URL to scrape (or type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break

        if not user_input.startswith("http"):
            print("Please enter a valid URL (e.g., https://example.com).")
            continue

        scraper.scrape_website(user_input)

        # Save results after every scrape
        scraper.save_to_csv()