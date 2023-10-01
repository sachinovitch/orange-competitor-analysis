from playwright.sync_api import sync_playwright
import json


URL = 'https://mobilevikings.be/en/offer/subscriptions/'


def extract_subscription_data(page):
    subscription_data = []

    page.wait_for_selector('.PostpaidOption')

    subscription_elements = page.query_selector_all('.PostpaidOption')

    for id, subscription_element in enumerate(subscription_elements, start=1):
        mobile_data = subscription_element.query_selector('.PostpaidOption__dataAmount__text').inner_text().lower().replace('gb', '').strip()
        network = subscription_element.query_selector('.PostpaidOption__dataAmount__networkTag')
        if network.query_selector('.FourGFiveG--has5g'):
            network = '5g'
        else:
            network = '4g'
        calls_texts = subscription_element.query_selector('.PostpaidOption__voiceTextAmount').inner_text().lower()
        price_per_month = subscription_element.query_selector('.monthlyPrice__price').inner_text().replace(',-', '')

        subscription_data.append({
            'id': id,
            'price_per_month': price_per_month,
            'mobile_data_gb': mobile_data,
            'network': network,
            'calls_texts': calls_texts
        })

    return subscription_data


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)
        page.get_by_role("button", name="Accept").click()

        subscription_data = extract_subscription_data(page)

        data_dict = {'subscription_plans': subscription_data}

        json_data = json.dumps(data_dict, indent=4)

        print(json_data)

        browser.close()


if __name__ == "__main__":
    main()
