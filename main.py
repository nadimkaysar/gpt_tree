# import streamlit as st
# from streamlit_chat import message
# import openai
# import os
# import Source.response as Response
# import Source.promptInitialization as PromptInisilization
# #import Source.mcta as MCTS
# import json
# #import Source.treegraph as treeBuild
# import Source.treegraphCriteria as treeBuildCriteria
# from langchain.memory import ConversationBufferMemory
# memory = ConversationBufferMemory(human_prefix="human", ai_prefix="AI",memory_key="history", return_messages=True)

# st.title("Well-Being Support For Student")
# USER_NAME = "user"
# ASSISTANT_NAME = "assistant"
# State_component = "State"
# end_greeting = ['Thanks','thanks','Thank You','thank you','Thanks for your information','thanks for your instruction', 'thanks for your suggestions']

# message_history = []

# patient_messages = []
# therapist_messages = []
# therapist_messages_last_utterace = ""
# patient_messages_last_utterace = ""
# subset_list =[]
# formatted_data = []
# def archive_messages(log_conversation_from_session):
#     # Iterate through messages and separate them based on the 'Name' key
#     """
#     for message in log_conversation_from_session:
#         message_history.append((message['Name'],':', message['msg'],' \n'))

#     print("The Message")
#     print(message_history)"""
    
#     for message in log_conversation_from_session:
#         if message['name'] == 'user':
#             patient_messages.append(message['msg'])
#         elif message['name'] == 'assistant':
#             therapist_messages.append(message['msg'])
    
#     for i in range(len(patient_messages)):
#         message_history.append("Patient :" + patient_messages[i] + '\n')
#         message_history.append("Therapist :" + therapist_messages[i] + '\n')

# # Create a mapping for i values based on the key
# key_to_i_mapping = {
#     "Impact on well-being": 1,
#     "User Goal Achievement": 2,
#     "User Satisfaction": 3,
#     "Feedback Quality": 4
# }

# utility_score_list = []

# def data_extraction(data_dict):
#     # Category you want to process
#     Mindfullness_data = data_dict['predictions']['Mindfulness']
#     Distress_Tolerance_data = data_dict['predictions']['Distress_Tolerance']
#     Interpersonal_Effectiveness_data = data_dict['predictions']['Interpersonal_Effectiveness']
#     Emotion_Regulation_data = data_dict['predictions']['Emotion_Regulation']
    
#     # For Mindfullness
#     utility_for_mindfullness = 0.0
#     for state in Mindfullness_data["possible_states"]:
#         probability = float(state["probability"])
#         reward = float(state["reward"])
#         utility_for_mindfullness += probability * reward
#     utility_score_list.append(float(utility_for_mindfullness))
    
#     # For DT
#     utility_for_Distress_Tolerance = 0.0
#     for state in Distress_Tolerance_data["possible_states"]:
#         probability = float(state["probability"])
#         reward = float(state["reward"])
#         utility_for_Distress_Tolerance += probability * reward
#     utility_score_list.append(float(utility_for_Distress_Tolerance))
    
#     # For IE
#     utility_for_Interpersonal_Effectiveness = 0.0
#     for state in Interpersonal_Effectiveness_data["possible_states"]:
#         probability = float(state["probability"])
#         reward = float(state["reward"])
#         utility_for_Interpersonal_Effectiveness += probability * reward
#     utility_score_list.append(float(utility_for_Interpersonal_Effectiveness))
    
#     # For ER
#     utility_for_Emotion_Regulation = 0.0
#     for state in Emotion_Regulation_data["possible_states"]:
#         probability = float(state["probability"])
#         reward = float(state["reward"])
#         utility_for_Emotion_Regulation += probability * reward
#     utility_score_list.append(float(utility_for_Emotion_Regulation))

#     print("All Utility score: ", utility_score_list)

#     if utility_score_list.index(max(utility_score_list)) == 0:
#       return "Mindfulness"
    
#     if utility_score_list.index(max(utility_score_list)) == 1:
#       return "Distress Tolerance"
    
#     if utility_score_list.index(max(utility_score_list)) == 2:
#       return "Interpersonal Effectiveness"
    
#     if utility_score_list.index(max(utility_score_list)) == 3:
#       return "Emotion Regulation"
  

# if "chat_log" not in st.session_state:
#     st.session_state.chat_log = []
#     st.session_state.state_log = []

# st.session_state['ABC'] = None

# utterance_list = []
# user_msg = st.chat_input("Enter Your Thought")

# if 'count' not in st.session_state: 
#     st.session_state.count = 0

# if st.chat_input:
#     st.session_state.count += 1

# if 'stage' not  in st.session_state:
#     st.session_state['stage'] = None

# print('Count = ' + str(st.session_state.count))

