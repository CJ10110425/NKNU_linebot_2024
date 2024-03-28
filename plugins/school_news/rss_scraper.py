import requests
import xml.etree.ElementTree as ET
import json
import os

class RssScraper:
    def __init__(self, url = "https://news.nknu.edu.tw/nknu_News/RSS.ashx"):
        self.url = url
        self.json_filename = os.path.dirname(__file__)+"/src/school_news_info.json"
    
    def fetch_and_convert_to_json(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            rss_content = response.content.decode("utf-8")
            root = ET.fromstring(rss_content)
            items = []
            for item in root.findall('.//item'):
                item_dict = {}
                for child in item:
                    if child.tag == 'title':
                        item_dict['title'] = child.text.strip() if child.text else ""
                    elif child.tag == 'description':
                        item_dict['description'] = child.text.strip() if child.text else ""
                    elif child.tag == 'link':
                        item_dict['link'] = child.text.strip() if child.text else ""
                    elif child.tag == 'pubDate':
                        item_dict['pubDate'] = child.text.strip() if child.text else ""
                    elif child.tag == 'category':
                        item_dict['category'] = child.text.strip() if child.text else ""
                items.append(item_dict)
            
            with open(self.json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(items, json_file, ensure_ascii=False, indent=4)

    def read_json_by_category(self, category):
        with open(self.json_filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            category_data = [item for item in data if 'category' in item and item['category'] == category]
            return category_data
    
if __name__ == "__main__":
    
    scraper = RssScraper()
    scraper.fetch_and_convert_to_json()

    # category = "行政資訊"  
    # category_data = scraper.read_json_by_category(category)
    # for i in category_data[:1]:
    #     # 使用 BeautifulSoup 解析 HTML
    #     soup = BeautifulSoup(i["description"], 'html.parser')

    #     # 提取純文字內容
    #     description_text = soup.get_text(separator="\n", strip=True)
    #     print(description_text)
    # soup = BeautifulSoup(category_data["description"], 'html.parser')

    # description_text = soup.get_text(separator="\n", strip=True)
    # print(description_text)