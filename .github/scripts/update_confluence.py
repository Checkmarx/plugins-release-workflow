import os
import requests
from requests.auth import HTTPBasicAuth
import json
from bs4 import BeautifulSoup
import argparse

# Fetching Confluence API credentials from environment variables
CONFLUENCE_BASE_URL = 'https://checkmarx.atlassian.net/wiki'
CONFLUENCE_API_USERNAME = os.getenv('CONFLUENCE_API_USERNAME')
CONFLUENCE_API_TOKEN = os.getenv('CONFLUENCE_API_TOKEN')
PAGE_ID = '8251998711'  # Replace with your actual page ID

# Function to get the current page content
def get_page_content():
    url = f'{CONFLUENCE_BASE_URL}/rest/api/content/{PAGE_ID}?expand=body.storage,version'
    response = requests.get(url, auth=HTTPBasicAuth(CONFLUENCE_API_USERNAME, CONFLUENCE_API_TOKEN))
    response.raise_for_status()
    return response.json()

# Function to update the page content
def update_page_content(new_content, version_number, title):
    url = f'{CONFLUENCE_BASE_URL}/rest/api/content/{PAGE_ID}'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'id': PAGE_ID,
        'type': 'page',
        'title': title,
        'body': {
            'storage': {
                'value': new_content,
                'representation': 'storage'
            }
        },
        'version': {
            'number': version_number + 1
        }
    }
    response = requests.put(url, headers=headers, data=json.dumps(data), auth=HTTPBasicAuth(CONFLUENCE_API_USERNAME, CONFLUENCE_API_TOKEN))
    response.raise_for_status()
    return response.json()

# Main function to perform the update
def main(product, version, status, additional_info):
    # Step 1: Get the current page content
    page_data = get_page_content()
    content = page_data['body']['storage']['value']
    version_number = page_data['version']['number']
    title = page_data['title']

    # Step 2: Parse the content to find and update the specific table row
    soup = BeautifulSoup(content, 'html.parser')
    # Locate the specific table by identifying it with a unique attribute or content
    table = soup.find('table', {'data-layout': 'default'})
    if table:
        # Iterate over the rows to find the matching product
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if cells and cells[0].get_text(strip=True) == product:
                # Update the cells with new data
                cells[1].string = version
                cells[2].string = status
                cells[3].string = additional_info
                break
        else:
            print('Specified product not found in the table.')
            return
    else:
        print('Table not found.')
        return

    # Convert the modified content back to a string
    new_content = str(soup)

    # Step 3: Update the page with the new content
    update_page_content(new_content, version_number, title)
    print('Page updated successfully.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update Confluence table row.')
    parser.add_argument('product', help='Product name')
    parser.add_argument('version', help='Product version')
    parser.add_argument('status', help='Pipeline status')
    parser.add_argument('additional_info', help='Additional information')
    args = parser.parse_args()
    main(args.product, args.version, args.status, args.additional_info)
