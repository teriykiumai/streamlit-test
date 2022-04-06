import tempfile
import streamlit as st

def uploaded2tempfile(uploaded_file):
    """uploaded2tempfile [summary]
    Args:
        uploaded_file ([type]): [description]
    Returns:
        temporary filepath [str]
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        # To convert to a string based
        fp = Path(tmp_file.name)
        fp.write_bytes(uploaded_file.getvalue())
    return tmp_file.name
