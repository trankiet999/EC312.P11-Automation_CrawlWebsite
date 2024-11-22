import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URL
BASE_URL = "https://www.thewatchery.com/men-s-watches?p="

# CSV file setup
CSV_FILE = "watch_data.csv"
FIELDS = ["Thương hiệu", "Tên sản phẩm", "Giá", "Giảm giá", "URL sản phẩm", "URL hình ảnh"]

# Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

# Cookies từ trình duyệt
COOKIES = {
    "cjConsent": "MHxOfDB8Tnww",
    "cjUser": "202b7727-96b4-4eb0-bc04-c0cf54d73b36",
    "GSIDuQxlIvMYat5N": "451c3d16-a366-45f4-8cf2-61c88f0b1f75",
    "STSID105284": "f4d4156d-96d9-4394-8ba7-96948cc71760",
    "_ga": "GA1.2.1928326463.1732169741",
    # ... (Thêm các key-value khác từ chuỗi cookies)
}

# Initialize CSV file
with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=FIELDS)
    writer.writeheader()

print("Đã tạo file CSV để lưu dữ liệu.")

# Crawl pages
for page in range(1, 54):  # Crawl từ trang 1 đến 53
    url = BASE_URL + str(page)
    try:
        response = requests.get(url, headers=HEADERS, cookies=COOKIES)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all("div", class_="product details product-item-details")

            page_data = []
            for product in products:
                try:
                    brand = product.find("span", class_="product-item-link product-item-brand").text.strip()
                    name = product.find("span", class_="product-item-link product-item-name").text.strip()
                    product_url = product.find("a", class_="product-item-name")['href']
                    price = product.find("span", class_="price").text.strip() if product.find("span", class_="price") else None
                    discount = product.find("div", class_="price-savings").text.strip() if product.find("div", class_="price-savings") else None
                    image_src = product.find("img")['src'] if product.find("img") else None

                    product_data = {
                        "Thương hiệu": brand,
                        "Tên sản phẩm": name,
                        "Giá": price,
                        "Giảm giá": discount,
                        "URL sản phẩm": product_url,
                        "URL hình ảnh": image_src,
                    }
                    page_data.append(product_data)

                except Exception as e:
                    print(f"Lỗi khi xử lý sản phẩm: {e}")

            # Write page data to CSV
            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writerows(page_data)

            print(f"Đã ghi dữ liệu trang {page} vào file CSV.")
        else:
            print(f"Không thể tải trang {page}. Mã trạng thái HTTP: {response.status_code}")
    except Exception as e:
        print(f"Lỗi khi tải trang {page}: {e}")

    time.sleep(2)  # Delay giữa các yêu cầu để tránh bị chặn

print("Quá trình crawl hoàn tất.")
