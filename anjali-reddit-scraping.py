!pip install praw
import requests
import pandas as pd
import praw

reddit = praw.Reddit(client_id='HEraiSpNQj2DOR0iINUxKA', client_secret='A7N8k7RsIhf8B_-NaTkKm2kJ6SczIw', user_agent='Web Scraping')

post_url = 'https://www.reddit.com/r/politics/comments/11j096k/calls_to_boycott_walgreens_grow_as_pharmacy/'
submission = reddit.submission(url=post_url)
submission.num_comments

# Creating an empty list to store the comments
comments = []
# Iterating through all the comments in the submission
for comment in submission.comments.list():
    # Skipping any "MoreComments" objects
    if isinstance(comment, praw.models.MoreComments):
        continue
    # Adding the comment's ID, body, score, and creation timestamp to the list
    comments.append({
        'id': comment.id,
        'body': comment.body,
        'score': comment.score,
        'created_utc': comment.created_utc
    })
# Converting the list of comments to a Pandas DataFrame
df = pd.DataFrame(comments) 

from datetime import datetime
# Converting the "created_utc" column to a datetime column
# Using the pd.to_datetime() function to convert the "created_utc" column into a datetime column
# We specify the unit as "s" to indicate that the timestamps in the "created_utc" column are in seconds
df['date_time'] = pd.to_datetime(df['created_utc'],  unit='s')    
# Extracting the date component from the "date_time" column and store it in a new "date" column
# Using the "dt" accessor to access the datetime properties of the "date_time" column
# Using the strftime() function to format the date component of the datetime column as a string with the format '%Y-%m-%d'
df['date'] = df['date_time'].dt.strftime('%Y-%m-%d') 
df.head()

# Removing the duplicate and saving the data to a csv file
WebScraping = df
WebScraping.drop_duplicates(subset='id', keep='last', inplace=True)
WebScraping.to_csv('LinkedinScraping.csv', index=True, header=True)

# Importing libraries
import pandas as pd
import numpy as np
import seaborn as sns

#Reading in the file from the web scraping notebook
Sentiment_analysis_df = pd.read_csv('LinkedinScraping.csv') 
Sentiment_analysis_df.head()

# Dropping unecessary columns
Sentiment_analysis_filtered_data = Sentiment_analysis_df.drop(columns = ['created_utc','Unnamed: 0'], axis = 1)
Sentiment_analysis_filtered_data.head()

# Removing unecessary symbols and stopwords (common words that do not have much meaning to the text)
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

# Defining a function to clean the Reddit text
def reddit_clean(redd):
    # Converting to lowercase
    redd = str(redd).lower()
    # Removing apostrophes
    redd = re.sub("'", "", redd)
    # Removing  usernames
    redd = re.sub("@[A-Za-z0-9_]+","", redd)
    # Removing  hashtags
    redd = re.sub("#[A-Za-z0-9_]+","", redd)
    # Removing URLs starting with "www."
    redd = re.sub(r"www.\S+", "", redd)
    # Removing URLs starting with "http" or "https"
    redd = re.sub(r"http\S+", "", redd)
    # Replacing some of the punctuation with spaces
    redd = re.sub('[()!?]', ' ', redd)
    # Removing text in square brackets
    redd = re.sub('\[.*?\]',' ', redd)
    # Removing non-alphanumeric characters
    redd = re.sub("[^a-z0-9]"," ", redd)
    # Removing words with 3 or fewer characters
    redd = re.sub(r"\b\w{1,3}\b"," ", redd)
    # Splitting text into individual words
    redd = redd.split()
    # Removing stopwords
    stopwords = STOPWORDS
    redd = [w for w in redd if not w in stopwords]
    # Joining the revised words back into a single string
    redd = " ".join(word for word in redd)
    return redd
# Cleaning the "body" column of the data frame by using the reddit_clean function
Sentiment_analysis_filtered_data['body'] = Sentiment_analysis_filtered_data['body'].apply(reddit_clean)
Sentiment_analysis_filtered_data.head()

# Tokenizing the comments
Tokenized_sentiment_analysis_filtered_data = Sentiment_analysis_filtered_data['body'].apply(lambda x: x.split())
print(Tokenized_sentiment_analysis_filtered_data)

from nltk.stem import PorterStemmer
# Creating an instance of the PorterStemmer class
stemmer = PorterStemmer()
# Applying stemming to each word in the Tokenized_sentiment_analysis_filtered_data df
tokenized_reddit_post = Tokenized_sentiment_analysis_filtered_data.apply(lambda x: [stemmer.stem(i) for i in x])
# Adding the stemmed words as a new column to the Sentiment_analysis_filtered_data df
Sentiment_analysis_filtered_data['tokenized'] = tokenized_reddit_post
# Printing the first few rows of the df to check the results
Sentiment_analysis_filtered_data.head()

# Importing other libraries
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections

