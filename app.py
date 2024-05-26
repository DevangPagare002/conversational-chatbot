import streamlit as st
from groq import Groq
import os
from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from dotenv import load_dotenv
from langchain_community.chat_models import ChatDeepInfra
from prompt import prompt_for_chapter_1
# from new_prompt import sys_prompt
from prompt import sys_prompt
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

load_dotenv()

def main():

    footer="""
    <style>
    a:link , a:visited{
    color: blue;
    background-color: transparent;
    text-decoration: underline;
    }

    a:hover,  a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
    }

    .footer {
    position: relative;
    left: 0;
    bottom: 0;
    width: 100%;
    color: rgb(250, 250, 250);
    color-scheme: dark;
    text-align: center;
    }
    </style>
    <div class="footer">
    <p>Developed by  <a style='display: block; text-align: center;' href="https://github.com/DevangPagare002" target="_blank">Devang Pagare</a> for <a style='display: block; text-align: center;' href="https://www.emergiq.com/" target="_blank">Emergiq</a></p>
    </div>
    """

    api_to_use = st.sidebar.selectbox(
        "Choose the family of models",
        ["Groq Models", "Deepinfra Models"]
    )

    st.session_state.model_family = [{"model_family":api_to_use}]

    if api_to_use=="Groq Models":
        model_selection = st.sidebar.selectbox(
            'Choose a model',
            ['llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it']
        )
        groq_api_key = os.getenv("GROQ_API_KEY")
        llm = ChatGroq(
                groq_api_key=groq_api_key, 
                model_name=model_selection
        )
    elif api_to_use=="Deepinfra Models":
        model_selection = st.sidebar.selectbox(
            'Choose a model',
            ['lizpreciatior/lzlv_70b_fp16_hf', 'mistralai/Mixtral-8x22B-Instruct-v0.1', 'Gryphe/MythoMax-L2-13b-turbo']
        )
        deepinfra_api_key = os.getenv("DEEPINFRA_API_TOKEN")
        llm = ChatDeepInfra(model_id=model_selection)
        llm.model_kwargs = {
            "temperature": 0.2,
            "repetition_penalty": 1.2,
            "max_new_tokens": 250,
            "top_p": 0.9,
        }

    st.title("Testing the LLMs!")
    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 25, value = 10)
    memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

    user_question = st.text_input("Ask a question:")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history=[]
    else:
        for message in st.session_state.chat_history:
            memory.save_context(
                {'input':message['human']},
                {'output':message['AI']}
                )
    
    print(len(st.session_state.chat_history))

    system_prompt = sys_prompt()

    if user_question:

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content = system_prompt
                ),  

                MessagesPlaceholder(
                    variable_name="chat_history"
                ), 

                HumanMessagePromptTemplate.from_template(
                    "{human_input}"
                ),
            ]
        )
        print(prompt)

        conversation = LLMChain(
            llm=llm,  
            prompt=prompt,  
            verbose=True,   
            memory=memory,  
        )

        response = conversation.predict(human_input=user_question)
        message = {'human':user_question,'AI':response}
        st.session_state.chat_history.append(message)
        st.write("Chatbot:", response)
        st.subheader("Chat history - ")
        st.write(st.session_state.chat_history)
    st.markdown(footer,unsafe_allow_html=True)




if __name__ == "__main__":
    main()