# Context Extraction
The main aim of the project is to scrap reviews from website for American cuisine restaurants in NYC. Then from the scrapped reviews, it would extract the context and calculate the accuracy for each context. (Contexts considered are: Whom, When, Where, and Occasion) 
    - 'Whom' denotes, with whom the user went to the restaurant (example: friends, family, etc.) 
    - 'When' denotes, for which part of the day the user dined in (example: lunch, dinner, etc.) 
    - 'Where' denotes, whether the user is local or tourist.
    - 'Occasion' denotes, for which particular occasion the user visited (example: birthday, wedding anniversary, etc.)

Step 1: In this step, the program scraps the list of 150 restaurants having their names along with unique usernames and URLs. It saves the list in a txt extension file.

Step 2: In the second step, it scraps raw HTML files for every review page (every review page consist of approximately 20 reviews) from all the restaurants in the list (generated in step 1). These HTML pages were stored under a folder created by the restaurants' unique username.

Step 3: After scrapping raw HTML files, in this step, the program scanned through every review HTML page of each restaurant and saved each review under the same restaurant folder as "restaurant-name-reviews.txt". Also, a copy of consolidated reviews was generated in the parent folder (one level up folder) as reviews.txt

Step 4: After extracting reviews for every restaurant, we have created training dataset by manually reviewing context for around 1000 random reviews. The training dataset consists of reviews followed by (context flags) 'whom', 'when', 'where', and 'occasion' separated by tab space in single line. These context flags are the binary values to represent the presence of context in the corresponding review. The structure of the file is as follows: 
    - Review Whom When Where Occasion I went with my family on lunch 1 1 0 0

Step 5: At this step, we have built a dictionary for each context based on the phrase or words found while creating the test-dataset. These dictionaries are the flat files, where every line contains any phrase or word that directly represents meaning information about the context. For example: for "Whom" context, the whom dictionary contains words like mother, mother-in-law, friends etc.

Step 6: This is the last step to reach our final observations. These observations were divided into two sub-sections: I. Find context out of any passed review. II. Find the context accuracy.

I. The program picks every word or phrase from the dictionary (flat file) and finds the similar word strings in every review. The program then stores the found similar strings in a set (to avoid duplicates) then check for an exact match on it. Each exact match then stored in python dictionary of a set. The saved dictionary has been returned after performing the same operations for each context. The output of this operations is as follows: 
    - Whom: friends, family 
    - When: lunch 
    - Where: tourist 
    - Occasion: birthday

II. To check the accuracy, the program reads all the reviews extracted before and generates a test-dataset. This test-dataset pertains the same structure to the train-dataset. Then, it loads all the lines of both training-dataset and test-dataset in run-time memory in two different lists. After creating two lists, it traverses through both lists parallelly and matches binary values for each context. For each context, the program maintains a counter and on every match, it increments the counter by 1. After matching each context for every review, it calculates the accuracy by dividing it by a total number of reviews or by the size of any list. The result of the observation is as followed: 
    - Whom Accuracy: xx.xx% 
    - When Accuracy: xx.xx% 
    - Where Accuracy: xx.xx% 
    - Occasion Accuracy: xx.xx%
