import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from datetime import datetime
import calendar
import database as db
incomes = ["Salary", "Blog", "Other Income"]
expenses = ["Rent", "Utilities", "Groceries", "Car", "Other Expenses", "Saving"]

currency = "INR"

page_title = "Income and Expense Tracker"
page_icon = ":money_with_wings:"

layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title+ " " + page_icon)

years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])

def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods

hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>

"""
st.markdown(hide_st_style, unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization"],
    icons = ["pencil-fill", "bar-chart-fill"],
    orientation= "horizontal"
)

if selected == "Data Entry":
    st.header(f"Data Entry in {currency}")
    with st.form("entry_form", clear_on_submit = True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select Month: ", months, key = "month")
        col2.selectbox("Select Year: ", years, key = "year")

        "---"
        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:", min_value = 0, format = "%i", step = 1000, key=income)
        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0, format="%i", step=1000, key=expense)
        with st.expander("Comment"):
            comment = st.text_area("", placeholder="Enter a comment here")
        
        
        "---"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses}
            db.insert_period(period, incomes, expenses, comment)
            # st.write(f"incomes: {incomes}")
            # st.write(f"expense: {expenses}")
            st.success("Data Saved")


if selected == "Data Visualization":
    st.header("Data Visualization")
    with st.form("saved_periods"):
        period = st.selectbox("Select Period:", get_all_periods())
        submitted = st.form_submit_button("Plot Period")

        if submitted:
            period_data = db.get_period(period)
            comment = period_data["comment"]
            incomes = period_data["incomes"]
            expenses = period_data["expenses"]

            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            remaining_budget = total_income - total_expense

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"{total_income} {currency}")
            col2.metric("Total Expense", f"{total_expense} {currency}")
            col3.metric("Remaining Budget", f"{remaining_budget} {currency}")

            st.text(f"Comment: {comment}")

            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses]
            value = list(incomes.values()) + list(expenses.values())


            link = dict(source = source, target = target, value = value)
            node = dict(label = label, pad=20, thickness=30, color="#f3f3f3")
            data = go.Sankey(link=link, node=node)
            
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0,r=0,t=5,b=5))
            st.plotly_chart(fig, use_container_width=True)