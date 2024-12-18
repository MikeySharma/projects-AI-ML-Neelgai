import joblib
import math
import nltk
from nltk.tokenize import sent_tokenize
from langchain import PromptTemplate
from langchain import LLMChain

# Load the tf-idf model
tfidf_model = joblib.load('./models/tfidf.pkl')

def extractive_summarize(paragraph):
    sentences = sent_tokenize(paragraph)
    num_sentences = math.ceil(len(sentences) * 0.25)

    tfidf_scores = {}
    for idx, sentence in enumerate(sentences):
        tfidf_score = 0
        words = nltk.word_tokenize(sentence)
        for word in words:
            if word in tfidf_model.vocabulary_:
                tfidf_score += tfidf_model.transform([sentence])[0, tfidf_model.vocabulary_[word]]
        tfidf_scores[idx] = (sentence, tfidf_score)

    sorted_sentences = sorted(tfidf_scores.items(), key=lambda x: x[1][1], reverse=True)
    top_indices = [sentence[0] for sentence in sorted_sentences[:num_sentences]]
    top_sentences = [sentences[idx] for idx in sorted(top_indices)]

    summarized_text = ' '.join(top_sentences)

    return summarized_text

def abstractive_summarize(paragraph, model):
    summarization_template = "Summarize: {text}"
    summarization_prompt = PromptTemplate(input_variables=["text"], template=summarization_template)
    summarization_chain = LLMChain(llm=model, prompt=summarization_prompt)
    summarized_text = summarization_chain.predict(text=paragraph)
    return summarized_text