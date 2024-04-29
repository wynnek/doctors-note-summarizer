from datetime import datetime
import streamlit as st
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

# Function to write a summary to a text file
def write_to_txt(summary):
    # Create the directory if it does not exist
    if not os.path.exists('summary-reports'):
        os.makedirs('summary-reports')

    # Remove leading space
    summary = summary.lstrip()

    # Format the summary
    headers = ['Patient Name', 'Date of Birth', 'Date of Consultation']
    for header in headers:
        summary = summary.replace(f'{header} :', f'{header}:')
    formatted_summary = summary.replace('\n:', ':')
    sentences = nltk.tokenize.sent_tokenize(formatted_summary)
    formatted_summary = '\n\n'.join(sentences)

    # Get the current date and time
    now = datetime.now()

    # Format the date and time
    datetime_str = now.strftime("%Y-%m-%d-%H-%M-%S")

    # Write the summary to a file named summary-report-{DATETIME}.txt in the summary-reports folder
    output_path = os.path.join('summary-reports', f"summary-report-{datetime_str}.txt")
    with open(output_path, 'w') as f:
        f.write(formatted_summary)

    
# Streamlit app
st.title("Doctor's Note Summarizer")
st.markdown("This app takes a patient's medical report, and summarizes it (below) in a way that is easy to understand.")
st.markdown("In the background, this app also saves the summary as a new .txt file in a folder called 'summary-reports'") 

# Ask for User Input
medical_note = st.text_area('Enter the medical note here:', '')

# User must click this button to summarize the note
if st.button('Summarize'):
    # Generate the summary
    summary = summarize_note(medical_note)

    # Output the summary to the page
    st.markdown("Summary") 
    st.write(summary)

    # Write the summary to a text file
    write_to_txt(summary)
