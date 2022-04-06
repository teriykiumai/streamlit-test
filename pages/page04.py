import pandas as pd
import pandas_profiling
from PIL import Image 
from sklearn import datasets
import streamlit as st
from streamlit_pandas_profiling import st_profile_report


@st.cache(allow_output_mutation=True)
def read_iris():
    iris = datasets.load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    return df

@st.cache(allow_output_mutation=True)
def create_profile(df):
    pr = pandas_profiling.ProfileReport(df)
    return pr

def app():
    st.header("データ分析")
    image = Image.open('./img/page04/pp.png')

    emp = st.empty()

    with st.sidebar:
        st.header("⚙️ Parameters")
        plot_data = st.selectbox("データの選択", ["iris"])
        st.image(image,use_column_width=True)

    if plot_data == "iris":
        df = read_iris()
        emp.subheader("Irisデータセットの統計データ")

    pr = create_profile(df)
    st_profile_report(pr)