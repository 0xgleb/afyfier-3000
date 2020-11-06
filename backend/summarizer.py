from transformers import pipeline

summarizer = pipeline("summarization")

def summarize(text):
    summarizer(text, max_length=60, min_length=30)[0]['summary_text']

print(summarize('If an event of default occurs we may demand immediate repayment of the Loan in writing.\n While we will always try to work with you to agree a way forward, if a default event occurs and we’re unable to agree a solution with you, we may demand immediate repayment of your Loan.'))
