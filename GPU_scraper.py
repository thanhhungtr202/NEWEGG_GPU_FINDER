from bs4 import BeautifulSoup
import requests
import re

search_term = input("Enter what you are searching for: ")
url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131"

webPage = requests.get(url).text
htmlDoc = BeautifulSoup(webPage, "html.parser")

#Looking for the element/tag with this class, then accessing its strong tag's text
pages_text = htmlDoc.find(class_ = "list-tool-pagination-text").strong.text
#Getting the final page
pages = int(pages_text.split("/")[-1])

search_results = {}
#Getting all items from all of the existing search result/page
for page in range(1, pages+1):
    url = f"https://www.newegg.com/p/pl?N=4131&d={search_term}&page={page}"
    webPage = requests.get(url).text
    htmlDoc = BeautifulSoup(webPage, "html.parser")

    #regex expression to find all that includes the search_term. first find() is to get access to the relevant div.
    items = htmlDoc.find(class_ = "item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell").find_all(string=re.compile(search_term))

    for item in items:
        link_tag = item.parent
        if link_tag.name != "a":
            continue

        link = link_tag["href"]
        price_tag = item.find_parent(class_ = "item-container")
        if price_tag.find(class_ = "price-current").strong != None:
            price = price_tag.find(class_ = "price-current").strong.string
            search_results[item] = {"price": int(price.replace(",", "")), "link": link}


sorted_results = sorted(search_results.items(), key=lambda x: x[1]["price"])

for item in sorted_results:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("---------------------------------------------")