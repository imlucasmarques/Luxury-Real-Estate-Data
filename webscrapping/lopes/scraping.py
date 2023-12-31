from .extract import get_estate_page_soup, extract_estates_from_soup
from .config import get_lopes_listing_url
import pandas as pd


def webscrapping():
    print("==================> WEBSCRAPPING LOPES ")
    print("========= EXTRACTING ESTATES: PAGE 1 =========")
    [max_page, soup] = get_estate_page_soup(
        get_lopes_listing_url(), return_max_page=True
    )

    estates_data = extract_estates_from_soup(soup)

    for page in range(2, max_page + 1):
        print(f"========= EXTRACTING ESTATES: PAGE {page} OF {max_page} =========")
        estates_data.append(
            extract_estates_from_soup(get_estate_page_soup(get_lopes_listing_url(page)))
        )

    return pd.DataFrame(estates_data)
