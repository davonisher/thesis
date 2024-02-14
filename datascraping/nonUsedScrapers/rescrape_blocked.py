

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
#


from toolinfoscraper_ta import scrape_page
import asyncio
import logging
from random import randint
import re
import pandas as pd
from playwright.async_api import async_playwright
from playwright.async_api import async_playwright
import pandas as pd
import asyncio
import os


async def rescrape_blocked_urls():
    # load the list of blocked URLs
    geblokkeerde_urls_df = pd.read_csv('/Users/macbook/thesis/geblokkeerde_urls.csv')
    geblokkeerde_urls = geblokkeerde_urls_df["Geblokkeerde URL"].tolist()

    batch_size = 500
    sub_batch_size = 3

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=['--proxy-server=http://127.0.0.1:24001'])
        context = await browser.new_context()

        for batch in range(0, len(geblokkeerde_urls), batch_size):
            final_data_list = []
            final_reviews_list = []
            job_info_df = []
            batch_urls = geblokkeerde_urls[batch:batch+batch_size]

            for i in range(0, len(batch_urls), sub_batch_size):
                sub_batch_urls = batch_urls[i:i+sub_batch_size]
                tasks = [scrape_page(context, url) for url in sub_batch_urls]
                results = await asyncio.gather(*tasks)

                for full_url, general_info, reviews, job_info_data in results:
                    if general_info is not None:
                        final_data_list.extend(general_info)
                        final_reviews_list.extend(reviews)
                        job_info_df.extend(job_info_data)

            # saves results
            pd.DataFrame(final_data_list, columns=['Use Case', 'Launch Date', 'Title', 'Amount of Ratings', 'Tool Link', 'Tags', 'Price Data', 'Description']).to_csv(f'rescraped_tool_data_batch_{batch // batch_size + 1}.csv', index=False)
            pd.DataFrame(final_reviews_list, columns=['Comment ID', 'User ID','date', 'Comment Text', 'Tool Link']).to_csv(f'rescraped_reviews_batch_{batch // batch_size + 1}.csv', index=False)
            pd.DataFrame(job_info_df, columns=['Job Link', 'Related Title', 'Impact', 'Impact Score', 'Tasks', 'AI', 'Tool Link']).to_csv(f'rescraped_job_info_batch_{batch // batch_size + 1}.csv', index=False)

        await browser.close()

asyncio.run(rescrape_blocked_urls())

# function to combine batches into a single CSV file
def auto_combine_batches_in_csv(file_prefix):
    # Zoek alle batch-bestanden
    batch_files = [f for f in os.listdir('.') if f.startswith(file_prefix) and f.endswith('.csv')]

    total_list = []
    for file in batch_files:
        df = pd.read_csv(file)
        total_list.append(df)

    # Combineer alle DataFrames
    final_df = pd.concat(total_list, ignore_index=True)

    # Sla de gecombineerde resultaten op in een nieuw bestand
    final_df.to_csv(f'final_{file_prefix}.csv', index=False)

# Combineer bestanden
auto_combine_batches_in_csv('rescraped_tool_data')
auto_combine_batches_in_csv('rescraped_reviews')
auto_combine_batches_in_csv('rescraped_job_info')