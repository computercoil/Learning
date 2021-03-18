# input a website, count and plot the top 7 words

from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import matplotlib.pyplot as plt
#from Ipython.display import clear_output


def main():
    while input("Would you like to scrape a website (y/n)? ") == 'y':
        try:
            #clear_output()
            site = input("Enter a website to analyze: ")
            user_bad = input("Enter a word NOT to analyzed: ")
            bad_words = {"the", "a", "in", "of", "to", "you", "\xa0", "and", "at", "on", "for", "from", "is", "that", "his", "are", "be", "-", "as", "&", "they", "with", "how", "was", "her", "him", "i", "has", "|", "^", ".", "", ")", "(", ","}
            bad_words.add(user_bad)
            scrape(site, bad_words)
        except:
            print("Something went wrong, please try again.")
    print("Thanks for analyzing! Come back again!")

def scrape(site, bad_words):
    page = requests.get(site)
    soup = BeautifulSoup(page.content, "html.parser")
    text = soup.find_all(text=True)
    visible_text = filter(filterTags, text)
    word_count = {}
    for text in visible_text:
        words = text.replace('\n', '').replace('\t','').split(' ')
        words = list(filter(lambda word: False if word.lower() in bad_words else True, words))
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    word_count = sorted(word_count.items(), key=lambda kv: kv[1], reverse=True)[:7]
    displayResults(word_count, site)
    
def filterTags(element):
        if element.parent.name in ["style", "script", "head", "title", "meta", "[document]" ]:
            return False
        if isinstance(element, Comment):
            return False
        return True
""" 
# for fixed band_words   
def filterWaste(word):
        bad_words = ("the", "a", "in", "of", "to", "you", "\xa0", "and", "at", "on", "for", "from", "is", "that", "his", "are", "be", "-", "as", "&", "they", "with", "how", "was", "her", "him", "i", "has", "|", "^", ".", "", ")", "(")       
        if word.lower() in bad_words:
            return False
        else:
            return True
"""
        
def displayResults(words, site):
    count = [item[1] for item in words]
    word = [item[0] for item in words]
    plt.figure(figsize=(20, 10))
    plt.bar(word, count)
    plt.title("Analyzing Top Words fron: {}...".format(site[:50]), fontname="Sans Serif", fontsize=24)
    plt.xlabel("Words", fontsize=24)
    plt.ylabel("# of Appearance", fontsize=24)
    plt.xticks(fontname="Sans Serif", fontsize=20)
    plt.yticks(fontname="Sans Serif", fontsize=20)
    plt.show()
    

if __name__ == "__main__":
    main()
