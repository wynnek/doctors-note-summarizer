from django.shortcuts import render
from .forms import SummarizerForm
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Check if the necessary NLTK packages are downloaded
def check_nltk_packages():
    nltk_packages = ['punkt', 'stopwords']
    for package in nltk_packages:
        try:
            nltk.data.find('tokenizers/' + package)
        except LookupError:
            nltk.download(package)

# Call the function to check and download the necessary NLTK packages
check_nltk_packages()

# Function to summarize a medical note
def summarize_note(medical_note):
    
    # Use Natural Language Toolkit (NLTK) library to preprocess the text (e.g., tokenization, stemming, removing stop words)
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(medical_note)

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(medical_note)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    # Average value of a sentence from the original report
    average = int(sumValues / len(sentenceValue))

    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence
    return summary

# View for the summarizer
def summarizer(request):
    if request.method == "POST":
        filled_form = SummarizerForm(request.POST)
        if filled_form.is_valid():
            medical_note = filled_form.cleaned_data["text"]
            summary = medical_note # summarize_note(medical_note)
            return render(request, "summarizer/home.html", {"summarizerform": filled_form, "summarizednote": summary})
    else:
        form = SummarizerForm()
        return render(request, "summarizer/home.html", {'summarizerform': form})
