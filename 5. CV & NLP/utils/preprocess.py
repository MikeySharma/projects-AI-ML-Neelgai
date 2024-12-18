from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def preprocess(text):
    text=str(text)
    #lowercasing
    text=text.lower()
    #Remove Stop Words
    stop_words=set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_list = [w for w in word_tokens if not w in stop_words]
    
    
    #Remove numbers and special Symbols
    #words like 100m 2m were not removed so using this
    num=['0','1','2','3','4','5','6','7','8','9']
    num_filter=[]
    for i in range(0,len(filtered_list)):
        for j in range(0,len(num)):
            if num[j] in filtered_list[i]:
                num_filter.append(filtered_list[i])
                break
    
    for filter in num_filter:
        filtered_list.remove(filter)
                
    filtered_list = [w for w in filtered_list if w.isalnum()]
    filtered_list=  [w for w in filtered_list if not w.isdigit()]
    
    
    
    #Lematizing
    wordnet_lemmatizer=WordNetLemmatizer()
    lemmatized_list=[wordnet_lemmatizer.lemmatize(w,wordnet.VERB) for w in filtered_list]
    lemmatized_string=' '.join(lemmatized_list)
    
    return lemmatized_string