#inport libraries
import re
import math
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np

#function to draw pie chart for accuracy
def drawPieChart(count):
    labels = 'Whom', 'When', 'Where', 'Occasion' #the slices will be ordered and plotted counter-clockwise.
    sizes = [count["Whom"] ,count["When"], count["Where"], count["Occasion"]] #size of each slice. These don;t have to sum up to 100. Python normalizes values automatically.
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral'] #color of each slice
    explode = (0, 0, 0, 0) #the explode value determines if a slice should be sticking out and to what extent
    #make the chart. Autopct is used to also add the percentage on top of the slice.
    #you can add/remove the shadow with the shadow feature.
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%.1f%%', shadow=True)
    plt.axis('equal') #set aspect ratio to be equal so that pie is drawn as a circle.
    plt.show()
    
    
#function to draw bar chart for accuracy
def drawBarChart(count):
    labels = ('Whom', 'When', 'Where', 'Occasion') #the labels of the bars    
    yPos = [0 ,1 ,2, 3] #the positions of each bar on the y-axis (5 bars in this case)
    accuracy = [count["Whom"] ,count["When"], count["Where"], count["Occasion"]] #the context accuracy
    
    error = np.random.rand(len(labels)) #make random error bars. np.random.rand(x) returns a table of x numbers between 0 and 1
    plt.barh(yPos, accuracy, xerr=error, align='center', color='red', alpha=0.4) #barh makes the histogram. Alpha tunes the darkness of the color    
    plt.yticks(yPos, labels) #add the labels
    plt.xlabel('Context') #add the label of the x axis

    #add the title of the plot
    plt.title('Context Extractiion Histogram')
    plt.show()
    plt.savefig('context-extraction-barchart.png', format='png') #save the plot


#function to sort dictionary based on the size of the word
def sortDictionary(dictionary):
    dictionary.sort(key = len, reverse = True)
    return dictionary


#function to get dictionary of any context
def getDictionary(context):
    path = "F:\\Projects\\BIA Scrapper\\Dictionary\\Dictionary - " + context + ".txt" #dictionary path
    dictionary = [] #list to store words

    file = open(path, 'r') #open the dictionary file
    for line in file: dictionary.append(line.strip()) #add word to the dictionary
    file.close() #close the dictionary file

    return sortDictionary(dictionary) #returns sorted dictionary


#function to clean the review
def getCleanReview(review):
    review = re.sub("[^a-zA-Z\s'\\-]+", ' ', review) #remove anything that isn't a letter, space, or number
    review = ' ' + re.sub(' +', ' ', review) #remove extra spaces
    review = review.strip().lower()
    return review


#function to save the data in a file
def saveDataInFile(data, filename, path):
    file = path + "Datasets\\" + filename #file absolute path
    saveData = open(file, 'w') #create a file
    saveData.write(data) #write data to the file
    saveData.close() #close the file
    
    
#function to check context word
def getContextAnnotation(review, context):
    dictionary = contextDictionary[context] #dictipnary of context
    for word in dictionary:
        word = '\\b' + word.strip() + '\\b'
        search = re.findall(word, review)
        
        if not len(search) == 0:
            return 1
    return 0


#function to build test data
def buildTestDataset(reviews):
    testData = "" #test data
    for review in reviews: #for each review in reviews
        review = getCleanReview(review) #get cleaned review
        whom = getContextAnnotation(review, "Whom")
        when = getContextAnnotation(review, "When")
        where = getContextAnnotation(review, "Where")
        occasion = getContextAnnotation(review, "Occasion")   
         
        testData = testData + review + "\t" + str(whom) + "\t" + str(when) + "\t" + str(where) + "\t" + str(occasion) + "\n"
    saveDataInFile(testData, "test-dataset.txt", dataPath) #save data in a file


#function to get total context counts
def getContextCount(trainDataset, testDataset):
    train = []
    test = []
    count = {
        "Whom": 0,
        "When": 0,
        "Where": 0,
        "Occasion": 0,
        "Total": 0, 
        "Overall": 0
    }
    #reading data from training dataset
    for line in trainDataset:
        train.append(line.strip())
        count["Total"] += 1

    #reading data from test dataset
    for line in testDataset:
        test.append(line.strip())
        
    #comparing data between training and test
    for i in range(0, count["Total"]):
        trainData = train[i].split("\t")
        testData = test[i].split("\t")
        
        if trainData[1] == testData[1]: #checking whom context
            count["Whom"] += 1
        if trainData[2] == testData[2]: #checking when context
            count["When"] += 1
        if trainData[3] == testData[3]: #checking where context
            count["Where"] += 1
        if trainData[4] == testData[4]: #checking occasion context
            count["Occasion"] += 1
        
    return count

    
