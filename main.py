import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="OneGPT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# LOAD API KEY
# ==================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

    /* MAIN APP */

    .stApp {
        background-color: #0f1117;
        color: white;
    }


    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background-color: #171923;
        border-right: 1px solid #292d3a;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 20px;
    }


    /* LOGO */

    .logo {
        font-size: 30px;
        font-weight: 700;
        color: white;
        padding-bottom: 25px;
    }

    .logo span {
        color: #8b5cf6;
    }


    /* BUTTONS */

    .stButton > button {

        width: 100%;

        background-color: #242735;

        color: white;

        border: 1px solid #343848;

        border-radius: 10px;

        padding: 10px;

        font-size: 15px;

        transition: 0.2s;
    }

    .stButton > button:hover {

        border-color: #8b5cf6;

        background-color: #2b2e3d;

        color: white;
    }


    /* MAIN WELCOME SCREEN */

    .main-title {

        text-align: center;

        font-size: 48px;

        font-weight: 700;

        margin-top: 120px;

        color: white;
    }

    .subtitle {

        text-align: center;

        color: #8b92a5;

        font-size: 18px;

        margin-bottom: 40px;
    }


    /* CHAT MESSAGES */

    [data-testid="stChatMessage"] {

        background-color: transparent;

        padding: 20px 10%;
    }


    /* CHAT INPUT */

    [data-testid="stChatInput"] {

        background-color: #0f1117;

        padding-bottom: 20px;
    }


    [data-testid="stChatInput"] textarea {

        background-color: #242735 !important;

        color: white !important;

        border: 1px solid #343848 !important;

        border-radius: 15px !important;

    }


    /* REMOVE STREAMLIT MENU */

    #MainMenu {

        visibility: hidden;

    }

    footer {

        visibility: hidden;

    }

    header {

        visibility: hidden;

    }


    /* SIDEBAR TEXT */

    .sidebar-text {

        color: #8b92a5;

        font-size: 13px;

        margin-top: 20px;
    }


    /* FOOTER */

    .footer {

        text-align: center;

        color: #666b7a;

        font-size: 12px;

        margin-top: 20px;

        padding-bottom: 10px;
    }

</style>
""", unsafe_allow_html=True)


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        '<div class="logo">One<span>GPT</span> 🤖</div>',
        unsafe_allow_html=True
    )


    # NEW CHAT BUTTON

    if st.button("＋ New Chat"):

        st.session_state.messages = []

        st.rerun()


    st.markdown("---")


    st.subheader("Recent Chats")


    # SHOW CHAT STATUS

    if len(st.session_state.messages) == 0:

        st.markdown(
            """
            <div class="sidebar-text">
            No conversations yet.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        # Get user messages

        user_messages = [

            message

            for message in st.session_state.messages

            if message["role"] == "user"

        ]


        # Show last few messages

        for message in user_messages[-5:]:

            title = message["content"][:30]

            if len(message["content"]) > 30:

                title += "..."

            st.button(
                "💬 " + title
            )


    st.markdown("---")


    st.markdown(
        """
        <div class="sidebar-text">

        <b>OneGPT</b><br><br>

        Your personal AI assistant.

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# WELCOME SCREEN
# ==================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="main-title">How can I help you?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Ask OneGPT anything.</div>',
        unsafe_allow_html=True
    )


# ==================================================
# DISPLAY CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message(
            "user",
            avatar="👤"
        ):

            st.markdown(
                message["content"]
            )


    elif message["role"] == "assistant":

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            st.markdown(
                message["content"]
            )


# ==================================================
# CHAT INPUT
# ==================================================

user_input = st.chat_input(
    "Message OneGPT..."
)


# ==================================================
# PROCESS USER MESSAGE
# ==================================================

if user_input:

    # ----------------------------------------------
    # SAVE USER MESSAGE
    # ----------------------------------------------

    st.session_state.messages.append(

        {
            "role": "user",
            "content": user_input
        }

    )


    # ----------------------------------------------
    # DISPLAY USER MESSAGE
    # ----------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(
            user_input
        )


    # ----------------------------------------------
    # GENERATE AI RESPONSE
    # ----------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner(
            "OneGPT is thinking..."
        ):

            try:

                response = client.responses.create(

                    model="gpt-5",

                    input=st.session_state.messages

                )


                # GET AI RESPONSE

                ai_response = response.output_text


                # DISPLAY AI RESPONSE

                st.markdown(
                    ai_response
                )


                # SAVE AI RESPONSE

                st.session_state.messages.append(

                    {
                        "role": "assistant",
                        "content": ai_response
                    }

                )


            except Exception as e:

                st.error(
                    f"Error: {e}"
                )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">

    OneGPT can make mistakes.
    Check important information.

    </div>
    """,
    unsafe_allow_html=True
)