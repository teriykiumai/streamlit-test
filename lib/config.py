import streamlit as st

def remove_menu_footer():
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def side_param():
    st.sidebar.write("---")
    st.sidebar.title("⚙️ Parameters")