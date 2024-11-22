import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URL of the website
url = "https://tomislavhorvat.com/mission-statement-examples/"

# Send a GET request to fetch the website content
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)
response.raise_for_status()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the <h2> header with the text "1-100"
header = soup.find('h2', string="1-100")
if not header:
    raise ValueError("Header not found on page.")

# Prepare a list to store company data
companies = []

# Start extracting data from the sibling elements of the header
next_element = header.find_next_sibling()
while next_element and next_element.name == 'p':  # Process only <p> tags
    try:
        # Get company name and mission statement
        company_name = " ".join((next_element.get_text(strip=True)).split(" ")[1:])
        next_element = next_element.find_next_sibling()  # Move to the next <p>
        mission_statement = next_element.get_text(strip=True)
        next_element = next_element.find_next_sibling() if next_element else None  # Move to the next <p>
        
        # Add to the list
        if company_name and mission_statement:
            companies.append({"company_name": company_name, "mission_statement": mission_statement})
    except AttributeError:
        break  # Stop if there's an issue with navigation

# Add metadata to the output
output_data = {
    "source": url,
    "extracted_date": datetime.now().strftime("%Y-%m-%d"),  # Current date in YYYY-MM-DD format
    "num_companies": len(companies),  # Number of companies included
    "companies": companies  # First 100 companies
}

# Save the data to a JSON file
output_file = "first_100_companies.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f"Saved first 100 companies with metadata to '{output_file}'.")
