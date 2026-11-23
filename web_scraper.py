
import requests
from bs4 import BeautifulSoup
import json

# Website URL
url = "https://quotes.toscrape.com/"

try:
    # Send HTTP request
    response = requests.get(url, timeout=10)

    # Check whether request was successful
    response.raise_for_status()

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all quotes
    quotes = soup.find_all("div", class_="quote")

    data = []

    for quote in quotes:
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)

        tags = [
            tag.get_text(strip=True)
            for tag in quote.find_all("a", class_="tag")
        ]

        data.append({
            "quote": text,
            "author": author,
            "tags": tags
        })

    # Save data in JSON file
    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    # Save data in text file
    with open("quotes.txt", "w", encoding="utf-8") as file:
        for item in data:
            file.write("Quote: " + item["quote"] + "\n")
            file.write("Author: " + item["author"] + "\n")
            file.write("Tags: " + ", ".join(item["tags"]) + "\n")
            file.write("-" * 50 + "\n")

    print("Web scraping completed successfully!")
    print("Total quotes extracted:", len(data))
    print("Data saved in quotes.json and quotes.txt")

except requests.exceptions.RequestException as error:
    print("HTTP Request Error:", error)

except Exception as error:
    print("An error occurred:", error)
