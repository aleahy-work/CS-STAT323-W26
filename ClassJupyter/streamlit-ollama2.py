import streamlit as st
import ollama

# --- App Configuration ---
st.set_page_config(page_title="Simple Ollama Chatbot")
st.title("Simple Ollama Chatbot")

# Define the local model to use
OLLAMA_MODEL = "llama3.2" 

# --- Session State Management ---
# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input and LLM Interaction ---
if prompt := st.chat_input("Say something"):
    # Add user message to chat history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get the assistant's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Call the Ollama API with the full conversation history
        # Streaming the response tokens for a better user experience
        stream = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )

        for chunk in stream:
            full_response += chunk['message']['content']
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
