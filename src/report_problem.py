import streamlit as st


def show_task():
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}", 'Avg': "{:.4f}"}
    df = st.session_state.mprob["task"]
    df_styled = df.style.format(format)
    st.subheader(f":green[Tasks ({df.shape[0]})]", divider="green")
    st.dataframe(df_styled, hide_index=True, use_container_width=True)


def show_expert():
    df = st.session_state.mprob["expert"]
    st.subheader(f":green[Experts ({df.shape[0]})]", divider="green")
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_assign():
    df = st.session_state.mprob["assign"]
    st.subheader(f":green[Assignment ({df.shape[0]})]", divider="green")
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_xbday():
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}", 'Lower': "{:.2f}", 'Upper': "{:.2f}"}
    df = st.session_state.mprob["xbday"]
    df_styled = df.style.format(format)
    st.subheader(f":green[xbday ({df.shape[0]})]", divider="green")
    st.dataframe(df_styled, hide_index=True, use_container_width=True)


def show_ubday():
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}", 'Lower': "{:.2f}", 'Upper': "{:.2f}"}
    df = st.session_state.mprob["ubday"]
    df_styled = df.style.format(format)
    st.subheader(f":green[ubday ({df.shape[0]})]", divider="green")
    st.dataframe(df_styled, hide_index=True, use_container_width=True)



def show_ebday():
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}", 'Lower': "{:.2f}", 'Upper': "{:.2f}"}
    df = st.session_state.mprob["ebday"]
    df_styled = df.style.format(format)
    st.subheader(f":green[ebday ({df.shape[0]})]", divider="green")
    st.dataframe(df_styled, hide_index=True, use_container_width=True)


def show_period():
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}"}
    df = st.session_state.mprob["period"]
    df_styled = df.style.format(format)
    st.subheader(f":green[Periods ({df.shape[0]})]", divider="green")
    st.dataframe(df_styled, hide_index=True, use_container_width=True)


def show_pbsum():
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}", 'Lower': "{:.2f}", 'Upper': "{:.2f}"}
    df = st.session_state.mprob["pbsum"]
    df_styled = df.style.format(format)
    st.subheader(f":green[pbsum ({df.shape[0]})]", divider="green")
    st.dataframe(df_styled, hide_index=True, use_container_width=True)

def show_exptas():
    col0, col1, col2 = st.columns(3)
    with col0:
        show_expert()
    with col1:
        show_task()
    with col2:
        show_assign()


def show_bounds():
    col0, col1, col2 = st.columns(3)
    with col0:
        show_xbday()
    with col1:
        show_ubday()
    with col2:
        show_ebday()


def show_periods():
    col0, col1 = st.columns(2)
    with col0:
        show_period()
    with col1:
        show_pbsum()


def show():
    if not st.session_state.show["problem"]:
        return

    st.divider()

    st.header(":material/database: :blue[Problem definition]", divider="blue")

    options = ["Experts / Tasks", "Bounds", "Periods"]

    selection = st.pills(
        "Select problem area",
        options,
        selection_mode="single",
        default=options[0],
        label_visibility="collapsed"
    )

    if selection == options[0]:
        show_exptas()
    elif selection == options[1]:
        show_bounds()
    elif selection == options[2]:
        show_periods()
