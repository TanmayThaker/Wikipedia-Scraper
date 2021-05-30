#importing necessary libraries
import requests
from bs4 import BeautifulSoup
import operator
import re
from flask import Flask, render_template,request

#listing out manually all the unncessary stop words 
my_stopwords=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours',
              'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 
              'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 
              'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
              'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
              'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
              'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 
              'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 
              'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 
              'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
              'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma',
              'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
              'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',';',',','also','may','want']

#listing out all the symbols that we do not want in our word list
symbols = '!@#$%^&*()_-+={[}]|\;:"<>?/.,__——– '
#initializing a list of all the words present on the page
my_wordlist = []
#initializing the top_frequent_words which will contain our top 10 most frequent words
top_frequent_words=None
def extract_information(url): 
   try:
      source_code = requests.get(url).text #try to get the text of the page from the url 
   except requests.exceptions.RequestException as e:  
      raise SystemExit(e) # if page is not available then raising an exception
   my_soup = BeautifulSoup(source_code, 'html.parser') #parsing the webpage as HTML
   wordlist="" #creating a empty string that contains all the texts of the page
   for lower_text in my_soup.findAll('div',{'class':'mw-body'}): #Extracting all the information that is present in all of the div of class : mw-body tag
      wordlist+=lower_text.text #concatenating to our string
      wordlist=re.sub(r'\[[0-9]*\]','',wordlist) #Using regular expression to remove numbers in brackets eg. [12]
      wordlist=re.sub(r'[0-9]','',wordlist) #Using regular expression to remove all the numeric values
   text=wordlist.lower() #converting our string to lower case
   words = [word for word in text.split() if word.lower() not in my_stopwords] #removing words that are present in our list of stop_words
   new_text = " ".join(words) #joining all that filtered words to new_text
   my_wordlist=Convert(new_text) #converting string to list of words
   clean_symbols(my_wordlist) #calling clean_symbols to clean out all the symbols from the text

def Convert(string): #Function to convert string to list
  li = list(string.split(" "))
  return li

def clean_symbols(my_wordlist): #Function to filter our wordlist from unnecessary symbols
   clean_list =[] #creating a new list of clean words 
   for word in my_wordlist: 
      for i in range (0, len(symbols)):
         word = word.replace(symbols[i], '') 
      if len(word) > 0:
         clean_list.append(word)
   print(clean_list)
   create_dictionary(clean_list) # calling the Function to count and store most frequent words

def create_dictionary(clean_list): #Function to count and store most frequent words
    word_count = {} #initializing a dictionary/map to store the words and their counts
    for word in clean_list: #iterating in our clean_words list
      if word in word_count: #if the same word is present in our word_count
        word_count[word] += 1  #We increase the count of that word by one
      else:
        word_count[word] = 1 #else it is the first time we are encountering that word so increase by one
    popular_words = dict(sorted(word_count.items(), key=operator.itemgetter(1),reverse=True)) #sorting our word_count in descending order
    #print(popular_words)
    global top_frequent_words
    top_frequent_words = {k: popular_words[k] for k in list(popular_words)[:10]} #extracting only the 1op 10 frequently used words
    print(top_frequent_words)
    return top_frequent_words #returning our final dictionary containing top 10 frequently used words


app = Flask(__name__) # initialising the flask app with the name 'app'
@app.route('/handle_data', methods =["GET", "POST"]) # route with allowed methods as POST and GET
def handle_data():
   global top_frequent_words
   if request.method=="POST":
      my_url = request.form.get("url")
      extract_information(my_url)
   return render_template("results.html",top_frequent_words=top_frequent_words)


@app.route("/")
def homepage():
  return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True,port=8000) # running the app on the local machine on port 8000


