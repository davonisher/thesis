from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time
from random import choice
import asyncio

#args=[
#        '--proxy-server=http://127.0.0.1:24001',  # Vervang dit door het adres van uw proxy server 
#        ]

#Create an empty dictionary to store the DataFrames
dfs = {}

# random user agents list
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48',
]
# Main function
async def main():

    #periods must be changed to skip already scraped periods
    periods = ['october', 'september', 'august', 'july', 'june', 'may', 'april', 'march', 'february', 'january', 'december', 'november', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015']
    #run the browser
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True) #, args=['--proxy-server=http://127.0.0.1:24001']) # Adding proxy

        # Loop through the periods
        try:
            for period in periods:
                # Create an empty list to store the data
                data_list = []
                # Randomly select a user agent from the list
                user_agent = choice(USER_AGENTS)
                # Create a new context
                context = await browser.new_context(user_agent=user_agent)
                # Create a new page
                page = await context.new_page()
                # Try to scrape the data
                try:
                    # Headers to be used in the request
                    await page.set_extra_http_headers({
                        'Referer': 'https://theresanaiforthat.com/',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            })
                    # Go to the page
                    await page.goto(f'https://theresanaiforthat.com/period/{period}/', wait_until="load")
                    # Wait for the page to load
                    await page.wait_for_timeout(15000)  
                    # Get the HTML content of the page
                    html_content = await page.content()
                    # Parse the HTML content
                    soup = BeautifulSoup(html_content, 'html.parser')
                    # Find all the items
                    items = soup.find_all('li', attrs={'data-name': True, 'data-task': True, 'data-url': True})

                    # Print the number of items scraped
                    print(f"Period: {period}, Number of items scraped: {len(items)}")
                    
                    # Loop through the items and extract the data
                    for item in items:
                        # Extract the data
                        data_name = item.attrs.get('data-name')
                        data_task = item.attrs.get('data-task')
                        data_url = item.attrs.get('data-url')
                        price_elem = item.select_one('div.available_starting a.ai_launch_date')
                        price = price_elem.text.strip() if price_elem else 'N/A'
                        saves_elem = item.select_one('div.saves')
                        saves = saves_elem.text.strip() if saves_elem else 'N/A'
                        likes_elem = item.select_one('div.comments')
                        likes = likes_elem.text.strip() if likes_elem else 'N/A'
                        stars_elem = item.select_one('span.star.star-empty')
                        stars = float(stars_elem.next_sibling.strip()) if stars_elem and stars_elem.next_sibling else 'N/A'
                        data_list.append([data_name, data_task, data_url, price, saves, likes, stars, period])
                    
                    # Wait for 8 seconds to mimic human behavior
                    await asyncio.sleep(8)  # Adding a delay of 8 seconds between requests
                      
                    # Create a DataFrame for the current period and store it in the dictionary
                    dfs[period] = pd.DataFrame(data_list, columns=['Name', 'Task', 'URL', 'Price', 'Saves', 'Likes', 'Stars', 'Period'])

                    # Print log message
                    print(f"Data collected for {period} is stored in a separate DataFrame.")
                    
                     # Close the context
                    await context.close()

            # Print log if error occurs
                except Exception as e:
                    print(f"Error processing period {period}: {str(e)}")

            # Print log if error occurs
        except Exception as e:
            print(f"Error initializing browser or context: {str(e)}")
        # Close the browser
        finally:
            browser.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    # 


