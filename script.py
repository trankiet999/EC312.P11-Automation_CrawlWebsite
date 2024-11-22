import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# Base URL
base_url = "https://www.thewatchery.com/men-s-watches?p="

# CSV file setup
csv_file = "watch_data.csv"
fields = ["Thương hiệu", "Tên sản phẩm", "Giá", "Giảm giá", "URL sản phẩm", "URL hình ảnh"]

# Initialize CSV with headers
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

print("Đã tạo file CSV để lưu dữ liệu.")

# Headers for requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Pragma": "no-cache",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
}

# Google Form URL
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdBCbPUnY-HB6SlF9Z6RE4IYH5h3kuDCocvVlSyUZXspVKN2w/formResponse"

# Crawl and write data for each page
for i in range(1, 54):
    url = base_url + str(i)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_divs = soup.find_all("div", class_="product details product-item-details")
            page_data = []

            # Extract information from each product div
            for div in product_divs:
                try:
                    link_tag = div.find("a", class_="product-item-name")
                    brand = link_tag.find("span", class_="product-item-link product-item-brand").text.strip()
                    name = link_tag.find("span", class_="product-item-link product-item-name").text.strip()
                    product_url = link_tag['href']

                    price_tag = div.find("span", class_="price-wrapper")
                    price = price_tag.find("span", class_="price").text.strip() if price_tag else None

                    discount_tag = div.find("div", class_="price-savings price-container")
                    discount = discount_tag.find("span", class_="price-container").text.strip() if discount_tag else None

                    image_tag = div.find_previous("img")
                    image_src = image_tag['src'] if image_tag else None

                    product_data = {
                        "Thương hiệu": brand,
                        "Tên sản phẩm": name,
                        "Giá": price,
                        "Giảm giá": discount,
                        "URL sản phẩm": product_url,
                        "URL hình ảnh": image_src
                    }

                    page_data.append(product_data)

                    # Send data to Google Form
                    form_data = {
                        "entry.2034772756": name,
                        "entry.1958697120": brand,
                        "entry.1574603368": price,
                        "entry.764015854": discount,
                        "entry.440066910": product_url,
                        "entry.1202505989": image_src,
                        "fvv": 1
                    }

                    try:
                        post_response = requests.post(google_form_url, data=form_data)
                        if post_response.status_code == 200:
                            print(f"Đã gửi dữ liệu sản phẩm '{name}' vào Google Form.")
                        else:
                            print(f"Lỗi gửi dữ liệu sản phẩm '{name}'. Mã trạng thái: {post_response.status_code}")
                    except Exception as e:
                        print(f"Lỗi khi gửi dữ liệu sản phẩm '{name}' vào Google Form: {e}")

                except Exception as e:
                    print(f"Lỗi xử lý sản phẩm: {e}")

            # Write page data to CSV
            with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writerows(page_data)
            
            print(f"Đã ghi dữ liệu của trang {i} vào file CSV.")
        else:
            print(f"Không thể tải trang {i}. Mã trạng thái HTTP: {response.status_code}")
    except Exception as e:
        print(f"Lỗi kết nối tới trang {i}: {e}")

print("Quá trình crawl hoàn tất.")
