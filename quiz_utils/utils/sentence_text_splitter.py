from nltk.tokenize import sent_tokenize
import nltk



class SentenceTextSplitter:
    def __init__(self, chunk_size=3, chunk_overlap=1):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_documents(self, docs):
        text = ""
        for doc in docs:
            text += doc.page_content.strip("\n")
            sentences = sent_tokenize(text)
            for i in range(0, len(sentences), self.chunk_size - self.chunk_overlap):
                chunk = sentences[i:i + self.chunk_size]
                yield ' '.join(chunk)



if __name__ == "__main__":
    nltk.download('punkt_tab')