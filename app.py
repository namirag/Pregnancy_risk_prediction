import streamlit as st
import numpy as np
from streamlit_option_menu import option_menu
import pickle
import warnings
import pandas as pd
import plotly.express as px
from io import StringIO
import requests

from codebase.dashboard_graphs import MaternalHealthDashboard

scale_mp = pickle.load(open(".\model\scaler.sav", "rb"))
maternal_model = pickle.load(open(".\model\_finalized_maternal_model_gbc.sav", "rb"))
maternal_model_rf = pickle.load(open(".\model\_finalized_maternal_model.sav", "rb"))
scale_fetus = pickle.load(open(".\model\scaler_fetus.sav", "rb"))
fetus_model = pickle.load(open(".\model\optimized_fetal_health_model.sav", "rb"))


# sidebar for navigation
with st.sidebar:
    st.title("MedPredict")
    st.write("Welcome to the MedPredict")
    st.write(" Choose an option from the menu below to get started:")

    selected = option_menu(
        "MedPredict",
        [
            "About us",
            "Pregnancy Risk Prediction",
            "Fetal Health Prediction",
            "Dashboard",
        ],
        icons=["chat-square-text", "hospital", "capsule-pill", "clipboard-data"],
        default_index=0,
    )

if selected == "About us":

    st.title("Welcome to MedPredict")
    st.write(
        "At MedPredict, our mission is to revolutionize healthcare by offering innovative solutions through predictive analysis. "
        "Our platform is specifically designed to address the intricate aspects of maternal and fetal health, providing accurate "
        "predictions and proactive risk management."
    )

    col1, col2 = st.columns(2)
    with col1:
        # Section 1: Pregnancy Risk Prediction
        st.header("Pregnancy Risk Prediction")
        st.write(
            "Our Pregnancy Risk Prediction feature utilizes advanced algorithms to analyze various parameters, including age, "
            "body sugar levels, blood pressure, and more. By processing this information, we provide accurate predictions of "
            "potential risks during pregnancy."
        )
        # Add an image for Pregnancy Risk Prediction
        st.image(
            "graphics\Preg_risk.jpeg",
            caption="Pregnancy Risk Prediction",
            use_container_width=True,
        )
    with col2:
        # Section 2: Fetal Health Prediction
        st.header("Fetal Health Prediction")
        st.write(
            "Fetal Health Prediction is a crucial aspect of our system. We leverage cutting-edge technology to assess the "
            "health status of the fetus. Through a comprehensive analysis of factors such as ultrasound data, maternal health, "
            "and genetic factors, we deliver insights into the well-being of the unborn child."
        )
        # Add an image for Fetal Health Prediction
        st.image(
            "graphics\_fetus_img.jpg",
            caption="Fetal Health Prediction",
            use_container_width=True,
        )

    # Section 3: Dashboard
    st.header("3. Dashboard")
    st.write(
        "Our Dashboard provides a user-friendly interface for monitoring and managing health data. It offers a holistic "
        "view of predictive analyses, allowing healthcare professionals and users to make informed decisions. The Dashboard "
        "is designed for ease of use and accessibility."
    )

    # Closing note
    st.write(
        "Thank you for choosing E-Doctor. We are committed to advancing healthcare through technology and predictive analytics. "
        "Feel free to explore our features and take advantage of the insights we provide."
    )

