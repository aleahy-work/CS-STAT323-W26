import streamlit as st

st.title("My First Streamlit App")
st.write("Hello, world! This is a simple Streamlit application.")

st.write("""  This is some text.

This is some more text.

This is some new text to see if this really works!!!!!

""")

st.image("leahy-cat2.png", caption="This is my cat")

user_input = st.text_input("Enter some text here:", "Type something...")
st.write("You entered:", user_input)

if st.button("Say Hello"):
    st.write("Hello there!")
