from matplotlib.pyplot import sca
import pandas as pd
import streamlit as st

import lib
from lib.music.diatonic import DiatonicChords


def chord_table(chord_item):
    st.subheader("ダイアトニック")
    degree_name = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ",]
    for scale, chord in chord_item.items():
        with st.expander(scale):
            df = pd.DataFrame(chord)
            df.index = degree_name
            st.table(df)

def role_table(role_item):
    st.subheader("コード役割")
    for scale, role in role_item.items():
        with st.expander(scale):
            df = pd.DataFrame(role.values()).T
            df = df.fillna("")
            df.columns = role.keys()
            st.table(df)

def composite_table(comp_item):
    st.subheader("構成音")
    def make_index(comp_len):
        if comp_len == 3:
            return ["root", "3rd", "5th"]
        elif comp_len == 4:
            return ["root", "3rd", "5th", "7th"]
  
    for scale, tonic in comp_item.items():
        with st.expander(scale):
            df = pd.DataFrame(tonic)
            df.index = make_index(len(df))
            st.table(df)


def app():
    lib.side_param()

    diatonic = DiatonicChords()
    with st.sidebar:
        key = st.selectbox("Key", diatonic.keys.select)
        scale = st.radio("Scale", diatonic.scales.select)
        chord = st.radio("和音", diatonic.select_chord_type)
        relative_show = st.checkbox("平行調を表示する")
    diatonic.update_chords(key, scale, chord)


    def show_scale():
        st.title("主調")
        scale_col = st.columns(3)

        with scale_col[0]:
            chord_table(diatonic.scale_chords)

        with scale_col[1]:
            role_table(diatonic.scale_roles)

        with scale_col[2]:
            composite_table(diatonic.scale_composites)


    def show_relative():
        st.title("平行調")
        rel_col = st.columns(3)
        with rel_col[0]:
            chord_table(diatonic.relative_chords)

        with rel_col[1]:
            role_table(diatonic.relative_roles)

        with rel_col[2]:
            composite_table(diatonic.relative_composites)

    show_scale()
    if relative_show:
        st.write("-"*3)
        show_relative()


