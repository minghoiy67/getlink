import re
import requests
from bs4 import BeautifulSoup

def load_keywords(file_path):
    """Load keywords from a file."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []

def extract_urls_from_page(url):
    """Extract URLs from a web page."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Debug: Save the fetched HTML to a file for inspection
        with open("debug_fetched_page.html", "w", encoding="utf-8") as debug_file:
            debug_file.write(soup.prettify())

        # Extract URLs from Bing search results
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith("http") and "bing.com" not in href:
                links.append(href)
        print(f"Extracted raw links: {links}")  # Debug log
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL '{url}': {e}")
        return []

def search_urls(keywords):
    """Search for URLs containing the given keywords."""
    urls = []
    exclude_keywords = [
        "info", "news", "support", "contact", ".edu", ".gov", "privacy",
        "frontdesk", "help", ".png", "school", "customerservices",
        "firstname", "compliance", "career", "example", "feedback",
        "subscriptions", "customercare", "editor", "questions",
        "contact us", "forum", "download", "login", "signup"
    ]
    try:
        with open("found_urls.txt", "w") as output_file:
            for keyword in keywords:
                print(f"Searching for URLs with keyword: {keyword}...")
                search_url = f"https://www.bing.com/search?q={keyword}"
                fetched_urls = extract_urls_from_page(search_url)
                print(f"Fetched URLs for keyword '{keyword}': {fetched_urls}")  # Debug log

                filtered_urls = [
                    url for url in fetched_urls
                    if not any(exclude in url.lower() for exclude in exclude_keywords)
                ]
                print(f"Filtered URLs for keyword '{keyword}': {filtered_urls}")  # Debug log

                for url in filtered_urls:
                    output_file.write(url + "\n")  # Save URL in real-time
                    output_file.flush()  # Ensure the URL is written immediately
                    urls.append(url)
                print(f"Found {len(filtered_urls)} URLs for keyword: {keyword}")
    except IOError as e:
        print(f"Error writing to file: {e}")
    return urls

# Load keywords from keywords.txt
keywords_file = "keywords.txt"
keywords = load_keywords(keywords_file)

if keywords:
    # Use the keywords to search for URLs
    urls = search_urls(keywords)

    # Print the total number of saved URLs
    print(f"Total URLs saved: {len(urls)}")

    # Print the found URLs
    for url in urls:
        print(url)
else:
    print("No keywords to process.")
