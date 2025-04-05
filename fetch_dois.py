import requests
import re
import pandas as pd

def extract_dois(url):
    """Extracts DOIs from a URL.

    Args:
        url (str): A URL.

    Returns:
        list: A list of DOIs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        text = response.text
        dois = re.findall(r'\b10\.\d{4,9}/[-.;()/:\w]+', text)
        return dois
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

def save_dois_to_csv(dois, filename="dois.csv"):
    """Saves DOIs to a CSV file.

    Args:
        dois (list): A list of DOIs.
        filename (str): The name of the CSV file.
    """
    if dois:
        links = ['https://doi.org/' + doi for doi in dois]
        df = pd.DataFrame({"DOI": links})
        df.to_csv(filename, index=False)
        print(f"DOIs saved to {filename}")
    else:
        print("No DOIs found to save.")

if __name__ == "__main__":
    url = input("Enter the URL to fetch DOIs from: ")
    dois = extract_dois(url)
    if dois:
        print(f"Found {len(dois)} DOIs:")
        for doi in dois:
            print(doi)
        save_dois_to_csv(dois)
    else:
        print("No DOIs found.")