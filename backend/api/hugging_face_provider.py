"""
Use this file if you wish to use Hugging face this is slower than OpenAI

Note: I couldn't use open ai because while creating embeddings I'm getting this error:
Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. 
For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', '
type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}

So, as an alternative I've used HuggingFaceInstructEmbeddings
"""

import dotenv
dotenv.load_dotenv()

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import HuggingFaceHub
from utils import extract_text_from_pdf


class AgentProvider:
    def __init__(self):
        self.vector_store = None

    def get_text_chunks(self, text):
        print("Starting Splliting into chuncks")
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=800,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_text(text)
        print("Completed Splliting into chuncks")
        return chunks

    def create_vector_store(self, text_chunks):
        print("Starting Vector Embedding")
        embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        self.vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        print("Completed Vector Embedding")


    async def process_pdf(self, pdf_path):
        try:        
            raw_text = await extract_text_from_pdf(pdf_path)
                
            text_chunks = self.get_text_chunks(raw_text)
            self.create_vector_store(text_chunks)
        except Exception as e:
            raise RuntimeError(f"Error processing PDF: {str(e)}")


    def get_answer(self, query):
        if self.vector_store == None:
            raise ValueError("Embedding is empty")
        try:
            llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
        
            memory = ConversationBufferMemory(
            memory_key='chat_history', return_messages=True)
            conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.vector_store.as_retriever(),
                memory=memory
            )

            answer = conversation_chain.run(query)
            return answer
        except Exception as e:
            print(e)
            raise RuntimeError(f"Error: Please try again! {str(e)}")