import streamlit as st
import pandas as pd
import io
from utils.cleanup import remove_clock_type_dupe


def check_file(df: pd.DataFrame) -> bool:
    required_columns = {"Type", "Job Position", "Date"}
    return required_columns.issubset(df.columns)


# Define functions for each operation
def clock_in_out_duplicate_removal(df: pd.DataFrame) -> pd.DataFrame:
    # st.write("Running Clock In/Out Duplicate Removal...")
    return remove_clock_type_dupe(df)


def add_sunday(df: pd.DataFrame) -> pd.DataFrame:
    st.warning("Will be implemented soon...")
    return df


def add_missing_clock_in_out(df: pd.DataFrame) -> pd.DataFrame:
    st.warning("Will be implemented soon...")
    return df


def download_data_prep(df: pd.DataFrame) -> io.BytesIO:
    buffer = io.BytesIO()
    df.assign(Date=lambda x: x["Date"].dt.strftime("%Y-%m-%d")).to_excel(
        buffer, index=False, engine="openpyxl"
    )
    buffer.seek(0)
    return buffer


SHEET_NAME = "Raw Data"


# Main page function
def main_page():
    st.title("Talenta Data Cleanup")
    st.write("Still Testing Phase")
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

    # Initialize session state for the DataFrame
    if "df" not in st.session_state:
        st.session_state.df = None

    # Define a mapping of operation names to functions
    operation_mapping = {
        "Clock In/Out Duplicate Removal": clock_in_out_duplicate_removal,
        "Add Sunday": add_sunday,
        "Add Missing Clock In/Out": add_missing_clock_in_out,
    }

    will_be_implemented = ["Add Sunday", "Add Missing Clock In/Out"]

    if "download_buffer" not in st.session_state:
        st.session_state.download_buffer = None

    if uploaded_file:
        if not uploaded_file.name.endswith(".xlsx"):
            st.error("Please upload a valid .xlsx file.")
            return
        try:
            # Load the uploaded file into a DataFrame
            st.session_state.df = pd.read_excel(
                uploaded_file, sheet_name=SHEET_NAME, parse_dates=["Date"]
            ).assign(
                unique_key=lambda x: x["Employee ID"].astype(str)
                + "_"
                + x["Date"].dt.strftime("%Y-%m-%d")
                + "_"
                + x["Type"]
            )
        except ValueError:
            st.error(f"The uploaded file does not contain a '{SHEET_NAME}' sheet.")
            st.session_state.df = None
            return

        st.write("Data Preview:")
        st.write(f"Total Rows: {len(st.session_state.df)} data")
        st.dataframe(st.session_state.df.head(20))

        # Display checkboxes for operations
        st.write("### Select Operations to Apply")
        selected_operations = []
        for operation_name in operation_mapping.keys():
            if operation_name in will_be_implemented:
                st.checkbox(
                    f"{operation_name} (Will be implemented soon)",
                    value=False,
                    disabled=True,
                )
            else:
                if st.checkbox(operation_name, value=False):
                    selected_operations.append(operation_name)

        # Execute the selected operations
        if st.button("Execute Selected Operations"):
            with st.spinner("Processing..."):
                df = st.session_state.df
                for operation_name in selected_operations:
                    operation_func = operation_mapping[operation_name]
                    df = operation_func(df)
                st.session_state.df = df

            # Display the final DataFrame
            st.write("Processed Data Preview:")
            st.write(f"Total Final Rows: {len(st.session_state.df)} data")
            st.dataframe(st.session_state.df.head(20))

            # Provide a download link for the processed data
            with st.spinner("Preparing download..."):
                buffer = download_data_prep(st.session_state.df)
                st.download_button(
                    label="Download Processed Data",
                    data=buffer,
                    file_name="processed_talenta_attendance_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )


if __name__ == "__main__":
    main_page()
