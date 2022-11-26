import streamlit as st
import numpy as np
import pandas as pd
import plotly.figure_factory as ff

from VizApp import *
from q_a import *

st.set_page_config(layout="wide")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Overview",
        "Data viz with recommendation system",
        "Q&A with KG",
        "Prediction of world trade using KG",
    ]
)
with tab1:
    st.header("Overview")

with tab2:
    st.header("Data viz with recommendation system")

    country_dict = (
        pd.read_csv("../data/country_codes.csv").set_index("name").T.to_dict("list")
    )
    df_trades = pd.read_csv("../data/trades_v3.csv")

    with st.form("my_form"):

        counter_country = st.selectbox(
            "Counter Country", [x.upper() for x in list(country_dict.keys())]
        )
        country_name = counter_country

        start_year, end_year = st.select_slider(
            "Select Year", options=[i for i in range(2010, 2021, 1)], value=(2010, 2018)
        )

        product_selected = st.selectbox("Product", df_trades["section_name"])

        submitted = st.form_submit_button("Submit")
        if submitted:
            counter_country = country_dict[counter_country.lower()][0].lower()
            start_year = start_year
            end_year = end_year
            product_selected = product_selected
            # st.write(counter_country, start_year, end_year, product_selected)
            run_visualization(
                country_name, counter_country, start_year, end_year, product_selected
            )


with tab3:
    st.header("Q&A with the world trade KG")
    st.write("Methodology to answer the questions")
    st.markdown("**Template Questions:**")
    st.warning(
        """\n
        What was the GDP of United States in 2018?\n
        What products did US export from China by 1st jan 2020?\n
        What does Machine contain?\n
        From whom did U.S export in 2020?\n
        With whom does U.S has FTA with?\n
        How much metals did USA export from China in 1st Jan 2010?\n
    """
    )

    with st.form("q_a_form"):

        question = st.text_input(
            "Enter the question", "With whom does U.S has FTA with?"
        )
        submitted_3 = st.form_submit_button("Submit")

        if submitted_3:
            updated_ques, context, ans = q_a_main(question)
            st.info("**Original question:** " + question + ":confetti_ball:")
            st.info("**Updated question:** " + updated_ques + ":confetti_ball:")
            st.info(
                "**Context generated to answer the question:** "
                + context[:1000]
                + ":confetti_ball:"
            )
            st.success("**Answer with scores:** ")
            st.write(ans)
with tab4:
    st.header("Prediction of world trade using KG")