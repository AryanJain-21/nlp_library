import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Website URL
url = "https://tomislavhorvat.com/mission-statement-examples/"

# GET request to access page, simulating browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)
response.raise_for_status()


soup = BeautifulSoup(response.text, 'html.parser')
companies = []

headers = ['1-100', '101-200', '201-300', '301-400', '401-500']

for extract in headers:

    header = soup.find('h2', string=extract)
    if not header:
        raise ValueError("Header not found on page.")

    # Start extracting data from the sibling elements of the header
    next_element = header.find_next_sibling()
    while next_element and next_element.name == 'p':
        try:
            # Get company name and mission statement
            company_name = " ".join((next_element.get_text(strip=True)).split(" ")[1:])

            next_element = next_element.find_next_sibling()

            mission_statement = next_element.get_text(strip=True)

            next_element = next_element.find_next_sibling() if next_element else None
            
            # Add to the list
            if company_name and mission_statement:
                companies.append({"company_name": company_name, "mission_statement": mission_statement})

        except AttributeError:
            break

# Metadata, the source, extracted date, number of companies represented, then the companies
output_data = {
    "source": url,
    "extracted_date": datetime.now().strftime("%Y-%m-%d"),
    "num_companies": len(companies),
    "companies": companies
}

# Save the data to a JSON file in the data directory
output_file = "data/fortune_500.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f"Saved to '{output_file}'.")
