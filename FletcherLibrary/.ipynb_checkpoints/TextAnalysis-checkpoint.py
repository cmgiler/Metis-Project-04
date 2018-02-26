__author__ = 'cmgiler'

import nltk
from IPython.display import clear_output

def SentenceBreak(content_list):
    if type(content_list) == str:
        sentences = nltk.tokenize.sent_tokenize(content_list)
        return sentences, len(sentences)
    
    sentences = []
    for i, text in enumerate(content_list):
        clear_output(wait=True)
        print('Progress: %d/%d' % (i+1, len(content_list)))
    sentences = [nltk.tokenize.sent_tokenize(text) for text in content_list]
    num_sentences = [len(s) for s in sentences]
    return sentences, num_sentences

def WordTokenization(sentence_list):
    for i in range(len(documents)):
        clear_output(wait=True)
        print("%d/%d" % (int(i+1), len(documents)))
        for j in range(len(documents[i])):
            documents[i][j] = nltk.tokenize.word_tokenize(documents[i][j])
            
def print_seperator():
    print('')
    print('-----')
    print('')
    
def TokenizeData(content):
    word_punct_tokenizer = nltk.tokenize.WordPunctTokenizer()
    tokens = word_punct_tokenizer.tokenize(content)
    tokens = [w.replace('-','') for w in tokens]
    tokens = [w.lower() for w in tokens if w.isalpha()]
    tokens = [w for w in tokens if len(w) > 1]
    return tokens
            
def ExploreData(content_list, 
                example_word='test', 
                words_of_interest=['test']):
    all_content = " ".join(a for a in content_list)
    all_content = all_content.lower()
    
    # Approximate size of text
    print("Text Size: %d bytes (%0.2f MB)" % (len(all_content),
                                              len(all_content)/1000000))
    print_seperator()
    
    tokens = TokenizeData(all_content)
    text = nltk.Text(tokens)
    
    print("Number of appearances for word '%s':" % example_word)
    print(text.concordance(example_word))
    
    print_seperator()
    
    # Frequency analysis for words of interest
    fdist = text.vocab()
    print("Frequency analysis for words of interest:")
    for word in words_of_interest:
        print("%s: %d" % (word, fdist[word]))
    
    print_seperator()
    
    print("Number of words in the text: %d" % len(tokens))
    print("Number of unique words in the text: %d" % len(fdist.keys()))
    
    print_seperator()
    
    print("Common words that aren't stopwords:")
    print([w for w in list(fdist.keys())[:100] if w.lower() not in nltk.corpus.stopwords.words('english')])
    
    print_seperator()
    
    print("Long words that aren't URLs:")
    print([w for w in fdist.keys() if len(w) > 15 and not w.startswith("http")][:100])
    
    print_seperator()
    
    print("Number of URLs")
    print(len([w for w in fdist.keys() if w.startswith("http")]))
    for url in [w for w in fdist.keys() if w.startswith("http")]:
        print(url)
    
    print_seperator()
    print("Enumerated Frequency Distribution:")
    for rank, word in enumerate(fdist.most_common()):
        if word[0] not in nltk.corpus.stopwords.words('english'):
            print(rank+1, '|', word[0], '|', word[1])
        if rank > 100:
            break