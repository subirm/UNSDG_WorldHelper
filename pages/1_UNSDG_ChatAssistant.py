# We're gathering tools and helpers to make our chat application.

import streamlit as st  # To create a website where you can chat.
import os  # To talk to the computer's system and find where everything is stored.
import json  # To read and write information in a special way that computers understand.
import requests  # To send and receive messages over the internet.
import pandas as pd  # To organize information into neat tables.

import subprocess  # To do special computer commands.
from sidebar import build_sidebar  # To make a cool sidebar for our website, like a drawer.

# We're getting some really smart tools to help our chat application understand and talk about big world problems.
from langchain.chains import ConversationChain
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.vectorstores import Qdrant

from qdrant_client import QdrantClient  # This is like a super-smart library catalog that can find anything instantly.

# We're setting some rules for when we look for information, like only picking the best matches.
NUM_TEXT_MATCHES = 3  # How many pieces of information we want to find.
SIMILARITY_THRESHOLD = 0.83  # How close the information needs to be to what we're asking.

# We're telling our program how to understand and find information in a really smart way.
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
embedding_model_name = "BAAI/bge-small-en"
os.environ['SENTENCE_TRANSFORMERS_HOME'] = './model_cache/'
embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en",
                                      model_kwargs=model_kwargs,
                                      encode_kwargs=encode_kwargs
                                     )

# These are like secret keys that let us access a super-smart brain and catalog.
qdrant_key = st.secrets["qdrant_api_key"]
openai_key = st.secrets["openai_api_key"]
qdrant_client = QdrantClient(host="59f8f159-fb60-44e8-bfc4-9f35c77ca8d4.us-east4-0.gcp.cloud.qdrant.io",
                             api_key=qdrant_key)

# Setting up our chat website with a special name.
st.set_page_config(page_title="UNSDG ChatAssist", layout="wide")

# Creating a drawer (sidebar) with tools and information.
with st.sidebar:
    build_sidebar()

# Keeping track of all the questions and answers in our chat, like a diary.
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Setting up our super-smart brain to think and talk about world problems.
if "conversation" not in st.session_state.keys() or len(st.session_state.messages) <= 1:
    rag_llm = ChatOpenAI(temperature=0, 
                            model='gpt-3.5-turbo-0613',
                            openai_api_key=openai_key)
    st.session_state.conversation = ConversationChain(
        llm=rag_llm,
        memory=ConversationSummaryMemory(llm=rag_llm),
        verbose=True
    )

# Showing all the messages in our chat, like flipping through the pages of a diary.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Asking you to type something into the chat.
if prompt := st.chat_input("Chat with UNSDG Chat Assist"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# This is like having a magnifying glass that helps us find the best information related to what you asked.
def get_relevant_docs(user_input):

    embedded_query = embeddings.embed_query(user_input)

    relevant_docs = qdrant_client.search(
            collection_name="unsdg",
            query_vector=embedded_query,
            limit=NUM_TEXT_MATCHES,
    )

    urls = [result.payload['metadata']['url'] for result in relevant_docs if result.score > SIMILARITY_THRESHOLD]
    titles = [result.payload['metadata']['Report title'] for result in relevant_docs if result.score > SIMILARITY_THRESHOLD]
    contexts = [result.payload['page_content'] for result in relevant_docs if result.score > SIMILARITY_THRESHOLD]

    return urls, titles, contexts

# This is composing a question to our super-smart brain, giving it all the information it needs to come up with a good answer.
def build_system_prompt(user_input):

    urls, titles, contexts = get_relevant_docs(user_input)

    template = """ You are a virtual assistant for UNSDG and your task is to answer questions related to UNSDG which includes general information about UNSDG.

                    Do not hallucinate. If you don't find an answer, you can point user to the official website here: https://sdgs.un.org/goals . 

                    In your response, include the following url links at the end of your response {url_links} and any other relevant URL links that you referred.

                    Also, at the end of your response, ask if your response was helpful". 

                    Here is some relevant context: {context}"""

    prompt_template = PromptTemplate(
        input_variables=["url_links", "context"],
        template=template
    )
    system_prompt = prompt_template.format( url_links=urls, context=contexts)

    return system_prompt

# This is where we ask our AI brain to think about the question and come up with an answer.
def queryAIModel(user_input):

    system_prompt = build_system_prompt(user_input)            
    messages = [
        SystemMessage(
            content=system_prompt
        ),
        HumanMessage(
            content=user_input
        ),
    ]
    output = st.session_state.conversation.predict(input=messages)

    return output

# This is where we actually get the AI brain to talk back to us with an answer.
def generate_response(prompt):
    response_generated = queryAIModel(prompt)
    return response_generated

# If the last thing in our chat wasn't an answer from our assistant, we ask for one now.
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(st.session_state.messages[-1]["content"])
            st.write(response)

    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
