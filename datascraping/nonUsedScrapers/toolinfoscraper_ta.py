
#
#
#
#
#
#
# THIS SCRAPER WORKS BUT GETS STUCK ON CLOUDFLARE PROTECTION AFTER A FEW ITERATIONS
# 
# This could be adjusted for future research to work properly
#
#
#
#
#
#

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
from random import choice
import asyncio
import logging
from random import randint
import re
import random


async def scrape_most_impacted_jobs(page):
    job_info_data = []

    # Vind de relevante sectie op de pagina
    jobs_section = await page.query_selector('div#most_impacted_jobs')

    # Controleer of de sectie bestaat
    if not jobs_section:
        return job_info_data

    # Vind alle 'a'-elementen (job links) binnen de sectie
    job_elements = await jobs_section.query_selector_all('a')

    for job_element in job_elements:
        # Extract de job link
        job_link = await job_element.get_attribute('href') if await job_element.get_attribute('href') else 'N/A'
        
        # Extract de job titel
        related_title_elem = await job_element.query_selector('span.related_job_name')
        related_title = await related_title_elem.text_content() if related_title_elem else 'N/A'
        
        # Extract overige gegevens
        impact_elem = await job_element.query_selector('span.related_impact')
        impact = await impact_elem.text_content() if impact_elem else 'N/A'
        impact_score = await impact_elem.get_attribute('data-score') if impact_elem else 'N/A'

        tasks_elem = await job_element.query_selector('span.related_tasks')
        tasks = await tasks_elem.text_content() if tasks_elem else 'N/A'

        ai_elem = await job_element.query_selector('span.related_ais')
        ai = await ai_elem.text_content() if ai_elem else 'N/A'

        # Vind de tool link
        tool_link_elem = await page.query_selector("#ai_top_link")
        tool_link = await tool_link_elem.get_attribute("href") if tool_link_elem else 'N/A'

        # Voeg de verzamelde job informatie toe aan de lijst
        job_info_data.append([job_link, related_title, impact, impact_score, tasks, ai, tool_link])

    return job_info_data

async def extract_general_info(page):
    data_list = []

    # Extract use case
    use_case_elem = await page.query_selector(".use_case")
    use_case = await use_case_elem.text_content() if use_case_elem else 'N/A'

    # Extract launch date
    launch_date_elem = await page.query_selector(".launch_date_top")
    launch_date = await launch_date_elem.text_content() if launch_date_elem else 'N/A'

    # Extract title
    title_elem = await page.query_selector(".title_inner")
    title = await title_elem.text_content() if title_elem else 'N/A'

    # Extract ratings count
    ratings_count_elem = await page.query_selector(".ratings_count")
    ratings_count = await ratings_count_elem.text_content() if ratings_count_elem else 'N/A'

    # Extract tool link
    tool_link_elem = await page.query_selector("#ai_top_link")
    tool_link = await tool_link_elem.get_attribute("href") if tool_link_elem else 'N/A'

    # Extract tags
    tag_elements = await page.query_selector_all("a.tag")
    tags_data = ', '.join([await tag.text_content() for tag in tag_elements]) if tag_elements else 'N/A'

    # Extract price data
    price_elem = await page.query_selector("span.tag.price")
    price_data = await price_elem.text_content() if price_elem else 'N/A'

    # Extract description data
    description_elem = await page.query_selector("div.description")
    description_data = await description_elem.text_content() if description_elem else 'N/A'

    # Voeg de geëxtraheerde data toe aan de lijst
    data_list.append([use_case, launch_date, title, ratings_count, tool_link, tags_data, price_data, description_data])
    return data_list


async def extract_reviews(page):
    comments_data = []
    
    # Select the comment elements directly with Playwright
    comment_elements = await page.query_selector_all("div#user_comments div.comment")

    if not comment_elements:
        return comments_data

    for comment_element in comment_elements:
        comment_id = await comment_element.get_attribute("data-id")
        user_id = await comment_element.get_attribute("data-user")
        # Extract de datum van de commentaar
        comment_date_elem = await comment_element.query_selector("div.comment_date")
        comment_date = await comment_date_elem.text_content() if comment_date_elem else 'N/A'
        
        # Extract de tekst van de commentaar
        comment_text_elem = await comment_element.query_selector("div.comment_body")
        comment_text = await comment_text_elem.text_content() if comment_text_elem else 'N/A'

        # Find the tool link with Playwright
        tool_link_elem = await page.query_selector("#ai_top_link")
        tool_link = await tool_link_elem.get_attribute("href") if tool_link_elem else 'N/A'

        comments_data.append([comment_id, user_id, comment_date, comment_text, tool_link])

    return comments_data
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36 Edg/102.0.1245.33',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 12; en-us; Pixel 5 Build/SP1A.210812.015) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
]





async def is_page_blocked(page):    
    cloudflare_elem = await page.query_selector("div#cf-wrapper")
    if cloudflare_elem:
        return True
    return False

