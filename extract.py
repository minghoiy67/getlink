import re
import os

def search_urls_with_keyword(text, keyword):
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    matching_urls = [url for url in urls if keyword in url]
    return matching_urls

if __name__ == "__main__":
    text = input("Enter the text to search: ")
    keyword = input("Enter the keyword to search for: ").strip()
    results = search_urls_with_keyword(text, keyword)
    # Ask user if they want to input a keyword or provide a file with keywords
    choice = input("Do you want to enter a single keyword or provide a file with keywords? (Enter 'single' or 'file'): ").strip().lower()

    if choice == 'file':
        file_path = input("Enter the path to the file with keywords: ").strip()
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                keywords = [line.strip() for line in f.readlines()]
            results = [url for keyword in keywords for url in search_urls_with_keyword(text, keyword)]
        else:
            print("File not found. Exiting.")
            results = []
    elif choice == 'single':
        results = search_urls_with_keyword(text, keyword)
    else:
        print("Invalid choice. Exiting.")
        results = []
    # Save results to link.txt in the same folder
    output_file = os.path.join(os.path.dirname(__file__), "link.txt")
    with open(output_file, "w") as file:
        for url in results:
            file.write(url + "\n")
    
    print(f"Matching URLs saved to {output_file}")
