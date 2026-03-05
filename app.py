import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("AI Business Analytics Platform")

st.write("Upload an Excel or CSV file to automatically generate KPIs, insights, and predictions.")

file = st.file_uploader("Upload Excel or CSV File", type=["xlsx","csv"])

if file is not None:

    # Read file
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    # Detect columns automatically
    numeric_cols = df.select_dtypes(include=['number']).columns
    text_cols = df.select_dtypes(include=['object']).columns

    st.header("Key Performance Indicators")

    for col in numeric_cols:
        total = df[col].sum()
        avg = df[col].mean()

        st.metric(f"Total {col}", round(total,2))
        st.metric(f"Average {col}", round(avg,2))

    if len(text_cols) > 0 and len(numeric_cols) > 0:

        category = text_cols[0]
        value = numeric_cols[0]

        summary = df.groupby(category)[value].sum()

        st.header("Insights")

        top = summary.idxmax()
        low = summary.idxmin()

        st.write(f"Top performing {category}: **{top}**")
        st.write(f"Lowest performing {category}: **{low}**")

        st.header("Prediction")

        prediction = df[value].mean()*1.1
        st.write(f"Predicted future {value}: **{round(prediction,2)}**")

        st.header("Visualization")

        fig, ax = plt.subplots()
        summary.plot(kind="bar", ax=ax)
        st.pyplot(fig)
