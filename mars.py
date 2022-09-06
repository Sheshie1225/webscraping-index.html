# Import
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# mars news site
url = 'https://redplanetscience.com/'
browser.visit(url)

browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object
html = browser.html
mars_soup = soup(html, 'html.parser')

slide = mars_soup.select_one('div.list_text')

slide.find('div', class_='content_title')

marsnews_title = slide.find('div', class_='content_title').get_text()
marsnews_title


# find the paragraph text
paragraph = slide.find('div', class_='article_teaser_body').get_text()
paragraph


# spaces images URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
image_click = browser.find_by_tag('button')[1]
image_click.click()


html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find image url
image_url = img_soup.find('img', class_='fancybox-image').get('src')
image_url

# create an absolute url
abs_url = f'https://spaceimages-mars.com/{abs_url}'
abs_url


facts_df = pd.read_html('https://galaxyfacts-mars.com')[0]
facts_df.head()

facts_df.columns=['Description', 'Mars', 'Earth']
facts_df.set_index('Description', inplace=True)
facts_df

#html
facts_df.to_html()


# 1. URL
url = 'https://marshemispheres.com/'

browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Retrieve the image urls and titles
for hemis in range(4):
    # Browse
    browser.links.find_by_partial_text('Hemisphere')[hemis].click()
    
    # Parser
    html = browser.html
    hemi_soup = soup(html,'html.parser')
    
    # Scraping
    title = hemi_soup.find('h2', class_='title').text
    img_url = hemi_soup.find('li').a.get('href')
    
    # Store findings and add to list
    hemispheres = {}
    hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
    hemispheres['title'] = title
    hemisphere_image_urls.append(hemispheres)
    
    # Browse back
    browser.back()

# Quit browser
browser.quit()


# 4. Print list
hemisphere_image_urls
