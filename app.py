import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("AI Business Analytics Platform")

st.write("Upload your Excel or CSV dataset to generate automatic KPIs, insights, and predictions.")

file = st.file_uploader("Upload Dataset", type=["xlsx","csv"])

if file is not None:

    # ---------- LOAD DATA ----------
    try:
        if file.name.endswith(".csv"):
            try:
                df = pd.read_csv(file, encoding="utf-8")
            except:
                df = pd.read_csv(file, encoding="latin1")
        else:
            df = pd.read_excel(file)
    except Exception as e:
        st.error("Error reading file. Please upload a valid dataset.")
        st.stop()

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # ---------- DETECT COLUMN TYPES ----------
    numeric_cols = df.select_dtypes(include=["number"]).columns
    text_cols = df.select_dtypes(include=["object"]).columns

    # ---------- KPI SECTION ----------
    st.header("Key Performance Indicators")

    if len(numeric_cols) > 0:
        cols = st.columns(min(4, len(numeric_cols)))

        for i, col in enumerate(numeric_cols):
            cols[i % 4].metric(
                label=f"Total {col}",
                value=round(df[col].sum(), 2)
            )
    else:
        st.write("No numeric columns found for KPI generation.")

    # ---------- INSIGHTS ----------
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
        plt.xticks(rotation=45)
        st.pyplot(fig)

    else:
        st.write("Not enough columns to generate insights.")

    # ---------- TREND ANALYSIS ----------
    st.header("Trend Analysis")

    date_col = None

    for col in df.columns:
        try:
            converted = pd.to_datetime(df[col])
            if converted.notna().sum() > len(df) * 0.5:
                df[col] = converted
                date_col = col
                break
        except:
            pass

    if date_col and len(numeric_cols) > 0:

        value = numeric_cols[0]

        df_sorted = df.sort_values(date_col)

        trend = df_sorted.groupby(date_col)[value].sum()

        fig2, ax2 = plt.subplots()
        trend.plot(ax=ax2)
        plt.xticks(rotation=45)

        st.pyplot(fig2)

    else:
        st.write("No valid date column detected for trend analysis.")

    # ---------- SIMPLE PREDICTION ----------
    st.header("Prediction")

    if len(numeric_cols) > 0:

        value = numeric_cols[0]

        prediction = df[value].mean() * 1.1

        st.write(f"Predicted next value for **{value}**: {round(prediction,2)}")

    else:
        st.write("Prediction unavailable (no numeric columns found).")