# Combining all the words in the 'body' column of the Sentiment_analysis_filtered_data df into a single string
all_words = ' '.join([text for text in Sentiment_analysis_filtered_data['body']])
# Counting the frequency of each word in the string and create a dictionary
count_word = collections.Counter(all_words.split())
# Creating a WordCloud object with specified width and height
wordcloud = WordCloud(width=800, height=500)
# Generating the word cloud using the frequency dictionary
wordcloud.generate_from_frequencies(count_word)
# Setting the size of the plot
plt.figure(figsize=(10, 7)) # In inches
# Displaying the word cloud image
plt.imshow(wordcloud)
# Turning off the x and y axes
plt.axis("off")
# Showing the plot
plt.show()

# Making a bar chart of the top 10 neutral words
# Creating a frequency distribution of words
word_freq = nltk.FreqDist(count_word)
# Creating a pandas dataframe from the word frequency distribution
word_freq_df = pd.DataFrame({'Word': list(word_freq.keys()),
                             'Count': list(word_freq.values())})
# Selecting the top 10 most frequent words 
top_words_df = word_freq_df.nlargest(columns="Count", n=10)
# Creating a bar plot of the top 10 most frequent words
plt.figure(figsize=(16,5))
ax = sns.barplot(data=top_words_df, x="Word", y="Count")
ax.set(ylabel='Word Count')
plt.show()

# Using the TextBlob library for the sentiment analysis
# The sentiment function of textblob returns two properties, polarity, and subjectivity. Polarity is float which lies in the range of [-1,1] where 1 means positive statement and -1 means a negative statement
# Subjective sentences generally refer to personal opinion, emotion or judgment whereas objective refers to factual information
# Subjectivity is also a float which lies in the range of [0,1]

from textblob import TextBlob 
Sentiment_analysis_filtered_data['polarity'] = Sentiment_analysis_filtered_data['body'].apply(lambda z: TextBlob(z).sentiment.polarity)
Sentiment_analysis_filtered_data['subjectivity'] = Sentiment_analysis_filtered_data['body'].apply(lambda y: TextBlob(y).sentiment.subjectivity)
Sentiment_analysis_filtered_data.head()

# Creating a function to classify the polarity
def PolarityClassification(text):
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity 
    sentiment_subjectivity = blob.sentiment.subjectivity
    if sentiment_polarity > 0:
        return 'Positive Sentiment'
    elif sentiment_polarity == 0:
        return 'Neutral Sentiment'
    else:
        return 'Negative Sentiment'
    

# Creating a sentiment column with the previous function
Sentiment_analysis_filtered_data['sentiment'] = Sentiment_analysis_filtered_data['body'].apply(PolarityClassification)
Sentiment_analysis_filtered_data.head()

# Creating a new subjectivity column
Sentiment_analysis_filtered_data['SubjectivityClassification'] = np.where(Sentiment_analysis_filtered_data['subjectivity'] > 0.5, 'Subjective', 'Objective')
Sentiment_analysis_filtered_data.head()

# Creating a histogram of the sentiment
plt.figure(figsize=(10,5))
plt.xlabel('Sentiment', fontsize=30)
plt.xticks(fontsize=15)
plt.ylabel('Frequency', fontsize=30)
plt.yticks(fontsize=15)
plt.hist(Sentiment_analysis_filtered_data['polarity'], bins=10)
plt.title('Sentiment Distribution', fontsize=30)
plt.show()

# Counting the number of cases that fall within each subjectivity category
Sentiment_analysis_filtered_data.SubjectivityClassification.value_counts()

# Creating a histogram of the subjectivity
plt.figure(figsize=(10,5))
plt.xlabel('Subjectivity', fontsize=30)
plt.xticks(fontsize=15)
plt.ylabel('Frequency', fontsize=30)
plt.yticks(fontsize=15)
plt.hist(Sentiment_analysis_filtered_data['subjectivity'], bins=10)
plt.title('Subjectivity Distribution', fontsize=30)
plt.show()

# Running summary statistics of polarity and subjectivity
Summary = Sentiment_analysis_filtered_data[["polarity", "subjectivity"]]
Summary.describe()        

import matplotlib.pyplot as plt
# Creating a box and whisker plot for the subjectivity column
plt.boxplot(Sentiment_analysis_filtered_data['subjectivity'])
plt.title('Subjectivity Boxplot')
plt.xlabel('Subjectivity')
plt.ylabel('Score')
plt.show()

# Creating a box and whisker plot for the polarity column
plt.boxplot(Sentiment_analysis_filtered_data['polarity'])
plt.title('Polarity Boxplot')
plt.xlabel('Polarity')
plt.ylabel('Score')
plt.show()

# Creating crosstabs of the classified data
pd.crosstab(Sentiment_analysis_filtered_data['sentiment'], Sentiment_analysis_filtered_data['SubjectivityClassification'])