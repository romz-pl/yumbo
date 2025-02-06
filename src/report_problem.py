import streamlit as st


def show_task():
    st.subheader(":green[Tasks]", divider="green")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}", 'Avg': "{:.4f}"}
    df = st.session_state.mprob["task"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_expert():
    st.subheader(":green[Experts]", divider="green")
    st.dataframe(st.session_state.mprob["expert"], hide_index=True, use_container_width=True)


def show_assign():
    st.subheader(":green[Assignment]", divider="green")
    st.dataframe(st.session_state.mprob["assign"], hide_index=True, use_container_width=True)


def show_xbday():
    st.subheader(":green[xbday]", divider="green")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}", 'Lower': "{:.2f}", 'Upper': "{:.2f}"}
    df = st.session_state.mprob["xbday"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_ubday():
    st.subheader(":green[ubday]", divider="green")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}", 'Lower': "{:.2f}", 'Upper': "{:.2f}"}
    df = st.session_state.mprob["ubday"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)



def show_ebday():
    st.subheader(":green[ebday]", divider="green")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}", 'Lower': "{:.2f}", 'Upper': "{:.2f}"}
    df = st.session_state.mprob["ebday"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_period():
    st.subheader(":green[Names and intervals]", divider="green")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}"}
    df = st.session_state.mprob["period"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_pbsum():
    st.subheader(":green[pbsum]", divider="green")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}", 'Lower': "{:.2f}", 'Upper': "{:.2f}"}
    df = st.session_state.mprob["pbsum"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)

def show_exptas():
    col0, col1, col2 = st.columns(3)
    with col0:
        show_task()
    with col1:
        show_expert()
    with col2:
        show_assign()


def customise_bounds():
    col0, col1, col2 = st.columns(3)
    with col0:
        show_xbday()
    with col1:
        show_ubday()
    with col2:
        show_ebday()


def customise_periods():
    col0, col1 = st.columns(2)
    with col0:
        show_period()
    with col1:
        show_pbsum()


def show():
    if not st.session_state.show["problem"]:
        return

    st.divider()

    st.header(":blue[Problem definition]", divider="blue")
    tab = st.tabs(["**Experts and Tasks**", "**Bounds**", "**Periods**"])

    with tab[0]:
        show_exptas()
    with tab[1]:
        customise_bounds()
    with tab[2]:
        customise_periods()
