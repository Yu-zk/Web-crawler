import requests
import re
import time
from decimal import Decimal

def getHTMLText(url):
    try:
        r = requests.get(url, timeout =300)
        r.raise_for_status()
        r.encodeing = r.apparent_encoding
        return r.text
    except:
        return ""

def parsePage(ilt, html):
    try:
        #精简h$tml的起点
        tli = re.findall(r'&quot;title&quot;:&quot;.*?;', html)
        pli = re.findall(r'&quot;price&quot;:[\d\.]*', html)
        upli = re.findall(r'&quot;unitPrice&quot;:[\d\.]*', html)
        #proli = re.findall(r'&quot;unitPrice&quot;:[\d\.]*', html)  打折信息待处理
        bnli = re.findall(r'&quot;brandName&quot;:&quot;.*?;', html)
        #dn 带分号
        anli = re.findall(r'&quot;aisleName&quot;:&quot;.*?;', html)
        snli = re.findall(r'&quot;shelfName&quot;:&quot;.*?;', html)
        ptli = re.findall(r'&quot;productType&quot;:&quot;.*?;', html)
        inli = re.findall(r'&quot;isNew&quot;:.*?;', html)
#         &quot;title&quot;:&quot;Tesco Apple And Raspberry Juice Drink 1.5 Litre&quot;,
#         &quot;price&quot;:0.8,&quot;unitPrice&quot;:0.053
#       ;,&quot;brandName&quot;:&quot;Tesco&quot;,&quot
#   quot;,&quot;aisleName&quot;:&quot;Baked Beans&quot;,&quot
#   quot;,&quot;shelfName&quot;:&quot;Tinned Baked Beans&quot;,&quot
#   quot;,&quot;productType&quot;:&quot;SingleProduct&quot;,
#        ,&quot;isNew&quot;:false,&quot;
        for i in range(23):
            title = tli[i].split("&quot;")[3]
            price = pli[i].split("&quot;price&quot;:")[1]
            uprice = upli[i].split("&quot;unitPrice&quot;:")[1]
            brandname = bnli[i].split("&quot;")[3]
            aislename = anli[i].split("&quot;")[3]
            shelfname = snli[i].split("&quot;")[3]
            productname = ptli[i].split("&quot;")[3]
            isnew = inli[i].split("&quot;")[2]
            if isnew==":false,":
                isnew="false"
            else:
                isnew="true"
            ilt.append([title, price, uprice, brandname, aislename, shelfname, productname,isnew])
    except:
        print("")

def printGoodList(ilt, n,f):
    tplp = "{:3}\t{:50}\t{:4}\t{:10}\t{:10}\t{:20}\t{:20}\t{:20}\t{:10}"
    f.write(tplp.format("No.","Name","price","unit price","brand name","aisle name","shelf name","product name","is new"))
    f.write('\n')
    count = 0
    for g in ilt:
        count = count + 1
        if count<=n :
            f.write(tplp.format(count, g[0], g[1], g[2], g[3], g[4], g[5], g[6],g[7]))
            f.write('\n')

def main():
    #文件的输出
    f = open("1.txt", "w")
    goods = input("Type name : ")
    n = int(input("Type number : "))
    depth = int(n / 24 + 1)
    start_url = "https://www.tesco.com/groceries/en-GB/search?query=" + goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&offset=2' + str(24*i)
            html = getHTMLText(url)
            parsePage(infoList, html)
            time.sleep(1)
        except:
            continue
    printGoodList(infoList,n,f)
    f.close()
main()
