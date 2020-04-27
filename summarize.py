from gensim.summarization.summarizer import summarize

def lambda_handler(event, context):
    text = text_content
    return summarize(text)
