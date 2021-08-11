from bs4 import BeautifulSoup
from splinter import Browser
import requests
import os.path
import pandas as pd

def get_page(url):
    executable_path = {"executable_path": "C:/Users/Jason/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    browser.quit()
    return html

def get_soup(url, nickname):
    if not os.path.isfile(nickname):
        html = get_page(url)
        with open(nickname, 'w') as file:
            file.write(html)
    with open(nickname, 'r') as html:
        soup = BeautifulSoup(html, 'html.parser')
    return soup

#########################
## RedPlanet news articles
#########################
soup = get_soup("https://redplanetscience.com/", "redplanet.html")

red_planet_titles = []
red_planet_text = []
for div in soup.find_all("div"):
    if 'content_title' in div['class']:
        red_planet_titles.append(div.text)
    if 'article_teaser_body' in div['class']:
        red_planet_text.append(div.text)

#########################
## SpaceImages Mars image
#########################

space_images_url = "https://spaceimages-mars.com/"
soup = get_soup(space_images_url, "spaceimages.html")

mars_image_url = space_images_url+'/'+ soup.find("img", class_="headerimage")['src']
print("\n\n"+"="*30+"\n"+mars_image_url+"\n\n")

#########################
## GalaxyFacts Mars Table
#########################

soup = get_soup("https://galaxyfacts-mars.com/", "mars_facts.html")

mars_table = soup.find('table', class_= 'table-striped')
mars_df = pd.read_html(str(mars_table))[0]
mars_table_html_from_pd = mars_df.to_html()

#########################
## GalaxyFacts Mars Table
#########################

galaxy_facts = requests.get("https://marshemispheres.com/")
soup = BeautifulSoup(galaxy_facts, "html.parser")

# soup = get_soup("https://marshemispheres.com/", "hemispheres_main")



# results = browser.find_by_xpath(xpath)
# img = results[0]
# img.click()

# # Use the requests library to download and save the image from the `img_url` above
# import shutil
# response = requests.get('http:'+img_url, stream=True)
# with open('img.png', 'wb') as out_file:
#     shutil.copyfileobj(response.raw, out_file)

# from IPython.display import Image
# Image(url='img.png')
