import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from openai import OpenAI
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_KEY"), 
)

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

# Function for industry classification
def industry_classification(company_name, mission_statement):

    prompt = (
        f"Given the company name '{company_name}' and the mission statement:\n"
        f"'{mission_statement}', classify the company into one of the following categories: "
        "Retail, Technology, Healthcare, Energy_Sector, Investment_Finance, or Other. "
        "Base it off the company name, mission statement, and some background research."
        "Only return the same formatted industry chosen from one of the above categories."
    )

    try:

        completion = client.chat.completions.create(
            model = "gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        industry = completion.choices[0].message.content
        
        return industry.strip()

    except Exception as e:
        print(f"Error predicting industry: {e}")
        return "Other"
    
count = 0
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
            count += 1
            print(count, company_name)
            industry = industry_classification(company_name, mission_statement)
            
            # Add to the list
            if company_name and mission_statement:
                companies.append({"company_name": company_name, "mission_statement": mission_statement, "industry": industry})

        except AttributeError:
            break

# Metadata, the source, extracted date, number of companies represented, then the companies
metadata_file = "data/fortune_500.json"
metadata = {
    "source": url,
    "extracted_date": datetime.now().strftime("%Y-%m-%d"),
    "num_companies": len(companies),
    "companies": companies
}

# Save the data to a JSON file in the data directory
with open(metadata_file, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, indent=4)

industry_groups = defaultdict(list)
for company in companies:

    industry = company["industry"]
    industry_groups[industry].append(company)

for industry, companies in industry_groups.items():

    industry_file = os.path.join("data/", f"{industry}.json")

    with open(industry_file, 'w', encoding='utf-8') as f:
        json.dump({
            "industry": industry,
            "num_companies": len(companies),
            "companies": companies
        }, f, ensure_ascii=False, indent=4)
        
    print(f"Saved {len(companies)} companies to '{industry_file}'.")

print("All JSON files have been created.")


