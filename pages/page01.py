import streamlit as st
import pandas as pd 
# from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import plotly.graph_objects as go

@st.cache(allow_output_mutation=True)
def _read_csv(read_csv):
    df = pd.read_csv(read_csv)
    return df

def donwload_df(df):
    csv = df.to_csv().encode('utf-8')
    output_name = st.text_input("保存名")
    st.download_button(
        "Press to Download",
        csv,
        f"{output_name}.csv",
        "text/csv",
        key='download-csv',
        disabled=not bool(output_name),
    )

def app():
    st.header("CSV Reader")
    uploaded_file = st.file_uploader("Please Upload CSV Data ", type='csv')

    if uploaded_file:
        df = _read_csv(uploaded_file)

        with st.sidebar:
            st.title("⚙️ Parameters")
            with st.expander("データ編集"):
                st.checkbox("転置Df.T")
                # また今度書く

            with st.expander("軸設定"):
                x = st.selectbox("X Axis", df.columns)
                # y = st.multiselect("Y Axis", df.columns.drop(x))
                y = st.selectbox("Y Axis", df.columns.drop(x))

            with st.expander("CSV書き出し"):
                donwload_df(df)
                

        # グラフの詳細決定
        data = go.Line(x=df[x], y=df[y])
        go_fig = go.Figure(data)
        # https://plotly.com/python/reference/layout/#layout-paper_bgcolor
        go_fig.update_layout(hovermode='closest', 
                                dragmode='pan', 
                                modebar={'orientation':'v'}, 
                                margin=dict(l=30, r=30, t=5, b=25), 
                            )
        st.plotly_chart(go_fig, use_container_width=True)

        with st.expander("show DataFrame"):
            # st.dataframe(df)
            st.table(df)


