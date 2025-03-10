# import re
# import streamlit as st
# import requests
# import json
# st.title('_:blue[Local GenAI Search]_')
# question = st.text_input("Ask a question based on your local files", "")
# if st.button("Ask a question") or not question=="":
#     st.write("The current question is \"", question+"\"")
#     url = "http://127.0.0.1:5003/ask_localai"

#     payload = json.dumps({
#       "query": question
#     })
#     headers = {
#       'Accept': 'application/json',
#       'Content-Type': 'application/json'
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)

#     answer = json.loads(response.text)["answer"]
#     rege = re.compile("\[Document\ [0-9]+\]|\[[0-9]+\]")
#     m = rege.findall(answer)
#     num = []
#     for n in m:
#         num = num + [int(s) for s in re.findall(r'\b\d+\b', n)]


#     st.markdown(answer)
#     documents = json.loads(response.text)['context']
#     show_docs = []
#     seen_ids = set()

    
#     for n in num:
#         for doc in documents:
#             # if int(doc['id']) == n:
#             #     show_docs.append(doc)
#             if doc['id'] not in seen_ids:
#                 if int(doc['id']) == n:
#                     show_docs.append(doc)
#                     seen_ids.add(doc['id'])
#     a = 1244
#     for doc in show_docs:
#         with st.expander(str(doc['id'])+" - "+doc['path']):
#             st.write(doc['content'])
#             with open(doc['path'], 'rb') as f:
#                 st.download_button("Download file", f, file_name=doc['path'].split('/')[-1],key=a
#                 )
#                 a = a + 1

# import re
# import streamlit as st
# import requests
# import json

# # Initialize session state for chat history if it doesn't exist
# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# st.title('_:blue[Local GenAI Chatbot]_')

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
#         # Display document context if it exists
#         if "documents" in message:
#             for doc in message["documents"]:
#                 with st.expander(f"{doc['id']} - {doc['path']}"):
#                     st.write(doc['content'])
#                     with open(doc['path'], 'rb') as f:
#                         st.download_button(
#                             "Download file",
#                             f,
#                             file_name=doc['path'].split('/')[-1],
#                             key=f"download_{doc['id']}_{len(st.session_state.messages)}"
#                         )

# # Chat input
# if prompt := st.chat_input("What would you like to know about your local files?"):
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Get bot response
#     url = "http://127.0.0.1:5003/ask_localai"
#     payload = json.dumps({
#         "query": prompt
#     })
#     headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json'
#     }

#     try:
#         response = requests.request("POST", url, headers=headers, data=payload)
#         response_data = json.loads(response.text)
#         answer = response_data["answer"]
#         documents = response_data['context']

#         # Extract document references
#         rege = re.compile(r"\[Document\ [0-9]+\]|\[[0-9]+\]")
#         m = rege.findall(answer)
#         num = []
#         for n in m:
#             num = num + [int(s) for s in re.findall(r'\b\d+\b', n)]

#         # Process relevant documents
#         show_docs = []
#         seen_ids = set()
#         for n in num:
#             for doc in documents:
#                 if doc['id'] not in seen_ids and int(doc['id']) == n:
#                     show_docs.append(doc)
#                     seen_ids.add(doc['id'])

#         # Display assistant response in chat message container
#         with st.chat_message("assistant"):
#             st.markdown(answer)
#             for doc in show_docs:
#                 with st.expander(f"{doc['id']} - {doc['path']}"):
#                     st.write(doc['content'])
#                     with open(doc['path'], 'rb') as f:
#                         st.download_button(
#                             "Download file",
#                             f,
#                             file_name=doc['path'].split('/')[-1],
#                             key=f"download_{doc['id']}_{len(st.session_state.messages)+1}"
#                         )

#         # Add assistant response to chat history
#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": answer,
#             "documents": show_docs
#         })

#     except Exception as e:
#         with st.chat_message("assistant"):
#             st.error(f"Error: {str(e)}")
#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": f"Error: {str(e)}"
#         })

# # Add a button to clear chat history
# if st.sidebar.button("Clear Chat History"):
#     st.session_state.messages = []
#     st.rerun()

# import re
# import streamlit as st
# import requests
# import json
# import uuid

# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# st.title('_:blue[Boots GPT]_')

