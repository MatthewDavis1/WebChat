#!/usr/bin/env python3

from langchain_openai import ChatOpenAI
from rag import RAGVectorStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
import argparse

class QAChat:
    def __init__(self, model="gpt-3.5-turbo", temperature=0):
        self.vector_store = RAGVectorStore()
        self.retriever = self.vector_store.get_retriever()
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.rag_chain = self._create_rag_chain()

    @staticmethod
    def _format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def _create_rag_chain(self):
        prompt = PromptTemplate.from_template(
            "Answer the question based on the context: {context}\n\nQuestion: {question}"
        )
        return (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def ask_question(self, question):
        return self.rag_chain.invoke(question)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", type=str, required=True)
    args = parser.parse_args()

    qa_chat = QAChat()
    print(qa_chat.ask_question(args.question))

if __name__ == "__main__":
    main()
