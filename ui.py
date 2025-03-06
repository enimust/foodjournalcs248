# ui.py
import streamlit as st
import altair as alt
import pandas as pd
from datetime import date
import base64


def render_new_entry_ui(conn):
    """Render the New Entry form with database insertion."""
    from datetime import datetime
    from database import add_entry

    # Define vegetarian dishes with calorie information.
    dishes = {
        "Breakfast": [
            {"name": "Avocado Toast", "calories": 250},
            {"name": "Vegan Pancakes", "calories": 300},
            {"name": "Oatmeal", "calories": 200},
            {"name": "Fruit Salad", "calories": 150},
            {"name": "Smoothie Bowl", "calories": 350}
        ],
        "Lunch": [
            {"name": "Grilled Vegetable Sandwich", "calories": 400},
            {"name": "Veggie Wrap", "calories": 350},
            {"name": "Quinoa Salad", "calories": 450},
            {"name": "Caprese Salad", "calories": 300},
            {"name": "Lentil Soup", "calories": 250}
        ],
        "Dinner": [
            {"name": "Vegetable Stir Fry", "calories": 500},
            {"name": "Veggie Pasta", "calories": 550},
            {"name": "Tofu Curry", "calories": 600},
            {"name": "Vegetable Lasagna", "calories": 650},
            {"name": "Mushroom Risotto", "calories": 400}
        ]
    }

    mood_options = [
        "😊 Happy",
        "😐 Neutral",
        "😞 Sad",
        "😡 Angry",
        "😌 Relaxed"
    ]

    st.header("Add a New Entry")
    entry_date = st.date_input("Select the date", value=date.today())
    meal = st.selectbox("Select Meal Time", list(dishes.keys()))
    meal_dishes = dishes[meal]
    dish_choice_index = st.selectbox(
        "Select a Dish",
        range(len(meal_dishes)),
        format_func=lambda i: f"{meal_dishes[i]['name']} ({meal_dishes[i]['calories']} calories)"
    )
    selected_dish = meal_dishes[dish_choice_index]
    mood = st.selectbox("How are you feeling?", mood_options)
    notes = st.text_area("Additional Notes")
    if st.button("Add Entry"):
        formatted_date = entry_date.strftime('%Y-%m-%d')
        entry = (formatted_date, meal, selected_dish['name'], selected_dish['calories'], mood, notes)
        add_entry(conn, entry)
        st.success("Entry added successfully!")

def render_journal_ui(conn):
    """Render the Food Journal view.
       Initially shows nothing until the user clicks 'Show Journal'.
    """
    st.header("Food Journal")
    view_option = st.radio("View Options", ["Range of dates", "Show all entries"], index=0)
    
    # If the user selects a range, show the date inputs immediately.
    if view_option == "Range of dates":
        start_date = st.date_input("Start Date", key="journal_start")
        end_date = st.date_input("End Date", key="journal_end")
    
    if st.button("Show Journal"):
        if view_option == "Range of dates":
            from database import get_entries_by_date_range
            rows = get_entries_by_date_range(conn,
                        start_date.strftime('%Y-%m-%d'),
                        end_date.strftime('%Y-%m-%d'))
        else:
            from database import get_all_entries
            rows = get_all_entries(conn)
        if rows:
            df = pd.DataFrame(rows, columns=["Date", "Meal", "Food", "Calories", "Mood", "Notes"])
            st.markdown(df.to_html(index=False), unsafe_allow_html=True)
        else:
            st.info("No entries found.")


def render_graphs_ui(conn):
    st.header("Calorie Graphs")
    st.write("Select a time period to view your daily calorie consumption.")
    start_date = st.date_input("Start Date", key="graph_start")
    end_date = st.date_input("End Date", key="graph_end")
    if st.button("Show Graph"):
        from database import get_calories_by_meal
        data = get_calories_by_meal(conn,
                    start_date.strftime('%Y-%m-%d'),
                    end_date.strftime('%Y-%m-%d'))
        if data:
            df = pd.DataFrame(data, columns=["Date", "Meal", "Calories"])
            # Convert to datetime
            df["Date"] = pd.to_datetime(df["Date"])
            # Sort the DataFrame by date
            df = df.sort_values("Date")
            
            # Create a numeric key for sorting
            df["SortKey"] = df["Date"].view("int64")
            
            # Create a label for display, e.g. 03/06/25
            df["DateLabel"] = df["Date"].dt.strftime('%m/%d/%y')
            
            # Build a stacked bar chart
            import altair as alt
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(
                    "DateLabel:N",
                    title="Date",
                    # Sort by the numeric SortKey
                    sort=alt.SortField(field="SortKey", order="ascending")
                ),
                y=alt.Y("Calories:Q", stack="zero", title="Calories"),
                color=alt.Color("Meal:N", title="Meal"),
                tooltip=[alt.Tooltip("Date:T", title="Date"), "Meal:N", "Calories:Q"]
            ).properties(width=600, height=400)
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No data found for the selected period.")