# if user_msg:
#     # 
#     for chat in st.session_state.chat_log:
#         with st.chat_message(chat["name"]):
#             st.write(chat["msg"])

#     with st.chat_message(USER_NAME):
#         st.write(user_msg)
#     test_key = 1

#     if 'action' not in st.session_state:
#         st.session_state.action = None

#     # promptInitilize and StateDefine
#     # stateSelectionPrompt = PromptInisilization.stateDefine(history, user_msg)
#     if st.session_state.count >= 2:
#         # Conversation Archieve
#         archive_messages(st.session_state.chat_log)
        
#         # Determine The Reward
#         #Subset_prompt  = PromptInisilization.determine_reward_final(message_history,user_msg,st.session_state.action)
#         #actual_reward = Response.SubsetSelection(Subset_prompt)
#         # print("Before Extract Reawrd: ",actual_reward)
#         #reward_data = json.loads(actual_reward)
#         #print("Reward After Json Data", reward_data)
        
#         # Determine The Reward with Criteria for OpenAI
#         # Subset_prompt  = PromptInisilization.subset_detection_with_weight(message_history,user_msg,st.session_state.action)
#         # actual_reward = Response.SubsetSelection(Subset_prompt)
#         # print("Before Extract Reawrd: ",actual_reward)
#         # reward_data = json.loads(actual_reward)
#         # print("Reward After Json Data", reward_data)
        
#         # Determine The Reward with Criteria for Antropic
#         Subset_prompt  = PromptInisilization.subset_detection_with_weight(message_history,user_msg,st.session_state.action)
#         actual_reward = Response.SubsetSelection_Anthropic_test(Subset_prompt)
#         print("Before Extract Reawrd: ",actual_reward)
#         reward_data = json.loads(actual_reward)
#         print("Reward After Json Data", reward_data)

        
#         # Data Extraction
#         best_action = treeBuildCriteria.dataImport(reward_data)

#         st.session_state.action = best_action
        
#         # MCTS Code Implimentation
#         # mcts_prompt = PromptInisilization.MCTS_prompt(message_history,user_msg)
#         # subset = MCTS.testMCTS(mcts_prompt)
#         # print("Test Subset from MCTS", subset)
#         # subset = "problem_understand"
#     else:
#         best_action = "problem_understand"
#         st.session_state.action = best_action
#         print("Test Subset Print: ",best_action)
    
#     # promptType = PromptInisilization.EnglishConversationPromptForGPT4oV8_testing(message_history,best_action,user_msg)
#     promptType = PromptInisilization.EnglishConversationPromptFor_Student_V11(message_history,best_action,user_msg)
#     # promptType = PromptInisilization.JapaneseConversationPromptFor_Student_V11(message_history,best_action,user_msg)
#     # promptType = PromptInisilization.EnglishConversationPromptForGPT4oV7_japansese(message_history,best_action,user_msg)
    
#     # promptType = PromptInisilization.JapaneseConversationPromptForGPT4o(message_history,subset,patient_messages)
 
#     # Save in Memory for Management
#     if 'chat_history' not in st.session_state:
#          st.session_state.chat_history = []
#     else:
#          for message in st.session_state.chat_history:
#               memory.save_context({'input':message['human']},{'output':message['AI']})

#     # Response Generation
#     response = Response.response_generation_from_antropic(promptType,user_msg,memory)
#     # response = Response.response_Genration_from_GPT4(promptType,user_msg,memory)
#     print("Final Response: ",response)
    
#     # Save in Session
#     message = {'human':user_msg,'AI':response}
#     st.session_state.chat_history.append(message)

#     with st.chat_message(ASSISTANT_NAME):
#         assistant_msg = ""
#         assistant_response_area = st.empty()
#         # for chunk in response:
#         tmp_assistant_msg = response
#         assistant_msg += tmp_assistant_msg
#         assistant_response_area.write(assistant_msg)

#     st.session_state.state_log.append({"name": State_component, "msg": best_action})
#     # print("State Log Print for the system: ", st.session_state.state_log )
#     st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
#     st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})

import streamlit as st
from streamlit_chat import message
import openai
import os
import streamlit as connections
from sqlalchemy import text

neon = st.secrets["neon"]

# Initialize connection with kwargs
conn = st.connection("neondb", type="sql", url=neon)


name = "nadim"
password = "12345"
email = "nadimkaysar1@gmail.com"
if st.button("Insert"):
    if name and email:
        with conn.session as session:
            session.execute(
                text("INSERT INTO user (name, email, password) VALUES (:name, :email, :password);"),
                {"name": name, "email": email, "password":password}
            )
            session.commit()
        st.success("✅ Data inserted successfully!")
    else:
        st.error("❗ Please fill in all fields.")
