import imggsum
import imghsum
import imgtsum
import streamlit as st


def show():
    if not st.session_state.glb["show_experts_overview"]:
        return

    st.divider()

    st.header(":blue[Experts overview]", divider="blue")
    col1, col2, col3 = st.columns(3)
    with col1:
        imggsum.plot()
    with col2:
        imgtsum.plot()
    with col3:
        imghsum.plot()

