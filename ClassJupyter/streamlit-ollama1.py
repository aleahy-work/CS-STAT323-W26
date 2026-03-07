import streamlit as st
import ollama

st.title("Simple Local Chatbot")

# Model selection
model = "llama3.2"

# Chat input
if prompt := st.chat_input("Ask me anything"):
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Call Ollama API without historical context
            response = ollama.chat(model=model, messages=[
                {'role': 'user', 'content': prompt},
            ])
            response_text = response['message']['content']
            st.write(response_text)
