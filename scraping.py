# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_facts(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


def hemisphere_facts(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    mars_hemispheres_soup = soup(html, 'html.parser').find_all(class_='collapsible results')

    # Find the hemisphere names and partial links
    mars_hemispheres_title_list = [{ 'title': mars_hemispheres_soup[0].find_all('h3')[i].get_text(),
                                     'href': mars_hemispheres_soup[0].find_all(class_='item')[i].find_all('a')[0]['href']}
                                     for i, x in enumerate(mars_hemispheres_soup[0].find_all('h3'))]

    for hem in mars_hemispheres_title_list:
        # Visit hemisphere
        hem_str = f'https://marshemispheres.com/{hem["href"]}'
        browser.visit(hem_str)
        #browser.is_element_present_by_css('div.list_text', wait_time=3)
    
        # Get a href tags
        hemisphere_soup = soup(browser.html, 'html.parser').find_all(class_='downloads')[0].find_all('a')
    
        for d in hemisphere_soup:
            if d.get_text() == 'Sample':
                #print(f'https://marshemispheres.com/{d["href"]}')
                img_url = f'https://marshemispheres.com/{d["href"]}'
            
        hemisphere_image_urls.append({ 'title': hem['title'], 
                                   'img_url': img_url })
    
        #print(hem_str)
        browser.back()

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

    



if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())