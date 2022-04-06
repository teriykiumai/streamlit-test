import time

import streamlit as st
import pandas as pd

import lib
import pages

# login 
def app():
    page_links = {
        "Deta Editer": pages.page01,
        "Code Editer": pages.page02,
        "Pict Editer": pages.page03,
        "Post Profiling": pages.page04,
    }
    # pagesで選択したファイルのapp関数を発火
    with st.sidebar:
        st.header("📺 Navigation")

        with st.expander("✈ アプリ選択 ✈"):
            selection = st.radio("機能一覧", options=list(page_links.keys()))

            if st.session_state['authentication_status']:
                st.write("-"*3)
                if st.button("ログアウト"):
                    st.session_state['authentication_status'] = None
                    st.experimental_rerun()
    # 各ページモジュールのappを実行
    page_links[selection].app()


### TEST CODE ###
if __name__ == "__main__":  
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None  
    app()


