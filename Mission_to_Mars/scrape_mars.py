# ADJUST THE CODE TO USE IN THE APP.PY

from splinter import Browser, browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    marsnews_title, paragraph = mars_news(browser)
    img_urls_titles = mars_hemis(browser)

    data = {
        'news_title' : news_title,
        'news_paragraph' : news_paragraph,
        'featured_image' : featured_image(browser),
        'facts' : mars_facts(),
        'hemispheres' : img_urls_titles,
        'last_modified' : dt.datetime.now()
    }
    browser.quit()
    return data

def mars_news(browser):
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    mars_soup = soup(html, 'html.parser')

    try:
        slide = news_soup.select_one('div.list_text')
        marsnews_title = slide.find('div', class_='content_title').get_text()
        paragraph = slide.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return marsnews_title, paragraph

def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    image_click = browser.find_by_tag('button')[1]
    image_click.click()

    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        image_url = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None 

    abs_url = f'https://spaceimages-mars.com/{abs_url}'
    return abs_url

def mars_facts():
    try:
        facts_df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    facts_df.columns = ['Description','Mars','Earth']
    facts_df.set_index('Description', inplace=True)

    return facts_df.to_html()
    
def mars_hemis(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []
    for hemis in range(4):
        browser.links.find_by_partial_text('Hemisphere')[hemis].click()
        html = browser.html
        hemi_soup = soup(html, 'html.parser')
        title = hemi_soup.find('h2', class_='title').text
        img_url = hemi_soup.find('li').a.get('href')
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape_all())