# for message_idx, message in enumerate(st.session_state.messages):
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
#         if "documents" in message:
#             for doc_idx, doc in enumerate(message["documents"]):
#                 with st.expander(f"{doc['id']} - {doc['path']}"):
#                     st.write(doc['content'])
#                     with open(doc['path'], 'rb') as f:
#                         unique_key = f"download_{message_idx}_{doc_idx}_{str(uuid.uuid4())}"
#                         st.download_button(
#                             "Download file",
#                             f,
#                             file_name=doc['path'].split('/')[-1],
#                             key=unique_key
#                         )

# if prompt := st.chat_input("What would you like to know about your local files?"):
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     url = "http://127.0.0.1:5003/ask_localai"
#     payload = json.dumps({
#         "query": prompt
#     })
#     headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json'
#     }

#     try:
#         response = requests.request("POST", url, headers=headers, data=payload)
#         response_data = json.loads(response.text)
#         answer = response_data["answer"]
#         documents = response_data['context']

#         rege = re.compile(r"\[Document\ [0-9]+\]|\[[0-9]+\]")
#         m = rege.findall(answer)
#         num = []
#         for n in m:
#             num = num + [int(s) for s in re.findall(r'\b\d+\b', n)]

#         show_docs = []
#         seen_ids = set()
#         for n in num:
#             for doc in documents:
#                 if doc['id'] not in seen_ids and int(doc['id']) == n:
#                     show_docs.append(doc)
#                     seen_ids.add(doc['id'])

#         with st.chat_message("assistant"):
#             st.markdown(answer)
#             for doc_idx, doc in enumerate(show_docs):
#                 with st.expander(f"{doc['id']} - {doc['path']}"):
#                     st.write(doc['content'])
#                     with open(doc['path'], 'rb') as f:
#                         unique_key = f"download_new_{doc_idx}_{str(uuid.uuid4())}"
#                         st.download_button(
#                             "Download file",
#                             f,
#                             file_name=doc['path'].split('/')[-1],
#                             key=unique_key
#                         )

#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": answer,
#             "documents": show_docs
#         })

#     except Exception as e:
#         with st.chat_message("assistant"):
#             st.error(f"Error: {str(e)}")
#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": f"Error: {str(e)}"
#         })

# if st.sidebar.button("Clear Chat History"):
#     st.session_state.messages = []
#     st.rerun()

# import re
# import streamlit as st
# import requests
# import json
# import uuid
# import time

# if 'messages' not in st.session_state:
#     st.session_state.messages = []
# if 'is_loading' not in st.session_state:
#     st.session_state.is_loading = False

# st.set_page_config(
#     page_title="Boots GPT",
#     page_icon=None,
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# st.markdown("""
# <style>
#     .main .block-container {
#         max-width: 800px;
#         padding-top: 2rem;
#         padding-bottom: 6rem;
#     }
#     .stApp {
#         background-color: white;
#     }
#     header {
#         visibility: hidden;
#     }
#     h1 {
#         text-align: center;
#         margin-bottom: 2rem;
#         font-weight: 400;
#         font-size: 1.8rem;
#     }
#     .stChatMessage > div:first-child {
#         display: none !important;
#     }
#     .stChatMessageContent {
#         width: 100%;
#         padding: 0;
#     }
#     .message-container {
#         padding: 1rem;
#         margin-bottom: 1rem;
#         border-radius: 8px;
#         //border: 1px solid #f0f0f0;
#     }
#     .user-message {
#         float: right;
#         clear: both;
#         max-width: 80%;
#         display: inline-block;
#         background-color: #eff6ff;
#     }
#     .assistant-message {
#         float: left;
#         clear: both;
#         width: 80%;
#         background-color: white;
#     }
#     .messages-container {
#         display: flex;
#         flex-direction: column;
#         width: 100%;
#     }
#     .clearfix::after {
#         content: "";
#         clear: both;
#         display: table;
#     }
#     .stChatInputContainer {
#         position: fixed;
#         bottom: 0;
#         left: 0;
#         right: 0;
#         background-color: white;
#         padding: 1rem;
#         padding-bottom: 2rem;
#         z-index: 100;
#         border-top: 1px solid rgba(0, 0, 0, 0.1);
#         max-width: 800px;
#         margin: 0 auto;
#     }
#     .chat-input {
#         border-radius: 8px;
#         border: 1px solid rgba(0, 0, 0, 0.2);
#     }
#     footer {
#         visibility: hidden;
#     }
#     button[data-testid="baseButton-secondary"] {
#         border-radius: 6px;
#         width: 100%;
#         margin-bottom: 10px;
#         background-color: white;
#         border: 1px solid rgba(0, 0, 0, 0.2);
#     }
#     .stExpander {
#         border: 1px solid rgba(0, 0, 0, 0.1);
#         border-radius: 6px;
#         margin-top: 0.5rem;
#     }
#     .loading-dots {
#         display: flex;
#         justify-content: flex-start;
#         margin: 20px 0;
#         width: 80%;
#         float: left;
#         clear: both;
#     }
#     .loading-dots span {
#         animation: pulse 1.4s infinite;
#         background-color: #555;
#         border-radius: 50%;
#         display: inline-block;
#         height: 8px;
#         margin: 0 4px;
#         width: 8px;
#     }
#     .loading-dots span:nth-child(2) {
#         animation-delay: 0.2s;
#     }
#     .loading-dots span:nth-child(3) {
#         animation-delay: 0.4s;
#     }
#     @keyframes pulse {
#         0% {
#             opacity: 0.4;
#             transform: scale(1);
#         }
#         50% {
#             opacity: 1;
#             transform: scale(1.2);
#         }
#         100% {
#             opacity: 0.4;
#             transform: scale(1);
#         }
#     }
#     .document-source {
#         font-size: 0.85rem;
#         color: #555;
#         margin-top: 10px;
#         font-style: italic;
#     }
#     .document-container {
#         float: left;
#         clear: both;
#         width: 80%;
#         margin-bottom: 1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# with st.sidebar:
#     st.sidebar.title("Boots GPT")
#     if st.sidebar.button("+ New Chat", use_container_width=True):
#         st.session_state.messages = []
#         st.session_state.is_loading = False
#         st.rerun()