async def scrape_page(context, full_url):
    # Randomly pick a user agent from the list
        
    page = await context.new_page()
    
    # Randomly select a user agent from the list
    user_agent = random.choice(USER_AGENTS)

    # Set the 'User-Agent' header using the randomly selected value and add proxy
    await page.set_extra_http_headers({'User-Agent': user_agent}, )

    #include prxy stated before

    #if previous_url:
      #  headers['Referer'] = previous_url

    # Set HTTP headers
    #await page.set_extra_http_headers(headers)
    #await page.set_default_navigation_timeout(60000)  # Set a reasonable timeout
      # Wacht een willekeurige tijd tussen 5 en 15 seconden
    await asyncio.sleep(randint(1, 4))

    await page.goto(full_url, wait_until="domcontentloaded", timeout=60000)
    #await page.wait_for_load_state(state="networkidle")
    
    if await is_page_blocked(page):
        return full_url, None, None, None  

    job_info_data = await scrape_most_impacted_jobs(page)
    general_info = await extract_general_info(page)
    reviews = await extract_reviews(page)
    # wait for a couple of seconds to close the page
    await asyncio.sleep(4)
    #close the page after 20 tabs are opened
    
    await page.close()

    return full_url, general_info ,reviews, job_info_data


args = ['--proxy-server=http://127.0.0.1:24001']
async def main():
    base_url = "https://theresanaiforthat.com"
    urls_df = pd.read_csv("/Users/macbook/thesis/new/code/data/data_aitools_links.csv")
    all_urls = [f"{base_url}{suffix}" for suffix in urls_df['url_content'].tolist()][740:750]
    #0-1000
    batch_size = 500
    sub_batch_size = 3

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=args)
        context = await browser.new_context()

        for batch in range(0, len(all_urls), batch_size):
            final_data_list = []
            final_reviews_list = []
            job_info_df = []
            geblokkeerde_urls = []
            batch_urls = all_urls[batch:batch+batch_size]

            for i in range(0, len(batch_urls), sub_batch_size):
                sub_batch_urls = batch_urls[i:i+sub_batch_size]
                tasks = [scrape_page(context, url) for url in sub_batch_urls]
                results = await asyncio.gather(*tasks)
                print(f"Sub-batch {i // sub_batch_size + 1} van batch {batch + 1} is voltooid.")

                for full_url, general_info, reviews, job_info_data in results:
                    if general_info is None:
                        geblokkeerde_urls.append(full_url)
                    else:
                        final_data_list.extend(general_info)
                        final_reviews_list.extend(reviews)
                        job_info_df.extend(job_info_data)

            # Sla de resultaten van deze batch op in CSV-bestanden
            pd.DataFrame(final_data_list, columns=['Use Case', 'Launch Date', 'Title', 'Amount of Ratings', 'Tool Link', 'Tags', 'Price Data', 'Description']).to_csv(f'2tool_data_batch_{batch // batch_size + 1}.csv', index=False)
            pd.DataFrame(final_reviews_list, columns=['Comment ID', 'User ID','date', 'Comment Text', 'Tool Link']).to_csv(f'2reviews_batch_{batch // batch_size + 1}.csv', index=False)
            pd.DataFrame(job_info_df, columns=['Job Link', 'Related Title', 'Impact', 'Impact Score', 'Tasks', 'AI', 'Tool Link']).to_csv(f'2job_info_batch_{batch // batch_size + 1}.csv', index=False)
            pd.DataFrame(geblokkeerde_urls, columns=["Geblokkeerde URL"]).to_csv(f'2geblokkeerde_urls_batch_{batch // batch_size + 1}.csv', index=False)

        await browser.close()

asyncio.run(main())

def combine_batches_in_csv(batch_count, file_prefix):
    total_list = []

    for i in range(1, batch_count + 1):
        df = pd.read_csv(f'{file_prefix}_batch_{i}.csv')

        total_urls_scraped = len(pd.read_csv(f'tool_data_batch_{i}.csv'))
        total_blocked_urls = len(pd.read_csv(f'geblokkeerde_urls_batch_{i}.csv'))
        percentage_blocked_urls = (total_blocked_urls / total_urls_scraped) * 100
        print(f"Total amount of URLs scraped: {total_urls_scraped}")
        print(f"Total amount of blocked URLs: {total_blocked_urls}")
        print(f"Percentage of blocked URLs: {percentage_blocked_urls}%")
        total_list.append(df)

    # Combineer alle DataFrames
    final_df = pd.concat(total_list, ignore_index=True)

    # Sla de gecombineerde resultaten op in een nieuw bestand
    final_df.to_csv(f'final_{file_prefix}.csv', index=False)

    # Combineer batches in CSV-bestanden
    combine_batches_in_csv(batch_count, 'tool_data')
    combine_batches_in_csv(batch_count, 'reviews')
    combine_batches_in_csv(batch_count, 'job_info')
    combine_batches_in_csv(batch_count, 'geblokkeerde_urls')

