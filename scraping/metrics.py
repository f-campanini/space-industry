# word cloud script
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from django_pandas.io import read_frame # to import dataset from django queryset
from nltk.corpus import stopwords 

# standard import to load data from database
from .models import News
from celery import shared_task

@shared_task
def run_wordcloud():
    # retrieve the entire dataset from the News table
    # possible improvement would be to pass a timerange through the endpoing
    # and use it to create the plot
    news_queryset = News.objects.all()
    
    # now build the pandas datasets using only the column title from the queryset
    df = read_frame(news_queryset, fieldnames=['title'])

    # step one:
    # make everything lowercase 
    # remove common words using nltk stopwords
    text = " ".join(title for title in df.title)
    my_list = [w for w in text.split() if w.isalnum()]
    s = set(stopwords.words('english'))
    my_list_one = [w.lower() for w in my_list if w.lower() not in s]
    
    # step two:
    # do a second parse to eliminate words from a static set loaded from file
    with open('stopwords.txt', 'r') as f:
        my_stopwords_set = set(f.read().split(' '))   
    my_list_two = [w for w in my_list_one if w not in my_stopwords_set]

    # step three:
    # do a third parse and get rid of numbers
    my_list_three = [w for w in my_list_two if not w.isdigit()]

    # step four
    # another parse to remove strings shorter than 3 characters
    my_list_four = [w for w in my_list_three if len(w) > 3]
    
    """
    # this is for testing only, to check which are the most frequents words
    my_dictionary = {}
    for item in my_list_four:
        if item in my_dictionary:
            my_dictionary[item] += 1
        else:
            my_dictionary[item] = 1
    print(sorted(my_dictionary, key = my_dictionary.get, reverse = True))
    """

    # join the list again to prepare it for the wordcloud
    parsed_text = ''
    for item in my_list_four: parsed_text += item + " "

    # lower max_font_size, change the maximum number of word and lighten the background:
    wordcloud = WordCloud(max_words=40, max_font_size=50, background_color="white").generate(parsed_text)
    
    # when changing the figure size check which is the dpi set in the views
    plt.figure(figsize=(3, 2))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('media/wordcloud.png', dpi=200)

# allowing to execute this from command line so you can test it from shell
if __name__ == "__main__":
    run_wordcloud()