# st.title('Boots GPT')

# messages_container = st.container()

# def display_message(message, idx):
#     role = message["role"]
#     content = message["content"]
    
#     with messages_container:
#         if role == "user":
#             st.markdown(f'<div class="message-container user-message">{content}</div><div class="clearfix"></div>', unsafe_allow_html=True)
#         else:  # assistant
#             st.markdown(f'<div class="message-container assistant-message">{content}</div><div class="clearfix"></div>', unsafe_allow_html=True)
            
#             if "documents" in message and message["documents"]:
#                 st.markdown('<div class="document-container">', unsafe_allow_html=True)
#                 for doc_idx, doc in enumerate(message["documents"]):
#                     with st.expander(f"Document: {doc['path'].split('/')[-1]}"):
#                         st.markdown(f"<div class='document-source'>Source: {doc['path']}</div>", unsafe_allow_html=True)
#                         st.text(doc['content'])
#                         with open(doc['path'], 'rb') as f:
#                             unique_key = f"download_{idx}_{doc_idx}_{str(uuid.uuid4())}"
#                             st.download_button(
#                                 "Download",
#                                 f,
#                                 file_name=doc['path'].split('/')[-1],
#                                 key=unique_key
#                             )
#                 st.markdown('</div><div class="clearfix"></div>', unsafe_allow_html=True)

# for message_idx, message in enumerate(st.session_state.messages):
#     display_message(message, message_idx)

# if st.session_state.is_loading:
#     with messages_container:
#         st.markdown("""
#         <div class="loading-dots">
#             <span></span>
#             <span></span>
#             <span></span>
#         </div>
#         <div class="clearfix"></div>
#         """, unsafe_allow_html=True)

# prompt = st.chat_input("Message Boots GPT...", key="chat-input", disabled=st.session_state.is_loading)

# if prompt and not st.session_state.is_loading:
#     display_message({"role": "user", "content": prompt}, len(st.session_state.messages))
#     st.session_state.messages.append({"role": "user", "content": prompt})
    
#     st.session_state.is_loading = True
#     st.rerun()

# if st.session_state.is_loading and st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
#     try:
#         prompt = st.session_state.messages[-1]["content"]
        
#         url = "http://127.0.0.1:5003/ask_localai"
#         payload = json.dumps({
#             "query": prompt
#         })
#         headers = {
#             'Accept': 'application/json',
#             'Content-Type': 'application/json'
#         }
        
#         response = requests.request("POST", url, headers=headers, data=payload)
#         response_data = json.loads(response.text)
#         answer = response_data["answer"]
#         documents = response_data['context']
        
