import streamlit as st

# import model
from . import model


def app():
    a = model.DiatonicChords()

    with st.sidebar:
        key = st.selectbox("Key", a.keys.select)
        scale = st.radio("Scale", a.scales.select)
        chord = st.radio("和音", a.select_chord_type)

        relative_show = st.checkbox("平行調を表示する")

    a.update_chords(key, scale, chord)

    st.header("主調")
    st.table(a.scale_chords)

    st.write("-"*5)
    st.subheader("tonic")
    # st.info("一 ".join(a.scale_roles["Major"]["tonic"]))
    st.write(a.scale_composites)


    if relative_show:
        st.write("-"*5)
        st.header("平行調")
        st.table(a.relative_chords)

# app()

