import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("AI Business Analytics Platform")

st.write("Upload your Excel or CSV dataset to generate automatic KPIs, insights, and predictions.")

file = st.file_uploader("Upload Dataset", type=["xlsx","csv"])

if file is not None:

    # Load data
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Detect column types
    numeric_cols = df.select_dtypes(include=['number']).columns
    text_cols = df.select_dtypes(include=['object']).columns
    date_cols = df.select_dtypes(include=['datetime']).columns

    st.header("Key Performance Indicators")

    for col in numeric_cols:
        st.metric(
            label=f"Total {col}",
            value=round(df[col].sum(),2)
        )

    st.header("Insights")

    if len(text_cols) > 0 and len(numeric_cols) > 0:

        category = text_cols[0]
        value = numeric_cols[0]

        summary = df.groupby(category)[value].sum()

        top = summary.idxmax()
        low = summary.idxmin()

        st.write(f"Top performing **{category}**: {top}")
        st.write(f"Lowest performing **{category}**: {low}")

        # Chart
        fig, ax = plt.subplots()
        summary.plot(kind="bar", ax=ax)
        st.pyplot(fig)

    st.header("Trend Analysis")

    # Detect date column automatically
    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col])
            date_col = col
            break
        except:
            continue

    if 'date_col' in locals():

        df_sorted = df.sort_values(date_col)

        if len(numeric_cols) > 0:

            value = numeric_cols[0]

            trend = df_sorted.groupby(date_col)[value].sum()

            fig2, ax2 = plt.subplots()
            trend.plot(ax=ax2)

            st.pyplot(fig2)

    st.header("Prediction")

    if len(numeric_cols) > 0:

        value = numeric_cols[0]

        prediction = df[value].mean() * 1.1

        st.write(f"Predicted next value for **{value}**: {round(prediction,2)}")