#         rege = re.compile(r"\[Document\ [0-9]+\]|\[[0-9]+\]")
#         m = rege.findall(answer)
#         num = []
#         for n in m:
#             num = num + [int(s) for s in re.findall(r'\b\d+\b', n)]
        
#         show_docs = []
#         seen_ids = set()
#         for n in num:
#             for doc in documents:
#                 if doc['id'] not in seen_ids and int(doc['id']) == n:
#                     show_docs.append(doc)
#                     seen_ids.add(doc['id'])
        
#         new_message = {
#             "role": "assistant",
#             "content": answer,
#             "documents": show_docs
#         }
        
#         display_message(new_message, len(st.session_state.messages))
        
#         st.session_state.messages.append(new_message)
    
#     except Exception as e:
#         error_message = {"role": "assistant", "content": f"Error: {str(e)}"}
#         display_message(error_message, len(st.session_state.messages))
#         st.session_state.messages.append(error_message)
    
#     st.session_state.is_loading = False
    
#     st.rerun()


import re
import streamlit as st
import requests
import json
import uuid
import time
from datetime import datetime
import csv
import io

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(
    page_title="Conversational AI",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="expanded"
)

description = """
    <div style="padding: 1rem; margin-bottom: 2rem; background-color: #f8f9fa; border-radius: 8px;">
        <h3 style="margin-bottom: 1rem;">Welcome to Conversational AI</h3>
        <p>This AI assistant helps you find and analyze information from your documents. 
        Simply type your question and get answers based on the available context.</p>
        <ul style="margin-top: 1rem;">
            <li>Ask questions about your documents</li>
            <li>View relevant source documents</li>
            <li>Download conversations for future reference</li>
            <li>Access chat history</li>
        </ul>
    </div>
"""

