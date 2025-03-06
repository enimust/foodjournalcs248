# app.py
import streamlit as st
from database import get_connection, initialize_db
import ui

conn = get_connection()
initialize_db(conn)


def main():

    # 1. Container for the local banner image
    with st.container():
        st.image("images/banner.jpg", use_container_width=True)

    # 2. Title container:
    st.markdown(
        "<h1 style='text-align:center;'>🍽️ Food journaling made easy 🍴</h1>",
        unsafe_allow_html=True
    )

    # 3. Container for the tabs
    tab1, tab2, tab3 = st.tabs(["New Entry 🍽️", "Journal 📓", "Graphs 📊"])

    # Fill in each tab with your custom UI/logic
    with tab1:
        ui.render_new_entry_ui(conn)

    with tab2:
        ui.render_journal_ui(conn)

    with tab3:
        ui.render_graphs_ui(conn)

if __name__ == "__main__":
    main()



