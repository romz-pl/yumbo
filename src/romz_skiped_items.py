import streamlit as st


def show_skiped_df_items(gdata, key, format = None):
    st.subheader(f"{key}")
    df = gdata[f"skiped:{key}"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)



def show(gdata):
    if not gdata["show_skiped_items"]:
        return

    st.subheader(":green[Skiped items]", divider="blue")
    st.caption("When importing the items from the Excel file, some of the items have been skipped.")

    col1, col2, col3 = st.columns(3)
    with col1:
        format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}", 'Avg': "{:.2f}"}
        show_skiped_df_items(gdata, "tasks", format)
    with col2:
        show_skiped_df_items(gdata, "experts")
    with col3:
        show_skiped_df_items(gdata, "links")


    col1, col2, col3, col4 = st.columns(4)
    with col1:
        format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
        show_skiped_df_items(gdata, "xbday", format)
    with col2:
        format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
        show_skiped_df_items(gdata, "xbsum", format)
    with col3:
        format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
        show_skiped_df_items(gdata, "ubday", format)
    with col4:
        format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
        show_skiped_df_items(gdata, "ubsum", format)


    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
        show_skiped_df_items(gdata, "expert bounds", format)
    with col2:
        format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
        show_skiped_df_items(gdata, "invoicing periods", format)
    with col3:
        format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
        show_skiped_df_items(gdata, "invoicing periods bounds", format)
    with col4:
        format = {'Date': "{:%Y-%m-%d}"}
        show_skiped_df_items(gdata, "public holidays", format)
    with col5:
        show_skiped_df_items(gdata, "misc")
