from matplotlib.pyplot import sca
import streamlit as st

# import model
import lib
from lib.music.diatonic import DiatonicChords


def app():
    lib.side_param()
    
    diatonic = DiatonicChords()

    with st.sidebar:
        key = st.selectbox("Key", diatonic.keys.select)
        scale = st.radio("Scale", diatonic.scales.select)
        chord = st.radio("和音", diatonic.select_chord_type)

        relative_show = st.checkbox("平行調を表示する")

    diatonic.update_chords(key, scale, chord)

    st.header("主調")
    st.table(diatonic.scale_chords)

    st.write("-"*5)
    st.subheader("構成音")
    for scale, tonic in diatonic.scale_composites.items():
        with st.expander(scale):
            st.table(tonic)


    if relative_show:
        st.write("-"*5)
        st.header("平行調")
        st.table(diatonic.relative_chords)

# app()

