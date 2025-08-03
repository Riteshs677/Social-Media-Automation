# It scrape max 4 URLs
import asyncio
from openpyxl import Workbook
from itertools import zip_longest
from playwright.async_api import async_playwright
import os

USER_DATA_DIR = "user_data"  

async def extract_image_posts_from_profile(page, profile_username, max_urls=6):
    profile_url = f"https://www.instagram.com/{profile_username}/"
    await page.goto(profile_url, timeout=60000)

    try:
        await page.wait_for_selector('a[href*="/p/"]', timeout=60000)
        post_elements = await page.query_selector_all('a[href*="/p/"]')

        urls = []
        seen = set()

        for element in post_elements:
            if len(urls) >= max_urls:
                break

            href = await element.get_attribute('href')
            if href and "/p/" in href:
                full_url = f"https://www.instagram.com{href}"
                if full_url not in seen:
                    urls.append(full_url)
                    seen.add(full_url)

        return urls
    except Exception as e:
        print(f" Failed to extract from @{profile_username}: {e}")
        return []

async def extract_multiple_to_columnar_excel(usernames, output_file="instagram_profiles.xlsx", max_urls=6):
    async with async_playwright() as p:
        #
        context = await p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless= False # Set to True later once login is cached
        )
        page = await context.new_page()

        
        print(" Please log in to Instagram manually if not already logged in...")
        await page.goto("https://www.instagram.com", timeout=60000)
        await asyncio.sleep(40)  
        # Next runs will reuse session

        all_data = {}

        for username in usernames:
            print(f" Extracting from @{username}...")
            urls = await extract_image_posts_from_profile(page, username, max_urls=max_urls)
            all_data[username] = urls
            print(f" Found {len(urls)} image URLs for @{username}")

        
        wb = Workbook()
        ws = wb.active
        ws.title = "Instagram Image Posts"

        ws.append(list(all_data.keys()))
        for row in zip_longest(*all_data.values(), fillvalue=""):
            ws.append(row)

        wb.save(output_file)
        print(f"\n All data saved to '{output_file}'")

        await context.close()

# List of Instagram usernames
usernames = ["techcrunch", "googledeepmind", "aifolksorg"]

asyncio.run(extract_multiple_to_columnar_excel(usernames, max_urls=6))
