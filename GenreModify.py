import matplotlib as mpl
import matplotlib.pylab as plt
import csv
import random
import re
specialChar = " ,.…:()!?-"

def titleNormalize(title):
    temp = ""
    for char in title:
        if char.isalnum():
            temp += char
    temp = re.sub(r'[^A-Za-z0-9 ]+', '', temp)
    return temp


# result: "abcd"

f = open("mergedData_7.3.1_2019_2020_rearrange.csv",'r',encoding="utf-8")
reader = csv.reader(f)
first = True

bookData = []
for row in reader:
    if row[0] == '':
        break
    bookData.append(row)
f.close()

bookPublisherDict = {}
for i in range(2011,2021):
    f = open("./publisher/" + str(i) + "_publisher.csv",'r',encoding="utf-8")
    reader = csv.reader(f)
    first = True
    for row in reader:
        if first:
            first = False
            continue
        if row[0] == '':
            break
        title = titleNormalize(row[2])
        # for char in specialChar:
        #     title = title.replace(char,'')
        # title = title.replace(u'\xa0', u'')
        # print(title)
        # title = re.sub(r'\W+', '', title)
        # print(title)
        isGlobal50 = (row[5] == "O")
        year = int(row[1])
        if title not in bookPublisherDict:
        #     bookPublisherDict[title].append((year,isGlobal50))
        # else:
            bookPublisherDict[title] = (year,isGlobal50)

    f.close()

first = True
for book in bookData:
    if first:
        book.append("isGlobal50 of first year")
        first = False
        continue
    title = titleNormalize(book[3])
    # title = re.sub(r'\W+', '', title)
    tempList = bookPublisherDict[title]
    isGlobal50 = tempList[1]
    book.append(isGlobal50)
    # minYear = tempList[0][0]
    # for elem in tempList:
    #     if elem[0] < minYear:

f1 = open('mergedData_7.4_publisherDataUpdate.csv','w',encoding="utf-8")
wr = csv.writer(f1)
for book in bookData:
    wr.writerow(book)