if selected == "Pregnancy Risk Prediction":

    # page title
    st.title("Pregnancy Risk Prediction")
    content = "Predicting the risk in pregnancy involves analyzing several parameters, including age, blood sugar levels, blood pressure, and other relevant factors. By evaluating these parameters, we can assess potential risks and make informed predictions regarding the pregnancy's health"
    st.markdown(
        f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>",
        unsafe_allow_html=True,
    )

    # getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input("Age of the Person", key="age")

    with col2:
        diastolicBP = st.text_input("diastolicBP in mmHg")

    with col3:
        BS = st.text_input("Blood glucose in mmol/L")

    with col1:
        bodyTemp = st.text_input("Body Temperature in Celsius")

    with col2:
        heartRate = st.text_input("Heart rate in beats per minute")

    riskLevel = ""
    predicted_risk = [0]
    # creating a button for Prediction
    with col1:
        if st.button("Predict Pregnancy Risk"):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                # scaling is important.
                scaled_input = scale_mp.transform(
                    [[age, diastolicBP, BS, bodyTemp, heartRate]]
                )
                predicted_risk_mp = maternal_model_rf.predict(scaled_input)
            # st
            st.subheader("Risk Level:")
            if predicted_risk_mp[0] == 0:
                st.markdown(
                    '<bold><p style="font-weight: bold; font-size: 20px; color: green;">Low Risk</p></bold>',
                    unsafe_allow_html=True,
                )
            elif predicted_risk_mp[0] == 1:
                st.markdown(
                    '<bold><p style="font-weight: bold; font-size: 20px; color: orange;">Medium Risk</p></Bold>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<bold><p style="font-weight: bold; font-size: 20px; color: red;">High Risk</p><bold>',
                    unsafe_allow_html=True,
                )
    with col2:
        if st.button("Clear"):
            st.rerun()

if selected == "Fetal Health Prediction":

    # page title
    st.title("Fetal Health Prediction")

    content = "Cardiotocograms (CTGs) are a simple and cost accessible option to assess fetal health, allowing healthcare professionals to take action in order to prevent child and maternal mortality"
    st.markdown(
        f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>",
        unsafe_allow_html=True,
    )

    BaselineValue = st.slider("Baseline Value", min_value=50.0, max_value=200.0)
    Accelerations = st.slider("Accelerations", min_value=0.0, max_value=10.0)
    fetal_movement = st.slider("Fetal Movement", min_value=0.0, max_value=10.0)
    uterine_contractions = st.slider(
        "Uterine Contractions", min_value=0.0, max_value=10.0
    )
    light_decelerations = st.slider(
        "Light Decelerations", min_value=0.0, max_value=10.0
    )
    severe_decelerations = st.slider(
        "Severe Decelerations", min_value=0.0, max_value=10.0
    )
    prolongued_decelerations = st.slider(
        "Prolongued Decelerations", min_value=0.0, max_value=10.0
    )
    abnormal_short_term_variability = st.slider(
        "Abnormal Short Term Variability", min_value=0.0, max_value=100.0
    )
    mean_value_of_short_term_variability = st.slider(
        "Mean Value Of Short Term Variability",
        min_value=0.0,
        max_value=100.0,
        value=0.5,
    )
    percentage_of_time_with_abnormal_long_term_variability = st.slider(
        "Percentage of Time with Abnormal Long Term Variability",
        min_value=0.0,
        max_value=100.0,
        value=43.0,
    )
    mean_value_of_long_term_variability = st.slider(
        "Mean Value of Long Term Variability",
        min_value=0.0,
        max_value=100.0,
        value=64.0,
    )
    histogram_width = st.slider(
        "Histogram Width", min_value=0.0, max_value=100.0, value=62.0
    )
    histogram_min = st.slider(
        "Histogram Min", min_value=0.0, max_value=200.0, value=62.0
    )
    histogram_max = st.slider(
        "Histogram Max", min_value=0.0, max_value=200.0, value=126.0
    )
    histogram_number_of_peaks = st.slider(
        "Histogram Number of Peaks", min_value=0.0, max_value=10.0, value=2.0
    )
    histogram_number_of_zeroes = st.slider(
        "Histogram Number of Zeroes", min_value=0.0, max_value=10.0, value=0.0
    )
    histogram_mode = st.slider(
        "Histogram Mode", min_value=0.0, max_value=200.0, value=120.0
    )
    histogram_mean = st.slider(
        "Histogram Mean", min_value=0.0, max_value=200.0, value=137.0
    )
    histogram_median = st.slider(
        "Histogram Median", min_value=0.0, max_value=200.0, value=121.0
    )
    histogram_variance = st.slider(
        "Histogram Variance", min_value=0.0, max_value=100.0, value=73.0
    )
    histogram_tendency = st.slider(
        "Histogram Tendency", min_value=0.0, max_value=10.0, value=1.0
    )

    # Prepare the input data
    input_data = [
        [
            BaselineValue,
            Accelerations,
            fetal_movement,
            uterine_contractions,
            light_decelerations,
            severe_decelerations,
            prolongued_decelerations,
            abnormal_short_term_variability,
            mean_value_of_short_term_variability,
            percentage_of_time_with_abnormal_long_term_variability,
            mean_value_of_long_term_variability,
            histogram_width,
            histogram_min,
            histogram_max,
            histogram_number_of_peaks,
            histogram_number_of_zeroes,
            histogram_mode,
            histogram_mean,
            histogram_median,
            histogram_variance,
            histogram_tendency,
        ]
    ]
    # creating a button for Prediction
    st.markdown("</br>", unsafe_allow_html=True)
    # getting the input data from the user
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Predict fetus Risk"):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                scale_fetus_input = scale_fetus.transform(input_data)
                predicted_risk = fetus_model.predict(scale_fetus_input)
                # st.subheader("Risk Level:")
                risk_class = predicted_risk[0]

            # Map prediction to risk level
            risk_mapping = {
                1.0: "Healthy (Low Risk)",
                2.0: "Medium Risk",
                3.0: "High Risk",
            }
            risk_category = risk_mapping.get(risk_class, "Unknown")

            # st.write(f"Predicted Risk Category: {risk_category}")
            st.markdown("</br>", unsafe_allow_html=True)
            if predicted_risk[0] == 0:
                st.markdown(
                    '<bold><p style="font-weight: bold; font-size: 20px; color: green;">Result  Comes to be  Normal</p></bold>',
                    unsafe_allow_html=True,
                )
            elif predicted_risk[0] == 1:
                st.markdown(
                    '<bold><p style="font-weight: bold; font-size: 20px; color: orange;">Result  Comes to be  Suspect</p></Bold>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<bold><p style="font-weight: bold; font-size: 20px; color: red;">Result  Comes to be  Pathological</p><bold>',
                    unsafe_allow_html=True,
                )
    with col2:
        if st.button("Clear"):
            st.rerun()

