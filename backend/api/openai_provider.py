"""
Use this file if you wish to use Hugging face this is slower than OpenAI

***** Note: I couldn't test this because while creating embeddings I'm getting this error:
Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. 
For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', '
type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}

So, as an alternative I've used HuggingFaceInstructEmbeddings
"""


import dotenv
dotenv.load_dotenv()

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from utils import extract_text_from_pdf
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

### If we want to use agent
# from langchain.agents import AgentExecutor, create_openai_tools_agent

class AgentProvider:
    def __init__(self):
        self.chain = load_qa_chain(OpenAI(), chain_type="stuff")
        self.vector_store = None

        ### If we want to use agent
        # self.prompt = prompt
        # self.agent = self.initialize_agent(prompt)
        # self.agent_executor = AgentExecutor(agent=self.agent, verbose=True)

    def get_text_chunks(self, text):
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=800,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_text(text)
        return chunks

    def create_vector_store(self, text_chunks):
        self.vector_store = FAISS.from_texts(text_chunks, OpenAIEmbeddings())

    async def process_pdf(self, pdf_path):
        try:        
            raw_text = await extract_text_from_pdf(pdf_path)
                
            text_chunks = self.get_text_chunks(raw_text)
            self.create_vector_store(text_chunks)
        except Exception as e:
            raise RuntimeError(f"Error processing PDF: {str(e)}")


    def get_answer(self, query):
        docs = self.vector_store.similarity_search(query)
        res = chain.run(input_documents=docs, question=query)
        return res

    ### If we want to use agent

    # def initialize_agent(self, prompt):
    #     print("Initializing agent")
    #     llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
    #     agent = create_openai_tools_agent(llm,tools=None, prompt=prompt)
    #     return agent

    # def invoke_agent(self, query):
    #     return self.agent_executor.invoke({"input": query})


### Example usage if we are using agent
# from constants import PROMPT
# agent_provider = AgentProvider(PROMPT)
# res = agent_provider.invoke_agent({"question": "What is the weather like today?"})
