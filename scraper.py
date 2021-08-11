from bs4 import BeautifulSoup
from splinter import Browser
import requests
import os.path
import pandas as pd
import re

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

def get_articles():
    soup = get_soup("https://redplanetscience.com/", "redplanet.html")

    red_planet_titles = []
    red_planet_text = []
    for div in soup.find_all("div"):
        if 'content_title' in div['class']:
            red_planet_titles.append(div.text)
        if 'article_teaser_body' in div['class']:
            red_planet_text.append(div.text)
    return zip(red_planet_titles, red_planet_text)


#########################
## SpaceImages Mars image
#########################

def get_mars_image():
    space_images_url = "https://spaceimages-mars.com/"
    soup = get_soup(space_images_url, "spaceimages.html")

    mars_image_url = space_images_url+'/'+ soup.find("img", class_="headerimage")['src']
    return mars_image_url


#########################
## GalaxyFacts Mars Table
#########################

def get_mars_fact_table():
    soup = get_soup("https://galaxyfacts-mars.com/", "mars_facts.html")

    mars_table = soup.find('table', class_= 'table-striped')
    mars_df = pd.read_html(str(mars_table))[0]
    mars_table_html_from_pd = mars_df.to_html()
    return mars_table_html_from_pd

#########################
## MarsHemispheres enhanced images
#########################

def get_mars_hemi_imgs():
    galaxy_url = "https://marshemispheres.com/"
    galaxy_facts = requests.get(galaxy_url)
    soup = BeautifulSoup(galaxy_facts.text, "html.parser")

    links = []
    names = []
    for div in soup.find_all("div", class_="description"):
        a = div.find('a')
        links.append(a['href'])
        names.append(a.find('h3').string)

    # print(names)
    # print(links)

    img_links = []
    for link in links:
        link_page = requests.get(f'{galaxy_url}{link}')
        link_soup = BeautifulSoup(link_page.text, 'html.parser')
        dt = link_soup.find(string="Filename").parent
        image_link = dt.next_sibling.next_sibling.find('a')['href']
        img_links.append(f'{galaxy_url}{image_link}')

    # print(img_links)

    mars_hemispheres = []
    for name, link in zip(names, img_links):
        mars_hemispheres.append({'title': name, 'img_url' : link})

    # print(mars_hemispheres)
    return mars_hemispheres



