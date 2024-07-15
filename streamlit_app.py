import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("👨🏼‍🍳 RamsayGPT")
st.write(
    "This is an AI tutor with the personality of world famous chef Gordon Ramsay! "
)
st.write(

    "This chatbot uses OpenAI's GPT-3.5 model to generate responses. " 
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)
st.header("Using Ramsay GPT:")
st.write(
    "You will be asked about what topic you would like to learn. Once you have chosen a topic, Chef Ramsay can teach you about it in one of three ways:"
)
st.write(
    "1. **Variation**, where RamsayGPT will give you different variations of the topic which will help you study the differences between them \n 2. **Game**, where RamsayGPT will create a game to help you learn the topic  \n 3. **Explain**, where RamsayGPT will give an explanation of the topic"
)
st.write("Feel free to choose the option that best fits your personal learning style! But be careful, RamsayGPT gets impatient if you don't answer the promps correctly :(")


# Ask user for their OpenAI API key via st.text_input.
# Alternatively, you can store the API key in ./.streamlit/secrets.toml and access it
# via st.secrets, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:   # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Initialize chat log with the initial context and greeting
    context = open("RamsayPersonality.txt", "r").read()
    initial_greeting = "Hello, chef! What topic would you like to learn about today?"

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat_log = [{'role': 'assistant', 'content': context}]
        st.session_state.chat_log.append({'role': 'assistant', 'content': initial_greeting})
        st.session_state.messages.append({'role': 'assistant', 'content': initial_greeting})

    # Display the existing chat messages via st.chat_message.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Talk to Chef Ramsay"):
        
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.chat_log,
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.chat_log.append({"role": "assistant", "content": response})
        st.session_state.messages.append({"role": "assistant", "content": response}) 
