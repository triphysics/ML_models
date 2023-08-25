import os, sys
import PyPDF2
import re
import openai

__author__ = "Lucas Soares"
# Here I assume you are on a Jupiter Notebook and download the paper directly from the URL
# !curl -o paper.pdf https://arxiv.org/pdf/2301.00810v3.pdf?utm_source=pocket_saves

openai.api_key=""
# Set the string that will contain the summary     
pdf_summary_text = ""
# Open the PDF file
pdf_file_path = sys.argv[1]
# Read the PDF file using PyPDF2
pdf_file = open(pdf_file_path, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
# Loop through all the pages in the PDF file
pdf_combined = []
for page_num in range(len(pdf_reader.pages)):
    # Extract the text from the page
    page_text = pdf_reader.pages[page_num].extract_text().lower()
    
    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful research assistant."},
                        {"role": "user", "content": f"Summarize this and tabulate new data compared to literature: {page_text}"},
                        # {"role": "user", "content": f"Summarize this and tabulate new data compared to literature: {page_text}"}, ## uncomment if also want to collect data
                            ],
                                )
    page_summary = response["choices"][0]["message"]["content"]
    pdf_summary_text+=page_summary + "\n"
    pdf_summary_file = pdf_file_path.replace(os.path.splitext(pdf_file_path)[1], "_summary.txt")
    # pdf_combined += page_text
    with open(pdf_summary_file, "w+") as file:
        file.write(pdf_summary_text)

response_ = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant."},
                    {"role": "user", "content": f"What is the new finding in this summary of a research paper, if any, that has not been discussed before: {pdf_summary_text}"},
                        ],
                            )
page_summary_ = response_["choices"][0]["message"]["content"]
pdf_summary_file = pdf_file_path.replace(os.path.splitext(pdf_file_path)[1], "_summary.txt")
with open(pdf_summary_file, "a") as file:
    file.write(page_summary_)

# pdf_file.close()
# file.close()

# with open(pdf_summary_file, "r") as file:
#     print(file.read())
