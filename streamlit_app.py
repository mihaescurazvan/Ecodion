import streamlit as st
import pandas as pd
import plost
import time
import json
from main_logic import match_and_enrich
from langchain_try import generative_insights

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# st.sidebar.header('Ecodion')
locations = []

st.sidebar.subheader("Company name")
company_name = st.sidebar.text_input(
    "Enter Text", "", key="company_name", label_visibility="collapsed"
)

st.sidebar.subheader("Company website")
company_website = st.sidebar.text_input(
    "Enter Text", "", key="company_website", label_visibility="collapsed"
)

    
if 'result_chatbot' not in st.session_state:
    st.session_state.result_chatbot = ""
    
if 'metadata' not in st.session_state:
    st.session_state.metadata = None

button_pressed = st.sidebar.button("Search")

if button_pressed:
    st.session_state.show_select = True

    if company_name != "" and company_website != "":
        flag = True
        loading_text = st.empty()
        loading_text.write("Loading...")
        with st.spinner("Processing..."):
            st.session_state.metadata = match_and_enrich(company_name, company_website)
            st.session_state.result_chatbot = generative_insights(st.session_state.metadata)

        loading_text.empty()

if st.session_state.get("show_select", False):
    for location in st.session_state.metadata["locations"]:
        if location["city"]:
            locations.append(location["city"])

    default_option = st.session_state.get("location_selector", locations[0])
    location_selector = st.sidebar.selectbox(
        "Select location", locations, index=locations.index(default_option)
    )
    st.session_state.selected_option = location_selector

    st.markdown(f"### {company_name}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Base Location", st.session_state.metadata["main_country"], "")
    col2.metric("Credit Score", st.session_state.metadata["credit_score"], "*Scale 0 to 100, 100 is best.")
    col3.metric("Avarage Air Quality Index", st.session_state.metadata["average_aqi"], "")

    st.markdown(
        """
        ---
        """
    )

    for location in st.session_state.metadata["locations"]:
        if location["city"] == location_selector:
            st.markdown("### Location Indexes and Pollution Data")
            col1, col2, col3 = st.columns(3)
            col1.metric("Air Quality Index", location["aqi"], "")
            col2.metric("Level of AIQ", location["air_category"].split()[0], "")
            col3.metric("Seismic Risk", location["seismic"][0], "")

            col1, col2, col3 = st.columns(3)
            col4, col5, col6 = st.columns(3)
            col1.metric(
                location["pollutants"][0]["name"],
                location["pollutants"][0]["concentration"]["value"],
                location["pollutants"][0]["concentration"]["units"],
            )
            col2.metric(
                location["pollutants"][1]["name"],
                location["pollutants"][1]["concentration"]["value"],
                location["pollutants"][1]["concentration"]["units"],
            )
            col3.metric(
                location["pollutants"][2]["name"],
                location["pollutants"][2]["concentration"]["value"],
                location["pollutants"][2]["concentration"]["units"],
            )
            col4.metric(
                location["pollutants"][3]["name"],
                location["pollutants"][3]["concentration"]["value"],
                location["pollutants"][3]["concentration"]["units"],
            )
            col5.metric(
                location["pollutants"][4]["name"],
                location["pollutants"][4]["concentration"]["value"],
                location["pollutants"][4]["concentration"]["units"],
            )
            col6.metric(
                location["pollutants"][5]["name"],
                location["pollutants"][5]["concentration"]["value"],
                location["pollutants"][5]["concentration"]["units"],
            )

    st.markdown(
        """
        ---
        """
    )

    st.markdown("### 🤖​ Ecodion Assistant")
    st.write(
        f'<div class="column-card">{st.session_state.result_chatbot}</div>',
        unsafe_allow_html=True,
    )

st.sidebar.markdown(
    """
---
Powered by Veridion.
"""
)
