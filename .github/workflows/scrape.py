import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.saudiexchange.sa/wps/portal/saudiexchange/ourmarkets/main-market-watch?locale=ar"


def extract_prices():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(URL)

    time.sleep(7)  # انتظار تحميل الجدول

    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    prices = {}

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            symbol = cells[-1].text.strip()      # رمز السهم
            close_price = cells[7].text.strip()  # سعر الإغلاق (حسب مكانه في الجدول)

            # تنظيف البيانات
            symbol = symbol.replace("\n", " ").split(" ")[-1]
            close_price = float(close_price)

            prices[symbol] = close_price
        except:
            continue

    driver.quit()

    # حفظ JSON
    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump(prices, f, ensure_ascii=False, indent=2)

    print("✓ تم حفظ الأسعار:", len(prices))


if __name__ == "__main__":
    extract_prices()