if selected == "Dashboard":
    api_key = "579b464db66ec23bdd00000139b0d95a6ee4441c5f37eeae13f3a0b2"
    api_endpoint = api_endpoint = (
        f"https://api.data.gov.in/resource/6d6a373a-4529-43e0-9cff-f39aa8aa5957?api-key={api_key}&format=csv"
    )
    st.header("Dashboard")
    content = "Our interactive dashboard offers a comprehensive visual representation of maternal health achievements across diverse regions. The featured chart provides insights into the performance of each region concerning institutional deliveries compared to their assessed needs. It serves as a dynamic tool for assessing healthcare effectiveness, allowing users to quickly gauge the success of maternal health initiatives."
    st.markdown(
        f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>",
        unsafe_allow_html=True,
    )

    dashboard = MaternalHealthDashboard(api_endpoint)
    dashboard.create_bubble_chart()
    with st.expander("Show More"):
        # Display a portion of the data
        content = dashboard.get_bubble_chart_data()
        st.markdown(
            f"<div style='white-space: pre-wrap;'><b>{content}</b></div>",
            unsafe_allow_html=True,
        )

    dashboard.create_pie_chart()
    with st.expander("Show More"):
        # Display a portion of the data
        content = dashboard.get_pie_graph_data()
        st.markdown(
            f"<div style='white-space: pre-wrap;'><b>{content}</b></div>",
            unsafe_allow_html=True,
        )