st.markdown("""
<style>
    .main .block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }
    .stApp {
        background-color: white;
    }
    header {
        visibility: hidden;
    }
    h1 {
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
        font-size: 1.8rem;
    }
    .stChatMessage > div:first-child {
        display: none !important;
    }
    .stChatMessageContent {
        width: 100%;
        padding: 0;
    }
    .message-container {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 8px;
        //border: 1px solid #f0f0f0;
    }
    .user-message {
        float: right;
        clear: both;
        max-width: 80%;
        display: inline-block;
        background-color: #eff6ff;
    }
    .assistant-message {
        float: left;
        clear: both;
        width: 80%;
        background-color: white;
    }
    .messages-container {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    .clearfix::after {
        content: "";
        clear: both;
        display: table;
    }
    .stChatInputContainer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 1rem;
        padding-bottom: 2rem;
        z-index: 100;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
        max-width: 800px;
        margin: 0 auto;
    }
    .chat-input {
        border-radius: 8px;
        border: 1px solid rgba(0, 0, 0, 0.2);
    }
    footer {
        visibility: hidden;
    }
    button[data-testid="baseButton-secondary"] {
        border-radius: 6px;
        width: 100%;
        margin-bottom: 10px;
        background-color: white;
        border: 1px solid rgba(0, 0, 0, 0.2);
    }
    .stExpander {
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 6px;
        margin-top: 0.5rem;
    }
    .loading-dots {
        display: flex;
        justify-content: flex-start;
        margin: 20px 0;
        width: 80%;
        float: left;
        clear: both;
    }
    .loading-dots span {
        animation: pulse 1.4s infinite;
        background-color: #555;
        border-radius: 50%;
        display: inline-block;
        height: 8px;
        margin: 0 4px;
        width: 8px;
    }
    .loading-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }
    .loading-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }
    @keyframes pulse {
        0% {
            opacity: 0.4;
            transform: scale(1);
        }
        50% {
            opacity: 1;
            transform: scale(1.2);
        }
        100% {
            opacity: 0.4;
            transform: scale(1);
        }
    }
    .document-source {
        font-size: 0.85rem;
        color: #555;
        margin-top: 10px;
        font-style: italic;
    }
    .document-container {
        float: left;
        clear: both;
        width: 80%;
        margin-bottom: 1rem;
    }    
    .history-item {
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #eee;
        border-radius: 4px;
        cursor: pointer;
    }
    .history-item:hover {
        background-color: #f8f9fa;
    }
    .download-button {
        margin-top: 1rem;
        width: 100%;
    }
    .chat-meta {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.sidebar.title("Conversational AI")
    
    if st.sidebar.button("+ New Chat", use_container_width=True):
        if st.session_state.messages:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            first_msg = st.session_state.messages[0]["content"][:50] + "..."
            st.session_state.chat_history.append({
                "preview": first_msg,
                "messages": st.session_state.messages.copy(),
                "timestamp": timestamp

            })
        st.session_state.messages = []
        st.session_state.is_loading = False
        st.rerun()
    
    st.sidebar.markdown("### Chat History")
    for idx, chat in enumerate(st.session_state.chat_history):
        if st.sidebar.button(
            f"{chat['preview']}\n{chat['timestamp']}", 
            key=f"history_{idx}",
            use_container_width=True
        ):
            st.session_state.messages = chat['messages'].copy()
            st.rerun()

    if st.session_state.messages:
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["Timestamp", "Role", "Content"])
        
        for msg in st.session_state.messages:
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                msg["role"],
                msg["content"]
            ])
        
        st.sidebar.download_button(
            label="Download Conversation",
            data=buffer.getvalue(),
            file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

st.markdown(description, unsafe_allow_html=True)
#st.title('Boots GPT')


messages_container = st.container()
 
def display_message(message, idx):
    role = message["role"]
    content = message["content"]
   
    with messages_container:
        if role == "user":
            st.markdown(f'<div class="message-container user-message">{content}</div><div class="clearfix"></div>', unsafe_allow_html=True)
        else:  # assistant
            st.markdown(f'<div class="message-container assistant-message">{content}</div><div class="clearfix"></div>', unsafe_allow_html=True)
           
            if "documents" in message and message["documents"]:
                st.markdown('<div class="document-container">', unsafe_allow_html=True)
                for doc_idx, doc in enumerate(message["documents"]):
                    with st.expander(f"Document: {doc['path'].split('/')[-1]}"):
                        st.markdown(f"<div class='document-source'>Source: {doc['path']}</div>", unsafe_allow_html=True)
                        st.text(doc['content'])
                        with open(doc['path'], 'rb') as f:
                            unique_key = f"download_{idx}_{doc_idx}_{str(uuid.uuid4())}"
                            st.download_button(
                                "Download",
                                f,
                                file_name=doc['path'].split('/')[-1],
                                key=unique_key
                            )
                st.markdown('</div><div class="clearfix"></div>', unsafe_allow_html=True)
 
for message_idx, message in enumerate(st.session_state.messages):
    display_message(message, message_idx)
 
if st.session_state.is_loading:
    with messages_container:
        st.markdown("""
        <div class="loading-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
        <div class="clearfix"></div>
        """, unsafe_allow_html=True)
 
prompt = st.chat_input("Ask a Question...", key="chat-input", disabled=st.session_state.is_loading)
 
if prompt and not st.session_state.is_loading:
    display_message({"role": "user", "content": prompt}, len(st.session_state.messages))
    st.session_state.messages.append({"role": "user", "content": prompt})
   
    st.session_state.is_loading = True
    st.rerun()
 
if st.session_state.is_loading and st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    try:
        prompt = st.session_state.messages[-1]["content"]
       
        url = "http://127.0.0.1:5003/ask_localai"
        payload = json.dumps({
            "query": prompt
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
       
        response = requests.request("POST", url, headers=headers, data=payload)
        response_data = json.loads(response.text)
        answer = response_data["answer"]
        documents = response_data['context']
       
        rege = re.compile(r"\[Document\ [0-9]+\]|\[[0-9]+\]")
        m = rege.findall(answer)
        num = []
        for n in m:
            num = num + [int(s) for s in re.findall(r'\b\d+\b', n)]
       
        show_docs = []
        seen_ids = set()
        for n in num:
            for doc in documents:
                if doc['id'] not in seen_ids and int(doc['id']) == n:
                    show_docs.append(doc)
                    seen_ids.add(doc['id'])
       
        new_message = {
            "role": "assistant",
            "content": answer,
            "documents": show_docs
        }
       
        display_message(new_message, len(st.session_state.messages))
       
        st.session_state.messages.append(new_message)
   
    except Exception as e:
        error_message = {"role": "assistant", "content": f"Error: {str(e)}"}
        display_message(error_message, len(st.session_state.messages))
        st.session_state.messages.append(error_message)
   
    st.session_state.is_loading = False
   
    st.rerun()