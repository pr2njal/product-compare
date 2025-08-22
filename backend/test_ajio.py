from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # show browser for debugging
        page = browser.new_page()
        page.goto("https://www.ajio.com/search/?text=shoes")  # test query
        page.wait_for_timeout(5000)  # wait 5s so page loads
        print("Title:", page.title())
        browser.close()

if __name__ == "__main__":
    run()
