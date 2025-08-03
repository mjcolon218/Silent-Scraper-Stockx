import logging
import sys
import os
from playwright.sync_api import sync_playwright, TimeoutError
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def parse_price(price_str):
    try:
        return float(price_str.strip().replace('$', '').replace(',', ''))
    except (ValueError, AttributeError):
        return None

def fetch_sneaker_data(search_term):
    try:
        url = f"https://stockx.com/search?s={search_term.replace(' ', '%20')}"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_selector('div[id="product-results"]', timeout=10000)

            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')

            results_div = soup.find('div', attrs={'id': 'product-results'})
            if not results_div:
                logger.warning("❌ Results container not found.")
                return []

            product_tiles = results_div.find_all("div", {"data-testid": "ProductTile"})

            sneakers = []
            for tile in product_tiles[:5]:
                a_tag = tile.find("a", href=True)
                link = "https://stockx.com" + a_tag["href"] if a_tag else "N/A"

                name_tag = tile.find("p")
                name = name_tag.text.strip() if name_tag else "N/A"

                price_tag = tile.find(string=lambda t: t and "$" in t)
                price_value = parse_price(price_tag)

                if price_value is not None:
                    sneakers.append({
                        "name": name,
                        "price": price_value,
                        "link": link
                    })
                else:
                    logger.warning(f"⚠️ Skipped product '{name}' due to invalid price: {price_tag}")

            return sneakers

    except TimeoutError as te:
        logger.error(f"❌ Playwright timeout: {te}")
        return []
    except Exception as e:
        logger.exception(f"❌ Unexpected error in fetch_sneaker_data: {e}")
        return []

if __name__ == "__main__":
    #results = fetch_sneaker_data("Air Jordan 4 Retro")
    #for sneaker in results:
        #print(f"{sneaker['name']} - ${sneaker['price']} - {sneaker['link']}")
    #print(results)
    fetch_sneaker_data()