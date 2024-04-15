# import autopipimport 
import requests
import re
import pandas as pd
import pyperclip

def extract_dois(url):
  """Extracts DOIs from a URL.

  Args:
    url: A URL.

  Returns:
    A list of DOIs.
  """

  response = requests.get(url)
  text = response.text
  dois = re.findall(r'\b10\.\d{4,9}/[-.;()/:\w]+', text)
  return dois
add_str = lambda x: 'https://doi.org/' + str(x)

def main():
  url = pyperclip.paste()
  dois = extract_dois(url)
  links = list(map(add_str, dois))
  df = pd.DataFrame({"DOI": links})
  df.to_csv("dois.csv", index=False)
  df['DOI'].to_clipboard(index=False, header=False)
  return df['DOI']

if __name__ == "__main__":
  doi_list = main()
  # library_id = '9769982'
  # api_key = 'fw2EPYr4Dby6PulXbrftoSZ2'
  # collection_id = "SILYZPVI"
  # add_items_to_zotero_by_doi(list(doi_list), library_id, api_key, collection_id)
  doi_list_string = '\n'.join(doi_list.astype(str))
  pyperclip.copy(doi_list_string)