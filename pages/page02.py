import streamlit as st
from streamlit_ace import st_ace, THEMES

import lib

# https://github.com/okld/streamlit-ace
def app():
    st.header("Text Editer")
    st.write("""
        - 自由にコードを書きましょう!
            - でも今は何も起こりません😢
        """)
    
    lib.config.side_param()

    with st.container():
        content = st_ace(
                language=st.sidebar.selectbox("Language mode", options=["python", "json", "yaml"], index=0),
                theme=st.sidebar.selectbox("Theme", options=THEMES, index=35),
                font_size=st.sidebar.slider("Font size", 5, 24, 14),
                tab_size=st.sidebar.slider("Tab size", 1, 8, 4),
                show_gutter=st.sidebar.checkbox("Show gutter", value=True),
                key="ace",
                )

    st.text(content)
    # st.write(LANGUAGES)