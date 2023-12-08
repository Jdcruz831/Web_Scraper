import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

seed = "https://www.simplehtmlguide.com/images.php"
url = [seed]

#Adding images to the html
def print_img(url):
     with open("Scraped_data_Pictures.html", 'a', encoding='utf-8') as file:
        # Append the formatted text to the file
        file.write(f'<img src="{url}" alt="Embedded Image">\n')

#Purple to represent each new page scrapped. 
def print_p(text, filename):
     with open(filename, 'a', encoding='utf-8') as file:
        # Append the formatted text to the file
        file.write(f'<b><p style="color:green;">{text}</p></b>\n')

 #Green bold to represend found then add to html
def print_b(text, not_bold, filename):
     with open(filename, 'a', encoding='utf-8') as file:
         file.write(f'<i><p style="color:purple;">{text}</p></i><p>{not_bold}</p>\n')
     

 #print red to mark no atrribute found to html page. 
def print_r(text, filename):
     with open(filename, 'a', encoding='utf-8') as file:
        # Append the formatted text to the file
        file.write(f'<i><p style="color:red;">{text}</p></i>\n')

#L for list items text to be added as well. 
def print_li(text):
     with open("Scraped_data_lists.html", 'a', encoding='utf-8') as file:
        # Append the formatted text to the file
        file.write(f'<p style="color:black;">{text}</p>\n')

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
        print(f"Failed to retrieve the HTML content. Status Code: {response.status_code}")


    #Try catch statment for tittle
    try: 
        title = soup.title.text
        print_b("Tittle: ", title, "Scraped_data_Titles.html")

    except AttributeError as e:
        print_r("No title attribute found.", "Scraped_data_Titles.html")


    #Try catch statment for tittle
    try: 
        img_tags = soup.find.all('img')

        for img_tag in img_tags:
            img_url = img_tag['src']
            print_img(img_tag)

    except AttributeError as e:
        print_r("No Images found.", "Scraped_data_Pictures.html")     


    #Try catch statment for loop through every heading tag
    for i in range(1,7):
        try:
                    #find(f'h{i}') is just to insted the i
            heading = soup.find(f'h{i}').text
            print_b("Heading: ", heading, "Scraped_data_Headings.html")
                    #find(f'h{i}') is just to insted the i
        except AttributeError as e:
            print_r(f"No h{i} text attribute found.", "Scraped_data_Headings.html")


    #Try Catch for text of Paragraph 
    try:
        paragraph = soup.p.text
        print_b("Paragraph: ", paragraph, "Scraped_data_Paragraphs.html")

    except AttributeError as e:
        print_r("No p text attribute found.", "Scraped_data_Paragraphs.html")  


    #try catch for print the list items
    try:  
        list_items = [li.text for li in soup.ul.find_all('li')]
        print_b("List Items:", "", "Scraped_data_lists.html")
        for item in list_items:
            print_li(f"- {item}")

    except AttributeError as e:
        print_r("No list items attribute found.", "Scraped_data_lists.html")

#Creates HTML Page on start
def create_html_file(filename, text):
    
    html_content = f'<!DOCTYPE html>\n<html>\n<head><title>Formatted Text</title></head>\n<body>\n<b>{text}</b>\n</body>\n</html>'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)



#------MAIN-----#
create_html_file("Scraped_data_Titles.html", "Scraped Images")
create_html_file("Scraped_data_Pictures.html", "Scraped Pictures")
create_html_file("Scraped_data_Headings.html", "Scraped Headings")
create_html_file("Scraped_data_Paragraphs.html", "Scraped Text")
create_html_file("Scraped_data_lists.html", "Scraped lists")

url.extend(extract_links(seed))

print("Runinng............")

for i in range(len(url)):

    print_p(f"PAGE: {i+1}" + "URL: " + url[i], "Scraped_data_Titles.html")
    print_p(f"PAGE: {i+1}" + "URL: " + url[i], "Scraped_data_Pictures.html")
    print_p(f"PAGE: {i+1}" + "URL: " + url[i], "Scraped_data_Headings.html")
    print_p(f"PAGE: {i+1}" + "URL: " + url[i], "Scraped_data_Paragraphs.html")
    print_p(f"PAGE: {i+1}" + "URL: " + url[i], "Scraped_data_lists.html")
    scrap(url[i])
print("DONE")