#function to calculate the accuracy
def getAccuracy(matchedRecords, totalRecords):
    accuracy = matchedRecords / totalRecords * 100
    accuracy = math.floor(accuracy * 100) / 100
    return accuracy


#function to get indexes of all similar or matched words
def getSimilarWordIndex(review, contextWord):
    return [m.start() for m in re.finditer(contextWord, review)] #find all index for matching word


#function to parse the matched or similar word from string
def parseSimilarWord(review, frontIndex, contextWord):
    word = "" #
    front = frontIndex #front index of the word
    last = frontIndex + len(contextWord) #last index of the word
    reviewLen = len(review)

    while(front < last and front < reviewLen): #loop until front and last index matched
        word += review[front]
        front += 1
    while(front < reviewLen-1 and review[front] != " "): #loop if word in not completely added
        word += review[front]
        front += 1
        
    return word #returns full word


#function to replace all matched or similar word in the review with empty character
def replaceSimilarWord(review, contextWord):
    return review.replace(contextWord, '') #return the replaced word review
    

#function to find a similar word and replace it
def findAndReplace(review, contextWord, similarWordsIndexes):
    words = set() #set of all similar or matched words
    
    #find and store all the similar or matched words in a set
    for i in range(0, len(similarWordsIndexes)): #foreach index
        index = similarWordsIndexes[i] #front index of each match
        words.add(parseSimilarWord(review, index, contextWord)) #add similar or matched word to the set
        
    review = replaceSimilarWord(review, contextWord) #remove context words from the review
    return review, words


# read review
def findContext(review, context):
    dictionary = contextDictionary[context] #dictipnary of context
    observation = set() #observed result
    review = getCleanReview(review) #get cleaned review
    isContextFound = False #flag to check if context found in review
    
    for contextWord in dictionary: 
        contextWord = " " + contextWord
        similarWords = set() #store all possible similar words
        
        if contextWord in review:
            contextWordCount = review.count(contextWord)
            for count in range(0, contextWordCount): #loop for each occurance of context word in review   
                similarWordsIndexes = getSimilarWordIndex(review, contextWord) #get all indexes of similar words
                review, similarWords = findAndReplace(review, contextWord, similarWordsIndexes) #update review and similar words set
            
                for word in similarWords: #foreach similar words
                    if contextWord == word: #if similar word matched with context word
                        isContextFound = True
                        observation.add(word) #add context matching word
         
    #print result
    print("\n" + context, end = ': ')
    for word in observation:
        print(word, end = ',')
        
    #return 0 or 1
    if isContextFound == False:
        return 0
    return 1


## main function
if __name__ == '__main__':
    global dataPath #directory path of saved scrapped data
    global contextDictionary #dictionry to hold contexts dictionary
    
    dataPath = "F:\\Projects\\BIA Scrapper\\Sample Data\\" 
    contextDictionary= {
        "Occasion": getDictionary("Occasion"), #get dictionary for "occasion" context
        "Where": getDictionary("Where"), #get dictionary for "where" context
        "When": getDictionary("When"), #get dictionary for "when" context
        "Whom": getDictionary("Whom") #get dictionary for "whom" context
    }

    userInp = input("Enter your choice \n\tA. Find contexts from a review. \n\tB. Find accuracy.\nPlease Enter A or B: ").lower()
    print("\nThe result is: ")
    if userInp == 'a':
        review = input("Enter review: ") #review
        findContext(review, "Whom")
        findContext(review, "When")
        findContext(review, "Where")
        findContext(review, "Occasion")
    
    elif userInp == 'b':
        #read all raw reviews and create test dataset
        reviews = open(dataPath + "NYC\\American\\" + "reviews.txt", 'r')
        buildTestDataset(reviews)
        
        #loading datasets
        trainDataset = open(dataPath + "Datasets\\" + "training-dataset.txt", 'r') #training dataset
        testDataset = open(dataPath + "Datasets\\" + "test-dataset.txt", 'r') #test dataset
        
        #calculating accuracy count
        count = getContextCount(trainDataset, testDataset)
        #print(count) #get exact compared data
        print("Whom Accuracy: " + str(getAccuracy(count["Whom"], count["Total"])))
        print("When Accuracy: " + str(getAccuracy(count["When"], count["Total"])))
        print("Where Accuracy: " + str(getAccuracy(count["Where"], count["Total"])))
        print("Occasion Accuracy: " + str(getAccuracy(count["Occasion"], count["Total"])))
        print("Overall Accuracy: " + str(getAccuracy(count["Whom"] + count["When"] + count["Where"] + count["Occasion"], count["Total"] * 4)))
        
        #draw graphs
        drawPieChart(count)
        drawBarChart(count)