from bs4 import BeautifulSoup
import requests
from lxml import etree
import json
import pandas as pd


class Scraper:
    def __init__(self):
        self.data = []
        self.n = 0

    @staticmethod
    def get_value(attr):
        if len(attr) == 0:
            return None
        return attr[0]

    @staticmethod
    def clean_html(html_content):
        if not html_content:
            return None
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text()



    def get_content(self, link):
        if link:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, "lxml")

            if "https://www.amazon.science" in link:
                article = soup.find_all("article", class_="ArticlePage-mainContent")[0]
                html_content = article.find("div", class_="ArticlePage-articleContainer")

            elif "https://siliconangle.com" in link:
                html_content = soup.find("div", class_="single-post-content")
                remove_div = html_content.find("div", class_="silic-after-content")

                if remove_div:
                    remove_div.decompose()

            return html_content.get_text()

        return None
    



    def get_analyticsindiamag_data(self):
        xml_url = "https://analyticsindiamag.com/feed/"
        response = requests.get(xml_url)
        xml_tree = etree.fromstring(response.content)
        namespaces = {"content": "http://purl.org/rss/1.0/modules/content/"}
        items = xml_tree.xpath("//item")

        for item in items:
            guid = item.xpath("guid/text()")
            title = item.xpath("title/text()")
            link = item.xpath("link/text()")
            pub_date = item.xpath("pubDate/text()")
            description = item.xpath("description/text()")
            content_encoded = item.xpath("content:encoded/text()", namespaces=namespaces)

            cleaned_description = self.clean_html(self.get_value(description))
            cleaned_content = self.clean_html(self.get_value(content_encoded))

            record = {
                "guid": self.get_value(guid),
                "title": self.get_value(title),
                "link": self.get_value(link),
                "pub_date": self.get_value(pub_date),
                "description": cleaned_description,
                "content": cleaned_content,
            }

            self.data.append(record)
            self.n += 1
            # print(self.n)
            # print(record)

        return self.data




    def get_amazon_science_data(self):
        url = "https://www.amazon.science/index.rss"
        response = requests.get(url)
        xml_tree = etree.fromstring(response.content)
        items = xml_tree.xpath("//item")

        for item in items:
            guid = item.xpath("guid/text()")
            title = item.xpath("title/text()")
            link = self.get_value(item.xpath("link/text()"))
            pub_date = item.xpath("pubDate/text()")
            description = item.xpath("description/text()")
            content = self.get_content(link)

            record = {
                "guid": self.get_value(guid),
                "title": self.get_value(title),
                "link": link,
                "pub_date": self.get_value(pub_date),
                "description": self.get_value(description),
                "content": content,
            }

            self.data.append(record)
            self.n += 1
            if self.n == 10:
                break
            # print(self.n)
            # print(record)

        return self.data
    


    def get_siliconangle_data(self):
        url = "https://siliconangle.com/category/ai/feed/"
        response = requests.get(url)
        xml_tree = etree.fromstring(response.content)
        items = xml_tree.xpath("//item")

        for item in items:
            guid = item.xpath("guid/text()")
            title = item.xpath("title/text()")
            link = self.get_value(item.xpath("link/text()"))
            pub_date = item.xpath("pubDate/text()")
            description_tag = item.xpath("description/text()")

            if self.get_value(description_tag):
                description_tag_content = BeautifulSoup(self.get_value(description_tag), "lxml")
                div_content = description_tag_content.find_all("div")[1].text
                paragraph_content = description_tag_content.find_all("p")[0].text
                description = div_content + "\n" + paragraph_content
            else:
                description = self.get_value(description_tag)

            content = self.get_content(link)

            record = {
                "guid": self.get_value(guid),
                "title": self.get_value(title),
                "link": link,
                "pub_date": self.get_value(pub_date),
                "description": description,
                "content": content,
            }

            self.data.append(record)
            self.n += 1
            if self.n == 10:
                break
            # print(self.n)
            # print(record)

        return self.data


    def get_data(self):
        return self.get_amazon_science_data()
        return self.get_siliconangle_data()
        return self.get_analyticsindiamag_data()


# Usage example
scraper = Scraper()
data = scraper.get_data()
# print(data)
df = pd.DataFrame(data)
# df.to_parquet("src/DATA/data.parquet")
df.to_csv("data.csv")

# with open("src/DATA/data-test.json", "w", encoding="utf-8") as json_file:
#     json.dump(data, json_file, indent=4, ensure_ascii=False)
