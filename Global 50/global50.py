import csv

for year in range(2017,2021):
    f = open("/Users/Koh/Documents/2017-_SNU/Research/DM/data/Global 50/pdftotext-2/Global50"+str(year)+".txt", 'r')
    publishers = []
    while True:
        line = f.readline()
        if not line: break
        if "." in line: 
            index = str(line).find('...')
            if index != 0:
                publishers.append(str(line)[:index])

    f1 = open('Global50'+str(year)+'.csv','w',encoding='utf-8')
    wr = csv.writer(f1)
    for p in publishers:
        wr.writerow([p])

# for year in range(2012,2017):
#     f = open("/Users/Koh/Documents/2017-_SNU/Research/DM/data/Global 50/Global50"+str(year)+".txt", 'r')
#     publishers = []
#     first = True
#     while True:
#         line = f.readline()
#         if first:
#             first = False
#             continue
#         if not line:
#             break
#         temp = str(line)
#         words = temp.split("\t")
#         pub = words[2]
#         publishers.append(pub)
#     f1 = open('Global50'+str(year)+'.csv','w',encoding='utf-8')
#     wr = csv.writer(f1)
#     for p in publishers:
#         wr.writerow([p])
