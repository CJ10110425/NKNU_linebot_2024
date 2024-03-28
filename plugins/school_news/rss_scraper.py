import requests
from lxml import etree
import json
import os
import re
from datetime import datetime, timedelta

class RssScraper:
    def __init__(self, url="https://news.nknu.edu.tw/nknu_News/RSS.ashx"):
        self.url = url
        self.json_filename = os.path.dirname(__file__) + "/src/school_news_info.json"
        self.last_updated_file = os.path.dirname(__file__) + "/src/last_updated.json"
        current_time = datetime.now()
        if self.should_update_rss(current_time):
            self.fetch_and_convert_to_json()
        else:
            print("RSS data 不需要更新") # FIXME:改成logging

    def fetch_and_convert_to_json(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            rss_content = response.content.decode("utf-8")
            parser = etree.XMLParser(recover=True)  # Ignore errors
            root = etree.fromstring(rss_content, parser=parser)
            items = []
            for item in root.findall('.//item'):
                item_dict = {}
                for child in item:
                    if child.tag == 'title':
                        item_dict['title'] = child.text.strip() if child.text else ""
                    elif child.tag == 'description':
                        item_dict['description'] = self.extract_chinese_descriptions(child.text.strip() if child.text else "")
                    elif child.tag == 'link':
                        item_dict['link'] = child.text.strip() if child.text else ""
                    elif child.tag == 'pubDate':
                        item_dict['pubDate'] = child.text.strip() if child.text else ""
                    elif child.tag == 'category':
                        item_dict['category'] = child.text.strip() if child.text else ""
                items.append(item_dict)

            with open(self.json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(items, json_file, ensure_ascii=False, indent=4)

            # Update last updated time
            self.update_last_updated_time()

    def update_last_updated_time(self):
        last_updated = {"last_updated": str(datetime.now())}
        with open(self.last_updated_file, 'w') as f:
            json.dump(last_updated, f)

    def get_last_updated_time(self):
        if os.path.exists(self.last_updated_file):
            with open(self.last_updated_file, 'r') as f:
                last_updated = json.load(f)
                return datetime.fromisoformat(last_updated["last_updated"])
        return datetime.min

    def should_update_rss(self, current_time):
        last_updated = self.get_last_updated_time()
        return (current_time - last_updated) > timedelta(hours=3)

    def extract_chinese_descriptions(self, description):
        if self.is_chinese(description):
            cleaned_description = self.clean_html_tags(description).strip()  # Clean HTML tags and &nbsp;, and strip leading/trailing whitespace
            cleaned_description = cleaned_description.replace('\n', '')  # Remove newline characters
            cleaned_description = ' '.join(cleaned_description.split())  # Remove extra whitespace between words
            return cleaned_description
        return "如需更多資訊請點擊以下按鈕"

    def is_chinese(self, text):
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False

    def clean_html_tags(self, text):
        cleanr = re.compile('<.*?>|&nbsp;')  # Compile regular expression to match HTML tags and &nbsp;
        cleantext = re.sub(cleanr, '', text)  # Use sub method to replace matched tags with an empty string
        return cleantext

if __name__ == "__main__":
    
    scraper = RssScraper()
    
