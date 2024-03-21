
import pandas as pd
import streamlit as st
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql.base import SQLDatabaseChain, SQLDatabaseSequentialChain
from langchain.prompts.prompt import PromptTemplate
import os

from dotenv import load_dotenv
load_dotenv()

st.title("Mysql database query helper")

QUERY = """
Given an input question, first create a syntactically correct mysql query to run, then look at the results of the query and return the answer and the sql query used.
.Never query for all columns from a table. You must query only the columns that are needed to answer the question.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Reply I don't know if you are not sure of the answer
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here\n
{question}

"""

with st.sidebar:
    
    username = st.sidebar.text_input("enter username")
    host = st.sidebar.text_input("Enter the host of your database ")
    db_name = st.sidebar.text_input("Enter the name of your database ,include no special characters")
    password = st.sidebar.text_input("Enter password include no special characters ")
    
    OPENAI_API_KEY = st.sidebar.text_input('Enter api_key', type = 'password')

    if OPENAI_API_KEY:
        db = SQLDatabase.from_uri(f'mysql://{username}:{password}@{host}/{db_name}')
        llm=OpenAI(temperature=0.1, openai_api_key=OPENAI_API_KEY)
        db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

prompt = st.text_input("Question: ")
if prompt:
    question = QUERY.format(question=prompt)
    st.header("Answer")
    st.write(db_chain.run(question))
 