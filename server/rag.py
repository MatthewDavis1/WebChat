#!/usr/bin/env python3

import argparse
import os
import sys
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredImageLoader,
    WebBaseLoader
)

# Hard-coded VECTOR_STORE_PATH
VECTOR_STORE_PATH = "./vector_store"

class RAGVectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma(
            persist_directory=os.path.abspath(VECTOR_STORE_PATH),
            embedding_function=self.embeddings
        )

    def create_vector_store(self):
        self.vector_store.persist()
        print(f"Vector store created at '{VECTOR_STORE_PATH}'")

    def add_documents(self, file_path):
        if not os.path.exists(file_path):
            print(f"File '{file_path}' does not exist.")
            return
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        
        documents = loader.load()
        self.vector_store.add_documents(documents)
        print(f"Added documents from '{file_path}' to the vector store.")

    def add_images(self, image_path):
        if not os.path.exists(image_path):
            print(f"Image file '{image_path}' does not exist.")
            return
        loader = UnstructuredImageLoader(image_path)
        images = loader.load()
        self.vector_store.add_documents(images)
        print(f"Added images from '{image_path}' to the vector store.")

    def add_webpages(self, webpage_paths):
        loader = WebBaseLoader(webpage_paths)
        documents = loader.load()
        self.vector_store.add_documents(documents)
        print(f"Added webpages from '{webpage_paths}' to the vector store.")

    def query_vector_store(self, query):
        docs = self.vector_store.similarity_search(query)
        for doc in docs:
            print(f"Document ID: {doc.metadata.get('source', 'N/A')}")
            print(f"Content: {doc.page_content}\n")

    def list_documents(self):
        docs = self.vector_store.get()
        if docs["ids"] and docs["documents"]:
            for id, document in zip(docs["ids"], docs["documents"]):
                print(f"Document ID: {id}")
                print(f"Document: {document[:100]}")
                print("\n-----------------------------------\n")
        else:
            print("No documents found.")

    def remove_document(self, doc_id):
        self.vector_store.delete(ids=[doc_id])
        print(f"Removed document with ID '{doc_id}' from the vector store.")

    def get_retriever(self, num_results=2):
        return self.vector_store.as_retriever(search_kwargs={"k": num_results})

    def clear_vector_store(self):
        self.vector_store.delete_collection()
        print("Vector store cleared. All documents have been removed.")

def main():
    vector_store = RAGVectorStore()

    parser = argparse.ArgumentParser(description="RAG Script with LangChain")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create vector store
    subparsers.add_parser("create", help="Create a new vector store")

    # Add documents
    add_parser = subparsers.add_parser("add", help="Add documents to the vector store")
    add_parser.add_argument("file_path", type=str, help="Path to the document file")

    # Add images
    add_image_parser = subparsers.add_parser("add_image", help="Add images to the vector store")
    add_image_parser.add_argument("image_path", type=str, help="Path to the image file")

    # Query
    query_parser = subparsers.add_parser("query", help="Query the vector store")
    query_parser.add_argument("query", type=str, help="Query string")

    # List documents
    subparsers.add_parser("list", help="List all documents in the vector store")

    # Remove document
    remove_parser = subparsers.add_parser("remove", help="Remove a document from the vector store")
    remove_parser.add_argument("doc_id", type=str, help="ID of the document to remove")

    # Clear vector store
    subparsers.add_parser("clear", help="Clear all documents from the vector store")

    # Add webpages
    add_webpages_parser = subparsers.add_parser("add_webpages", help="Add webpages to the vector store")
    add_webpages_parser.add_argument("webpage_paths", type=str, help="Links to the webpages")

    args = parser.parse_args()

    if args.command == "create":
        vector_store.create_vector_store()
    elif args.command == "add":
        vector_store.add_documents(args.file_path)
    elif args.command == "add_image":
        vector_store.add_images(args.image_path)
    elif args.command == "query":
        vector_store.query_vector_store(args.query)
    elif args.command == "list":
        vector_store.list_documents()
    elif args.command == "remove":
        vector_store.remove_document(args.doc_id)
    elif args.command == "clear":
        vector_store.clear_vector_store()
    elif args.command == "add_webpages":
        vector_store.add_webpages([link for link in args.webpage_paths.split(',') if len(link) > 0])
    else:
        parser.print_help()

if __name__ == "__main__":
    main()