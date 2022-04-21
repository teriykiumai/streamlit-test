import streamlit as st

import pages

# login 
def app():
    page_links = {
        "作成中": pages.music,
        "Data Editter": pages.page01,
        "Code Editter": pages.page02,
        "Pict Editter": pages.page03,
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
    import lib
    st.set_page_config(page_title='owllwo', page_icon='owl',layout="wide")
    lib.config.remove_menu_footer()
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None  

    app()


