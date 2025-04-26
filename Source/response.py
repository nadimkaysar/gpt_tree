from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import anthropic
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from langchain.schema import messages_to_dict
from langchain.schema import messages_from_dict
from langchain_community.chat_models import ChatOpenAI
import openai
from langchain_community.llms import OpenAI
from langchain.llms import OpenAI
from openai import OpenAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
#from langchain.chat_models import ChatOpenAI
# pip install langchain openai --upgrade this is use for update
from langchain import OpenAI
from openai import OpenAI
import langchain
#from pydantic import BaseModel
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import streamlit as st
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# memory_final = ConversationBufferMemory(memory_key="history", return_messages=True)
# memory_final = ConversationBufferMemory(human_prefix="Patient", ai_prefix="Therapist", memory_key="history", return_messages=True)

def response_Genration_from_GPT4(tem, user_query,conversation_memory):
  system_msg_template = SystemMessagePromptTemplate.from_template(template=tem)

  human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
  prompt_template = ChatPromptTemplate.from_messages(
                                                    [system_msg_template,
                                                     MessagesPlaceholder(variable_name="history"),
                                                     human_msg_template])

  conversation = ConversationChain(memory=conversation_memory, 
                                   prompt=prompt_template, 
                                   llm=ChatOpenAI(
                                       model= 'gpt-4o',
                                       temperature=0.6, 
                                       openai_api_key=OPENAI_API_KEY), verbose=True)
  response = conversation.predict(input=user_query)
  return response



def SubsetSelection(prompt):
    client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=OPENAI_API_KEY,
        )

    chat_completion = client.chat.completions.create(
            model="gpt-4o",
            temperature = 0,
            response_format={ "type": "json_object" },
            messages=[
                    {"role": "system", "content": "Follow user Prompt"},
                    {"role": "user", "content": prompt}
                ]
        )
    chat_completion = str(chat_completion.choices[0].message.content)
    return chat_completion




