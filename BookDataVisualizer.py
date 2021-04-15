import matplotlib as mpl
import matplotlib.pylab as plt
import csv
import random
import numpy as np

class BookDataVisualizer:

    def __init__(self,dataFileName,publisherFileName):

        f = open(dataFileName,'r',encoding="ISO-8859-1")
        reader = csv.reader(f)
        first = True
        
        self.bookData = []
        self.legend = []
        self.genreNumToName = {0:"etc", 1:"Biographies&Memoirs", 2:"Business&SelfHelp", 3:"Children'sBooks", 4:"CookbooksFood&Wine", 5:"HealthFitness&Dieting, \n MedicalBooks", 6:"Literature&Fiction,\nTeen&Youngadult,\n Comics&GraphicNovels",7: "Politics&SocialSciences,\n History, Science&Math"}
        for row in reader:
            if first:
                self.legend = row
                first = False
                continue
            if row[0] == '':
                break
            self.bookData.append(row)
        f.close()
        
        self.globalPublisherDict = {}
        for year in range(2012,2021):
            f = open("/Users/Koh/Documents/2017-_SNU/Research/DM/data/Global 50/usable/Global50"+str(year)+".csv",'r')
            rd = csv.reader(f)
            for line in rd:
                pub = str(line[0]).strip()
                if year in self.globalPublisherDict:
                    self.globalPublisherDict[year].append(pub)
                else:
                    self.globalPublisherDict[year] = [pub]
            f.close()
        
        f = open(publisherFileName,'r',encoding="ISO-8859-1")
        reader = csv.reader(f)
        self.publisherDict = {}
        for row in reader:
            if first:
                first = False
                continue
            if row[0] == '':
                break
            publisher = row[0]
            motherPublisher = row[1]
            self.publisherDict[publisher] = motherPublisher
        f.close()
        
        self.colors = []
        for i in range(len(self.bookData)):
            tempC = [random.uniform(0.3,1),random.uniform(0.3,1),random.uniform(0.3,1)]
            self.colors.append(tempC)
    
        # divide data by duration - short / long / recent
        shortSellerIndex = []
        longSellerIndex = []
        allSellerIndex = []
        self.indexByDurationDict = {}
        for i in range(len(self.bookData)):
            bookIndex = int(self.bookData[i][15])
            allSellerIndex.append(i)
            if bookIndex == 0:
                shortSellerIndex.append(i)
            elif bookIndex == 1:
                longSellerIndex.append(i)

        self.indexByDurationDict[0] = shortSellerIndex
        self.indexByDurationDict[1] = longSellerIndex
        self.indexByDurationDict[2] = allSellerIndex

    def getPublisherData(self):
        for book in self.bookData:
            year = int(book[0])+1
            if year == 2021:
                year = 2020
            title = book[3]
            publisher = book[6]
            publisher = publisher.strip()
            mother = "Not Found"
            isGlobal50 = False
            if (publisher in self.publisherDict):
                mother = self.publisherDict[publisher]
                if mother in self.globalPublisherDict[year]:
                    isGlobal50 = True
                else:
                    for globalPub in self.globalPublisherDict[year]:
                        if mother in globalPub or globalPub in mother:
                            isGlobal50 = True
            book.append(mother)
            book.append(isGlobal50)
        
        global50 = 0
        notG = 0
        for book in self.bookData:
            if(book[-1]):
                global50 += 1
            else:
                notG += 1
        print(global50,notG)
            
    
    def getDurationBookData(self,durationNum):
        tempBookData = []
        for i in self.indexByDurationDict[durationNum]:
            tempBookData.append(self.bookData[i])
        return tempBookData

    def getNewGenreImage(self):
        numList = [[0,0] for i in range(3)] # Fiction, Nonfiction, Children
        # label = ["Children Short", "Children Long", "Fiction Short", "Fiction Long", "Nonfiction Short", "Nonfiction Long"]
        label = ["Nonficton","Fiction","Children"]
        for i in range(2):
            bd = self.getDurationBookData(i)
            for book in bd:
                if book[2] == "3":
                    numList[2][i] += 1
                elif book[2] == "6":
                    numList[1][i] += 1
                else:
                    numList[0][i] += 1
        
        barNumList = [[0,0,0] for i in range(2)]
        for i in range(2):
            for j in range(3):
                barNumList[i][j] = numList[j][i]

        print(barNumList)

        pos = np.arange(3)
        p1 = plt.barh(pos,barNumList[1],color='b',alpha=0.5,edgecolor='black')
        p2 = plt.barh(pos,barNumList[0],color='navy',alpha=0.5,left=barNumList[1],edgecolor='black',hatch='//')

        # plt.bar(pos,barNumList,color=['green','green','red','red','yellow','yellow'])
        plt.ylabel("Genre")
        plt.xlabel("Num. of Books")
        plt.title("Short, Long Bestseller Num. by Genre")
        plt.yticks(pos,label)
        plt.legend((p1[0], p2[0]), ('Short', 'Long'), fontsize=8)
        plt.show()

    def getGenreImage(self):
        genreColorDict = {}
        for i in range(10):
            genreColorDict[i] = self.colors[i]
        for durationNum in range(3):
            plotName = "Genre"
            if durationNum == 0:
                plotName += " (Short "
            else:
                plotName += " (Long "
            plotName += "BestSeller)"

            tBD = self.getDurationBookData(durationNum)
            
            genreDict = {}
            for i in range(10):
                genreDict[i] = 0
            i = 0
            for book in tBD:
                genre = book[2]
                genreDict[int(genre)] += 1
            
            genreNumList = []
            for genre in genreDict:
                genreNumList.append((genre,genreDict[genre]))
            
            genreNumList.sort(reverse = True, key = lambda genre: genre[1])
            genreList = []
            numList = []
            tempColors = []
            for i in range(8):
                genreList.append(self.genreNumToName[genreNumList[i][0]])
                numList.append(genreNumList[i][1])
                tempColors.append(genreColorDict[genreNumList[i][0]])

           # plt.title(plotName,fontdict={'fontsize':30})
            a,b,c = a,b,c=plt.pie(numList, colors = tempColors, labels = genreList, autopct='%1.1f%%', startangle=90)
            for text in b:
                text.set_fontsize(30)
            plt.axis('equal')
            plt.show()

    
    def getSpecificGenreImage(self):
        genreColorDict = {}
        for i in range(20):
            genreColorDict[i] = self.colors[i]

        for genreNum in [2,3,6]:
                
            tBD = self.getDurationBookData(2)
            
            referenceDict = {}
            for i in range(5):
                referenceDict[i] = 0
            
            for book in tBD:
                if int(book[2]) == genreNum:
                    reference = int(book[9])+int(book[10])
                    if reference > 3:
                        referenceDict[4] += 1
                    else:
                        referenceDict[reference] += 1
            genreDict = referenceDict
            
            genreNumList = []
            for genre in genreDict:
                genreNumList.append((genre,genreDict[genre]))
            
            genreNumList.sort(key = lambda genre: genre[0])
            genreList = []
            numList = []
            tempColors = []
            for i in range(len(genreNumList)):
                print(genreNumList[i])
                if genreNumList[i][0] == 4:
                    genreList.append(">3")
                else:
                    genreList.append(genreNumList[i][0])
                numList.append(genreNumList[i][1])
                tempColors.append(genreColorDict[genreNumList[i][0]])

            #plt.title(plotName,fontdict={'fontsize':20})
            a,b,c = a,b,c=plt.pie(numList, colors = tempColors, labels = genreList, autopct='%1.1f%%', startangle=90)
            for text in b:
                text.set_fontsize(20)
            plt.axis('equal')
            plt.show()

    def getPublishYearImage(self,labelNum):
        for durationNum in range(2):
            plotName = "BSYear - PublishedYear"
            if durationNum == 0:
                plotName += " (Short "
            else:
                plotName += " (Long "
            plotName += "BestSeller)"

            tBD = self.getDurationBookData(durationNum)
            yearDict = {}
            for book in tBD:
                bsYear = int(book[0])
                pYear = int(book[4])
                difYear = bsYear - pYear
                if difYear in yearDict:
                    yearDict[difYear] += 1
                else:
                    yearDict[difYear] = 1
            
            yearNumList = []
            for year in yearDict:
                yearNumList.append((year,yearDict[year]))
            yearNumList.sort(reverse = True, key = lambda year: year[0])
            print(yearNumList)

            if labelNum < len(yearNumList):
                etcNum = 0
                for i in range(labelNum,len(yearNumList)):
                    etcNum += yearNumList[i][1]
                yearNumList = yearNumList[0:labelNum]
                yearNumList.append(('etc',etcNum))

            yearList = []
            numList = []
            for i in range(len(yearNumList)):
                yearList.append(yearNumList[i][0])
                numList.append(yearNumList[i][1])
            tempColors = self.colors[:len(numList)]

            plt.title(plotName,fontdict={'fontsize':30})
            a,b,c=plt.pie(numList, colors = tempColors, labels = yearList, autopct='%1.1f%%', startangle=90)
            for text in b:
                text.set_fontsize(20)
            plt.axis('equal')
            plt.show()

    def getReferenceByImage(self):
        tempRefList = []
        for i in range(2):
            bD = self.getDurationBookData(i)
            for book in bD:
                if book[1] == 'Literature&Fiction':
                    tempRefList.append((book[1],int(book[8])+int(book[9]),int(book[12])))
        
        tempRefList.sort(reverse = True, key = lambda genre: genre[1])

        refDict = {}
        for book in tempRefList:
            if book[1] in refDict:
                refDict[book[1]] += 1
            else:
                refDict[book[1]] = 1
        
        temp = []
        for ref in refDict:
            temp.append((ref,refDict[ref]))
        temp.sort(key = lambda genre: genre[0])
        
        genreList = []
        numList = []
        tempColors = []
        for i in range(len(temp)):
            genreList.append(temp[i][0])
            numList.append(temp[i][1])
        tempColors = self.colors[:len(numList)]

        numList[6] = sum(numList[6:])
        numList = numList[:7]
        genreList = genreList[:6]
        genreList.append('etc')
        
        tempColors = self.colors[:len(genreList)]
        a,b,c=plt.pie(numList, colors = tempColors, labels = genreList, autopct='%1.1f%%', startangle=90)
        for text in b:
                text.set_fontsize(20)
        plt.axis('equal')
        plt.show()
        # sizeDictP = {}
        # sizeDictM = {}
        # for i in range(len(byPerson)):
        #     if byPerson[i] in sizeDictP:
        #         sizeDictP[byPerson[i]] += 1
        #     else:
        #         sizeDictP[byPerson[i]] = 1
        #     if byMag[i] in sizeDictM:
        #         sizeDictM[byMag[i]] += 1
        #     else:
        #         sizeDictM[byMag[i]] = 1
        
        # xP, yP, sP = [], [], []
        # for key in sizeDictP:
        #     xP.append(key[0])
        #     yP.append(key[1])
        #     sP.append(sizeDictP[key]*2)
        
        # plt.scatter(xP,yP,s=sP)
        # plt.show()

        # xM, yM, sM = [], [], []
        # for key in sizeDictM:
        #     xM.append(key[0])
        #     yM.append(key[1])
        #     sM.append(sizeDictM[key]*2)

        # plt.scatter(xM,yM,s=sM)
        # plt.show()

    def getGenderImage(self):
        for i in range(2):
            tBD = self.getDurationBookData(i)

            plotName = "Gender"
            if i == 0:
                plotName += " (Short "
            else:
                plotName += " (Long "
            plotName += "BestSeller)"

            gender = [0,0] # F,M
            label = ['Female','Male']
            for book in tBD:
                if book[10] == 'F':
                    gender[0] += 1
                elif book[10] == 'M':
                    gender[1] += 1
            tempColors = self.colors[:2]

            plt.title(plotName,fontdict={'fontsize':30})
            a,b,c=plt.pie(gender, colors = tempColors, labels = label, autopct='%1.1f%%', startangle=90)
            for text in b:
                text.set_fontsize(20)
            plt.axis('equal')
            plt.show()

    def getPriceImage(self):
        for i in range(2):
            tBD = self.getDurationBookData(i)

            plotName = "Price"
            if i == 0:
                plotName += " (Short "
            else:
                plotName += " (Long "
            plotName += "BestSeller)"

            priceDurationList = []
            for book in tBD:
                if(book[6][0] != ':'):
                    if (int(book[6])!=0):
                        priceDurationList.append((float(book[7])/int(book[6]),int(book[12])))
            priceDurationList.sort(reverse = True, key = lambda price: price[0])

            prices = []
            durations = []

            for elem in priceDurationList:
                prices.append(elem[0])
                durations.append(elem[1])

            plt.scatter(prices,durations)
            plt.show()

    def getPublisherImage(self,labelNum):
        for durationNum in range(2):
            plotName = "Genre"
            if durationNum == 0:
                plotName += " (Short "
            else:
                plotName += " (Long "
            plotName += "BestSeller)"

            tBD = self.getDurationBookData(durationNum)
            genreDict = {}
            for book in tBD:
                genre = book[5]
                if genre in genreDict:
                    genreDict[genre] += 1
                else:
                    genreDict[genre] = 1
            
            genreNumList = []
            for genre in genreDict:
                genreNumList.append((genre,genreDict[genre]))
            genreNumList.sort(reverse = True, key = lambda genre: genre[1])
            print(genreNumList)
            if labelNum < len(genreNumList):
                etcNum = 0
                for i in range(labelNum,len(genreNumList)):
                    etcNum += genreNumList[i][1]
                genreNumList = genreNumList[0:labelNum]
                genreNumList.append(('etc',etcNum))

            genreList = []
            numList = []
            for i in range(len(genreNumList)):
                genreList.append(genreNumList[i][0])
                numList.append(genreNumList[i][1])
            tempColors = self.colors[:len(numList)]

            plt.title(plotName,fontdict={'fontsize':30})
            a,b,c=plt.pie(numList, colors = tempColors, labels = genreList, autopct='%1.1f%%', startangle=90)
            for text in b:
                text.set_fontsize(20)
            plt.axis('equal')
            plt.show()

    def getImpactImage(self):
        
        tBD = self.getDurationBookData(2)

        plotName = "Impact"

        genreImpactDict = {2:[],3:[],6:[]}
        for book in tBD:
            impact = book[16]
            if "E" in impact:
                indexE = impact.index("E")
                temp = float(impact[:indexE]) * (10**int(impact[indexE+2:]))
                impact = temp
            else:
                impact = float(impact)
            
            if int(book[2]) in [2,3,6]:
                genreImpactDict[int(book[2])].append(impact)

        impacts = []
        genres = []

        for key in genreImpactDict:
            genreImpactDict[key] = sum(genreImpactDict[key])/len(genreImpactDict[key])
            genres.append(self.genreNumToName[key])
            impacts.append(genreImpactDict[key])

        # plt.scatter(impacts,durations)
        plt.title("Average Impact",fontdict={'fontsize':20})
        plt.bar(genres,impacts)
        plt.show()

    def getFirstBSImage(self):
        for i in range(2):
            tBD = self.getDurationBookData(i)

            plotName = "isFirstBestseller"
            if i == 0:
                plotName += " (Short "
            else:
                plotName += " (Long "
            plotName += "BestSeller)"

            isFBS = [0,0] # F,N
            label = ['First','not First']
            for book in tBD:
                if book[11] == '1':
                    isFBS[0] += 1
                elif book[11] == '0':
                    isFBS[1] += 1
            tempColors = self.colors[:2]

            plt.title(plotName,fontdict={'fontsize':30})
            a,b,c=plt.pie(isFBS, colors = tempColors, labels = label, autopct='%1.1f%%', startangle=90)
            for text in b:
                text.set_fontsize(20)
            plt.axis('equal')
            plt.show()