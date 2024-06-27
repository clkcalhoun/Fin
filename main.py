import random
import streamlit as st
import openai
import time
import hmac

# Set your OpenAI Assistant ID here
assistant_id = st.secrets["assistant_id"]

# Initialize the OpenAI client (ensure to set your API key in the sidebar within the app)
openai.api_key = st.secrets["OPENAI_API_KEY"]
client = openai

# Initialize session state variables for file IDs and chat control
if "file_id_list" not in st.session_state:
    st.session_state.file_id_list = []

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Set up the Streamlit page with a title and icon
st.set_page_config(page_title="Fin", page_icon=":speech_balloon:")

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here
st.title("Hello, I'm Fin")
st.write("Ask me questions about your finances")

# # Define the function to process messages with citations
# def process_message_with_citations(message):
#     """Extract content and annotations from the message and format citations as footnotes."""
#     message_content = message.content[0].text
#     annotations = message_content.annotations if hasattr(message_content, 'annotations') else []
#     citations = []

#     # Iterate over the annotations and add footnotes
#     for index, annotation in enumerate(annotations):
#         # Replace the text with a footnote
#         message_content.value = message_content.value.replace(annotation.text, f' [{index + 1}]')

#         # Gather citations based on annotation attributes
#         if (file_citation := getattr(annotation, 'file_citation', None)):
#             # Retrieve the cited file details (dummy response here since we can't call OpenAI)
#             cited_file = {'filename': 'cited_document.pdf'}  # This should be replaced with actual file retrieval
#             citations.append(f'[{index + 1}] {file_citation.quote} from {cited_file["filename"]}')
#         elif (file_path := getattr(annotation, 'file_path', None)):
#             # Placeholder for file download citation
#             cited_file = {'filename': 'downloaded_document.pdf'}  # This should be replaced with actual file retrieval
#             citations.append(f'[{index + 1}] Click [here](#) to download {cited_file["filename"]}')  # The download link should be replaced with the actual download path

#     # Add footnotes to the end of the message content
#     full_response = message_content.value + '\n\n' + '\n'.join(citations)
#     return full_response




# Only show the chat interface if the chat has been started
# if st.session_state.start_chat:
thread = client.beta.threads.create()
st.session_state.thread_id = thread.id
# Initialize the model and messages list if not already in session state
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-4o"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages in the chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input for the user
if prompt := st.chat_input("Message Fin"):
    # Add user message to the state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add the user's message to the existing thread
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt
    )

    # Create a run with additional instructions
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id,
    )

    # Poll for the run to complete and retrieve the assistant's messages
    while run.status != 'completed':
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=run.id
        )

    # Retrieve messages added by the assistant
    messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread_id,
        order="asc"
    )

    # Process and display assistant messages
    assistant_messages_for_run = [
        message for message in messages 
        if message.run_id == run.id and message.role == "assistant"
    ]
    for message in assistant_messages_for_run:
        # full_response = process_message_with_citations(message)
        st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
        with st.chat_message("assistant"):
            st.markdown(message.content[0].text.value, unsafe_allow_html=True)
            

    # if prompt := st.chat_input("What is up?"):
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    #     with st.chat_message("user"):
    #         st.markdown(prompt)

    #     with st.chat_message("assistant"):
    #         stream = client.chat.completions.create(
    #             model=st.session_state["openai_model"],
    #             messages=[
    #                 {"role": m["role"], "content": m["content"]}
    #                 for m in st.session_state.messages
    #             ],
    #             stream=True,
    #         )
    #         response = st.write_stream(stream)
    #     st.session_state.messages.append({"role": "assistant", "content": response})
# else:
#     st.write("Click 'Start Chat' on the left to begin the conversation.")
#     st.button("Start Chat")
#     st.session_state.start_chat = True
#     thread = client.beta.threads.create()
#     st.session_state.thread_id = thread.id
