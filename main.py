import streamlit as st
import pandas as pd


def dummy_cleanup(df: pd.DataFrame) -> pd.DataFrame:
    # Example cleanup: Drop rows with any null values
    return df.drop_duplicates(subset=["id"])


st.title("Talenta Data Cleanup")
st.write("cihuy")
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(df)

    if st.button("Clean Data"):
        cleaned_df = dummy_cleanup(df)
        st.write("Cleaned Data Preview:")
        st.dataframe(cleaned_df)

        # Provide a download link for the cleaned data
        cleaned_file = "cleaned_data.xlsx"
        cleaned_df.to_excel(cleaned_file, index=False)
        with open(cleaned_file, "rb") as file:
            btn = st.download_button(
                label="Download Cleaned Data",
                data=file,
                file_name=cleaned_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
