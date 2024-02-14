import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import re

async def scrape_info(page):

    # Search for all product elements
    product_elements = await page.query_selector_all('div[class^="styles_item__jDvwG"]')

    # List for storing scraped data
    scraped_data = []

    # Loop through each product element to extract the data
    for product_element in product_elements:
        # Name of tool
        name_element = await product_element.query_selector('div[data-test="product-item-name"]')
        product_name = await name_element.inner_text() if name_element else 'N/A'

        # URL of tool
        url_element = await product_element.query_selector('a[target="_blank"]')
        product_url = await url_element.get_attribute('href') if url_element else 'N/A'

        followers_element = await page.query_selector('div.styles_followersCount__Auv5S')
        followers_count = await followers_element.inner_text() if followers_element else 'N/A'

        # Counted stars
        filled_stars_count = 0
        for i in range(1, 6):  # Loop door 5 sterren
            star_selector = f'svg[data-test="star-{i}-filled"]'
            if await page.query_selector(star_selector):
                filled_stars_count += 1

        reviews_element = await page.query_selector('a.styles_review__P4dw9 > div.ml-1.color-lighter-grey.fontSize-12.fontWeight-400')
        reviews_text = await reviews_element.inner_text() if reviews_element else 'N/A'
        
        # Main image URL
        image_element = await product_element.query_selector('img.styles_thumbnail__Y9ZpZ')
        image_url = await image_element.get_attribute('srcset') if image_element else ''

            # if not image_url, try to get it from the source element
        if not image_url:
            source_element = await page.query_selector('source')
            image_url = await source_element.get_attribute('src') if source_element else ''
        

        scraped_data.append((product_name, product_url, image_url, followers_count, filled_stars_count, reviews_text))

    return scraped_data

async def main():
    final_info_list_ph = []
    base_url = "https://www.producthunt.com/topics/artificial-intelligence?order=most_followed"
    args = ['--proxy-server=http://127.0.0.1:24000']

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=args)
        context = await browser.new_context()
        
        page = await context.new_page()
        await page.goto(base_url)

        
        # max 10000 scrolls
        for _ in range(10000):  
            # Scroll down to the bottom of the page
            await page.keyboard.press('Space')
            # Wait for the next set of items to load
            await asyncio.sleep(2) 
        
        # Scrape the page
        info_ph = await scrape_info(page)
        # Append the data to the list
        final_info_list_ph.extend(info_ph)

        await context.close()

    # Save reviews to CSV
    comments_df = pd.DataFrame(final_info_list_ph, columns=['product_name', 'product_url', 'product_image_url. ', 'followers_count', 'filled_stars_count', 'reviews_count'])
    comments_df.to_csv('product_hunt_general_info5.csv', index=False)

# Run the main function
asyncio.run(main())

