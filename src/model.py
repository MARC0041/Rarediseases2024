import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from operator import itemgetter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch


class LLMModel:
    def __init__(self):
        load_dotenv()
        self.model_name = os.getenv("MODEL", "llama3")
        self.model = Ollama(model=self.model_name)
        self.parser = StrOutputParser()

        # Define the prompt template
        self.template = """Answer the question based on the context below. If you can't answer the question, reply "I don't know".
Context: {context}

Question: {question}"""
        self.prompt = PromptTemplate.from_template(template=self.template)
        self.prompt.format(context="Here is some context", question="Here is a question")


    def load_document(self, path):
        """Loads a document from the specified path and extracts its content."""
        loader = PyPDFLoader(path)
        pages = loader.load_and_split()
        return pages

    def create_embeddings(self):
        """Creates embeddings for the provided documents using the Ollama embeddings."""
        embeddings = OllamaEmbeddings(model=self.model_name)
        return embeddings

    def build_search(self, documents):
        """Builds a document search using DocArrayInMemorySearch."""
        embeddings = self.create_embeddings()
        vectorstore = DocArrayInMemorySearch.from_documents(
            documents, embedding=embeddings
        )
        self.retriever = vectorstore.as_retriever()
        return 

    def answer_question(self, question):
        """Answers a question based on the context, question, and provided documents.

        Args:
            context: The context to provide to the model.
            question: The question to be answered.
            documents: A list of documents to search for relevant information.

        Returns:
            The answer generated by the model.
        """
        chain = (
            {
                "context": itemgetter("question") | self.retriever,
                "question": itemgetter("question"),
            }
            | self.prompt
            | self.model
            | self.parser
        )
        return chain.invoke({'question':question})


if __name__ == "__main__":
    # Example usage
    model = LLMModel()
    path = r"C:\Users\TechD\Documents\Marcus\LLMs\Rarediseases2024\data\HPP Papers (PDF) Via Liezl Puzon\10.1002___ajmg.a.33146.pdf"
    pages = model.load_document(path)
    model.build_search(pages)
    print(f"pages: {pages[:2]}")
    questions = [
    # Input questions
    "What is HPP?",
    "Can you give me a summary of HPP?"
    ]
    for q in questions:
        answer = model.answer_question(q)
        print(f"Question: {q}")
        print(f"Answer: {answer}")
