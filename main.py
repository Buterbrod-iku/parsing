import csv
import json
import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_all_pages():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.0.2526 Yowser/2.5 Safari/537.36"
    }
    result = []

    r = requests.get(url="https://363-5005.рф/product-category/krepezh/shpilki/", headers=headers)

    if not os.path.exists("data"):
        os.mkdir("data")

    if not os.path.exists("data/pagin"):
        os.mkdir("data/pagin")

    with open("data/page_1.html", "w") as file:
        file.write(r.text)

    with open("data/page_1.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    allFirstType = soup.find_all("li", class_="product-category")
    mainHref = []

    for item in allFirstType:
        # print(item.find("h2").text + "---" + item.find("a").get("href"))
        mainHref.append({"header": item.find("h2").text, "href": item.find("a").get("href")})


    for item in range(0, len(mainHref)):
        urlr = mainHref[item]["href"]
        print(mainHref[item]["header"])
        block = {"id": item, "header": mainHref[item]["header"]}
        headerSecond = []

        rr = requests.get(url=urlr, headers=headers)

        with open(f"data/bolt{item}.html", "w") as file:
            file.write(rr.text)

        with open(f"data/bolt{item}.html") as file:
            srcr = file.read()

        soupSecond = BeautifulSoup(srcr, "lxml")
        allSecondType = soupSecond.find_all("li", class_="product-category")
        mainHrefSecond = []
        if len(allSecondType) != 0:
            for i in allSecondType:
                # print(i.find("h2").text + "---" + i.find("a").get("href"))
                mainHrefSecond.append({"header": i.find("h2").text, "href": i.find("a").get("href")})

            itemsProduct = []

            for item2 in range(0, len(mainHrefSecond)):
                itemHrefAll = []
                url2 = mainHrefSecond[item2]["href"]
                # result.append({"headerSecond": mainHrefSecond[item2]["header"]})
                blockTypeProduct = {"id": item2, "type": mainHrefSecond[item2]["header"]}
                itemsProductItems = []
                print(mainHrefSecond[item2]["header"] + "type")
                url22 = f"{url2}page/{1}/"

                r2 = requests.get(url=url22, headers=headers)

                with open(f"data/pagin/boltType{item2}.html", "w") as file:
                    file.write(r2.text)

                with open(f"data/pagin/boltType{item2}.html") as file:
                    src2 = file.read()

                soupLast = BeautifulSoup(src2, "lxml")

                # надо фиксить начинает не с первой страницы
                paginacia = soupLast.find_all("ul", class_="page-numbers")
                if len(paginacia) != 0:
                    pages_count = int(soupLast.find("ul", class_="page-numbers").find_all("a", class_="page-numbers")[-2].text)
                    for j in range(1, pages_count + 1):
                        pagUrl = f"{url2}/page/{j}/"

                        r4 = requests.get(url=pagUrl, headers=headers)

                        with open(f"data/pagin/boltType{j}.html", "w") as file:
                            file.write(r4.text)

                        with open(f"data/pagin/boltType{j}.html") as file:
                            src4 = file.read()

                        soupLast = BeautifulSoup(src4, "lxml")
                        itemHref = soupLast.find_all("li", "title")

                        for items in itemHref:
                            itemHrefAll.append(items.find("a").get("href"))

                    for g in range(0, len(itemHrefAll)):
                        request = requests.get(url=itemHrefAll[g], headers=headers)

                        with open(f"data/pagin/boltTypeItem.html", "w") as file:
                            file.write(request.text)

                        with open(f"data/pagin/boltTypeItem.html") as file:
                            src5 = file.read()

                        soupLastLast = BeautifulSoup(src5, "lxml")

                        if soupLastLast.find("h2", class_="single-post-title") is not None:
                            title = soupLastLast.find("h2", class_="single-post-title").text.strip()
                        else:
                            title = "нет"

                        price = soupLastLast.find("p", class_="price").text.strip()
                        text = soupLastLast.find("div", id="tab-description").find("p").text.strip()
                        tableTH = soupLastLast.find_all("th", class_="woocommerce-product-attributes-item__label")
                        tableTD = soupLastLast.find_all("td", class_="woocommerce-product-attributes-item__value")

                        data = []

                        for th in tableTH:
                            data.append(th.text.strip())
                        for td in tableTD:
                            data.append(td.text.strip())

                        image = soupLastLast.find_all("div", class_="woocommerce-product-gallery__image")
                        images = []

                        for img in image:
                            images.append(img.find("img").get("src"))

                        itemsProductItems.append({"id": g, "title": title, "price": price, "text": text, "table": data, "images": images})
                        print(g)
                else:
                    pagUrl = url2
                    r4 = requests.get(url=pagUrl, headers=headers)

                    with open(f"data/pagin/boltTypeNext.html", "w") as file:
                        file.write(r4.text)

                    with open(f"data/pagin/boltTypeNext.html") as file:
                        src4 = file.read()

                    soupLast = BeautifulSoup(src4, "lxml")
                    itemHref = soupLast.find_all("li", "title")

                    for items in itemHref:
                        itemHrefAll.append(items.find("a").get("href"))

                    for g in range(0, len(itemHrefAll)):
                        request = requests.get(url=itemHrefAll[g], headers=headers)

                        with open(f"data/pagin/boltTypeItem.html", "w") as file:
                            file.write(request.text)

                        with open(f"data/pagin/boltTypeItem.html") as file:
                            src5 = file.read()

                        soupLastLast = BeautifulSoup(src5, "lxml")

                        if soupLastLast.find("h2", class_="single-post-title") is not None:
                            title = soupLastLast.find("h2", class_="single-post-title").text.strip()
                        else:
                            title = "нет"

                        price = soupLastLast.find("p", class_="price").text.strip()
                        text = soupLastLast.find("div", id="tab-description").find("p").text.strip()
                        tableTH = soupLastLast.find_all("th", class_="woocommerce-product-attributes-item__label")
                        tableTD = soupLastLast.find_all("td", class_="woocommerce-product-attributes-item__value")

                        data = []

                        for th in tableTH:
                            data.append(th.text.strip())
                        for td in tableTD:
                            data.append(td.text.strip())

                        image = soupLastLast.find_all("div", class_="woocommerce-product-gallery__image")
                        images = []

                        for img in image:
                            images.append(img.find("img").get("src"))

                        itemsProductItems.append({"id": g, "title": title, "price": price, "text": text, "table": data, "images": images})
                        print(g)

                blockTypeProduct["items"] = itemsProductItems
                headerSecond.append(blockTypeProduct)
            block["headerSecond"] = headerSecond
            result.append(block)
        else:
            itemsProduct = []
            itemHrefAll = []
            soupSecond2 = BeautifulSoup(srcr, "lxml")
            itemHref2 = soupSecond2.find_all("li", "title")

            pagincia2 = soupSecond2.find_all("ul", class_="page-numbers")

            if len(pagincia2) != 0:
                pages_count = int(soupSecond2.find("ul", class_="page-numbers").find_all("a", class_="page-numbers")[-2].text)
                for j in range(1, pages_count + 1):
                    pagUrl = f"{urlr}/page/{j}/"

                    r4 = requests.get(url=pagUrl, headers=headers)

                    with open(f"data/pagin/boltType{j}.html", "w") as file:
                        file.write(r4.text)

                    with open(f"data/pagin/boltType{j}.html") as file:
                        src4 = file.read()

                    soupLast = BeautifulSoup(src4, "lxml")
                    itemHref = soupLast.find_all("li", "title")

                    for items in itemHref:
                        itemHrefAll.append(items.find("a").get("href"))

                for g in range(0, len(itemHrefAll)):
                    request = requests.get(url=itemHrefAll[g], headers=headers)

                    with open(f"data/pagin/boltTypeItem.html", "w") as file:
                        file.write(request.text)

                    with open(f"data/pagin/boltTypeItem.html") as file:
                        src5 = file.read()

                    soupLastLast = BeautifulSoup(src5, "lxml")
                    if soupLastLast.find("h2", class_="single-post-title") is not None:
                        title = soupLastLast.find("h2", class_="single-post-title").text.strip()
                    else:
                        title = "нет"

                    price = soupLastLast.find("p", class_="price").text.strip()
                    text = soupLastLast.find("div", id="tab-description").find("p").text.strip()
                    tableTH = soupLastLast.find_all("th", class_="woocommerce-product-attributes-item__label")
                    tableTD = soupLastLast.find_all("td", class_="woocommerce-product-attributes-item__value")

                    data = []

                    for th in tableTH:
                        data.append(th.text.strip())
                    for td in tableTD:
                        data.append(td.text.strip())

                    image = soupLastLast.find_all("div", class_="woocommerce-product-gallery__image")
                    images = []

                    for img in image:
                        images.append(img.find("img").get("src"))

                    itemsProduct.append({"id": g, "title": title, "price": price, "text": text, "table": data, "images": images})
                    print(g)
                block["items"] = itemsProduct
                result.append(block)
            else:
                pagUrl = urlr

                r4 = requests.get(url=pagUrl, headers=headers)

                with open(f"data/pagin/boltTypeNextNext.html", "w") as file:
                    file.write(r4.text)

                with open(f"data/pagin/boltTypeNextNext.html") as file:
                    src4 = file.read()

                soupLast = BeautifulSoup(src4, "lxml")
                itemHref = soupLast.find_all("li", "title")

                for items in itemHref:
                    itemHrefAll.append(items.find("a").get("href"))

                for g in range(0, len(itemHrefAll)):
                    request = requests.get(url=itemHrefAll[g], headers=headers)

                    with open(f"data/pagin/boltTypeItem.html", "w") as file:
                        file.write(request.text)

                    with open(f"data/pagin/boltTypeItem.html") as file:
                        src5 = file.read()

                    soupLastLast = BeautifulSoup(src5, "lxml")
                    if soupLastLast.find("h2", class_="single-post-title") is not None:
                        title = soupLastLast.find("h2", class_="single-post-title").text.strip()
                    else:
                        title = "нет"

                    price = soupLastLast.find("p", class_="price").text.strip()
                    text = soupLastLast.find("div", id="tab-description").find("p").text.strip()
                    tableTH = soupLastLast.find_all("th", class_="woocommerce-product-attributes-item__label")
                    tableTD = soupLastLast.find_all("td", class_="woocommerce-product-attributes-item__value")

                    data = []

                    for th in tableTH:
                        data.append(th.text.strip())
                    for td in tableTD:
                        data.append(td.text.strip())

                    image = soupLastLast.find_all("div", class_="woocommerce-product-gallery__image")
                    images = []

                    for img in image:
                        images.append(img.find("img").get("src"))

                    itemsProduct.append({"id": g, "title": title, "price": price, "text": text, "table": data, "images": images})
                    print(g)
                block["items"] = itemsProduct
                result.append(block)
    with open("data.json", "a") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)






def main():
    get_all_pages()


if __name__ == '__main__':
    main()
