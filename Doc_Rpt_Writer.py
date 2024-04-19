import streamlit as st
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import io
import re

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

# Function to load and read a text file
def load_and_read_txt(file):
    report = file.getvalue().decode('utf-8')
    
    # Extract the patient's name
    patient_name = None
    for line in report.split('\n'):
        if line.startswith('Patient Name:'):
            patient_name = line.split(':')[-1].strip()
            break

    return report, patient_name

# Function to summarize a report
def summarize_report(report):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(report)

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(report)
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
def write_to_txt(summary, patient_name):
    # Create the directory if it does not exist
    if not os.path.exists('summary-reports'):
        os.makedirs('summary-reports')

    # Format the patient name
    patient_name = patient_name.replace(' ', '_')

    # Remove leading space
    summary = summary.lstrip()

    # Format the summary
    headers = ['Patient Name', 'Date of Birth', 'Date of Consultation']
    for header in headers:
        summary = summary.replace(f'{header} :', f'{header}:')
    formatted_summary = summary.replace('\n:', ':')
    sentences = nltk.tokenize.sent_tokenize(formatted_summary)
    formatted_summary = '\n\n'.join(sentences)

    output_path = os.path.join('summary-reports', f"{patient_name}_Summary.txt")
    with open(output_path, 'w') as f:
        f.write(formatted_summary)

    
# Streamlit app
st.title('Patient\'s Medical Report Summarizer')
st.markdown("This App reads in a patient's medical report and writes it into a more easily readable format, without the heavy technical medical or health-related terminologies") 
st.markdown("Please upload a patient's medical report in .txt format to get started.")

file = st.file_uploader('Upload a patient\'s medical report', type=['txt'])

if file is not None:
    report, patient_name = load_and_read_txt(file)
    summary = summarize_report(report)
    if patient_name:
        write_to_txt(summary, patient_name)
        st.write(summary)
    else:
        st.write("Could not extract patient's name from the report.")