import streamlit as st
from groq import Groq
import os
from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
import time
from dotenv import load_dotenv
from langchain_community.chat_models import ChatDeepInfra
from prompts.chapter1.prompt import prompt_for_chapter_1
# from new_prompt import sys_prompt
from prompts.chapter1.prompt import chapter_0
from prompts.chapter1.prompt import prompt_for_chapter_2
from prompts.chapter1.prompt import attempt12
from prompts.chapter1.prompt import attempt13
from prompts.chapter1.prompt import attempt14
from prompts.chapter1.prompt import attempt15
from prompts.chapter1.prompt import attempt16
from prompts.chapter1.prompt import attempt17
from prompts.chapter2.prompt import attempt1
from prompts.chapter2.prompt import attempt2
from prompts.chapter3.prompt import chapter3_prompt
from cdifflib import CSequenceMatcher
import difflib
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

load_dotenv()

def using_difflib():
    boring_json = {
      "IndicatingDisinterestOrWantingToEndConversation": {
        "OneWordResponses": [
          "Okay",
          "Sure",
          "Yeah",
          "Fine",
          "Cool",
          "K"
        ],
        "NoncommittalOrVagueReplies": [
          "Maybe",
          "I guess",
          "Not sure",
          "We'll see"
        ],
        "ExplicitExpressionsOfDisinterest": [
          "I don't care",
          "Whatever",
          "It doesn't matter",
          "Not really interested",
          "Let's drop it"
        ],
        "MinimalEngagement": [
          "Uh-huh",
          "Mm-hmm",
          "Right",
          "Got it"
        ]
      },
      "IndicatingDesireToChangeTopic": {
        "RedirectingStatements": [
          "Anyway...",
          "By the way...",
          "That reminds me...",
          "Speaking of which..."
        ],
        "QuestionsToShiftFocus": [
          "Have you heard about...?",
          "What do you think about...?",
          "Did you see...?",
          "What's your opinion on...?"
        ],
        "StatementsSignalingShift": [
          "On a different note...",
          "Changing the subject...",
          "That’s enough about that...",
          "Let’s talk about something else..."
        ]
      },
      "NonVerbalCuesInTextForm": {
        "DelaysInResponse": [
          "Taking a long time to reply",
          "Responding with \"...\""
        ],
        "UseOfEmojis": [
          "👍",
          "😐",
          "😴"
        ]
      }
    }
    boring_list = boring_json["IndicatingDisinterestOrWantingToEndConversation"]["OneWordResponses"] + boring_json["IndicatingDisinterestOrWantingToEndConversation"]["NoncommittalOrVagueReplies"] + boring_json["IndicatingDisinterestOrWantingToEndConversation"]["ExplicitExpressionsOfDisinterest"]
    if len(st.session_state.chat_history) > 3:
        li = st.session_state.chat_history[-3:]
        new_li = []
        for i in li:
            new_li.append(i["human"])
        print(new_li)
        print(boring_list)
        print(li)
        s = difflib.SequenceMatcher(None, new_li, boring_list)
        print("########################################################")
        print(s.ratio())
        print("############################################")
        return s.ratio()

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

    if len(st.session_state.chat_history) == 20:
        with st.spinner('Changing to chapter 2...please wait!'):
            time.sleep(5)
        st.success('Done!')
    if len(st.session_state.chat_history) == 40:
        with st.spinner('Changing to chapter 3...please wait!'):
            time.sleep(5)
        st.success('Done!')

    if len(st.session_state.chat_history) >= 40:
        print("chapter 3")
        system_prompt = chapter3_prompt()
    elif len(st.session_state.chat_history) >= 20: 
        print("chapter 2")
        system_prompt = attempt1()
    else:
        print("chapter 1")
        system_prompt = attempt15()
    
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
        # st.write(using_difflib())
    st.markdown(footer,unsafe_allow_html=True)




if __name__ == "__main__":
    main()