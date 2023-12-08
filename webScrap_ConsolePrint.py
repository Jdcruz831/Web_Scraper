import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


seed = "https://www.w3schools.com/html/html_basic.asp"
url = [seed]

#Make Purple aka next page. 
def print_p(text):
    print("\033[3;95m" + text + "\033[0m")

#Make Bold method
def print_b(text, not_bold):
    print("\033[1;32m" + text + "\033[0m" + not_bold)

#Make Red aka no attribute found. 
def print_r(text):
    print("\033[3;31m" + text + "\033[0m")

#make sure url starts with http
def is_valid_url(url):
    return url.startswith(('http', 'https'))

#extract all sublinks and adds to url list. 
def extract_links(seed):
    response = requests.get(seed)
    sublinks = []

    #if pulled link susesfully
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor tags with an 'href' attribute
        for anchor_tag in soup.find_all('a', href=True):
            sublink = anchor_tag['href']

            # Join the relative URL with the base URL to get the absolute URL
            absolute_url = urljoin(seed, sublink)

            #check to make sure valid before adding to url then append to list
            if is_valid_url(absolute_url):
                sublinks.append(absolute_url)

    return sublinks


    

def scrap(url):

    # Make an HTTP request to get the HTML content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content with Beautiful Soup and 'html5lib'
        soup = BeautifulSoup(response.text, 'html5lib')


    else:
        print_r(f"Failed to retrieve the HTML content. Status Code: {response.status_code}")


    #Try catch statment for tittle
    try: 
        title = soup.title.text
        print_b("Tittle: ", title)

    except AttributeError as e:
        print_r("No title attribute found.")



    #Try catch statment for loop through every heading tag
    for i in range(1,7):
        try:
                    #find(f'h{i}') is just to insted the i
            heading = soup.find(f'h{i}').text
            print_b("Heading: ", heading)
                    #find(f'h{i}') is just to insted the i
        except AttributeError as e:
            print_r(f"No h{i} text attribute found.")


    #Try Catch for text of Paragraph 
    try:
        paragraph = soup.p.text
        print_b("Paragraph: ", paragraph)

    except AttributeError as e:
        print_r("No p text attribute found.")  


    #try catch for print the list items
    try:  
        list_items = [li.text for li in soup.ul.find_all('li')]
        print_b("List Items:", "")
        for item in list_items:
            print(f"- {item}")

    except AttributeError as e:
        print_r("No list items attribute found.")



url.extend(extract_links(seed))

for i in range(len(url)):
    print_p(f"PAGE: {i+1}")
    scrap(url[i])
