import pandas as pd


def remove_clock_type_dupe(df: pd.DataFrame) -> pd.DataFrame:
    def mark_duplicates(
        df: pd.DataFrame,
        type_filter: str,
        position_filter=None,
        subset_key="unique_key",
        keep="first",
    ):
        """
        Marks duplicates conditionally based on type and position filters.

        Args:
            df (pd.DataFrame): The DataFrame to process.
            type_filter (str): The value of the 'Type' column to filter (e.g., 'Clock In').
            position_filter (str, optional): The value of the 'Job Position' column to exclude from duplication checks.
            subset_key (str): The column to use for duplication checks.
            keep (str): Whether to keep 'first' or 'last' duplicate.

        Returns:
            pd.Series: A boolean Series indicating duplicates.
        """
        filtered_df = df[df["Type"] == type_filter]

        if position_filter:
            filtered_df = filtered_df[filtered_df["Job Position"] != position_filter]

        return filtered_df.duplicated(subset=[subset_key], keep=keep)

    process_df = df.copy()

    process_df["clock_in_dupe"] = (
        process_df.query("Type == 'Clock In'")
        .duplicated(subset=["unique_key"], keep="first")
        .astype(bool)
    )
    process_df["clock_out_dupe"] = (
        process_df.query("Type == 'Clock Out'")
        .duplicated(subset=["unique_key"], keep="last")
        .astype(bool)
    )

    process_df["clock_in_dupe"] = False  # Default to False
    process_df.loc[process_df["Type"] == "Clock In", "clock_in_dupe"] = mark_duplicates(
        process_df, type_filter="Clock In", position_filter="Security", keep="first"
    )

    process_df["clock_out_dupe"] = False  # Default to False
    process_df.loc[process_df["Type"] == "Clock Out", "clock_out_dupe"] = (
        mark_duplicates(
            process_df, type_filter="Clock Out", position_filter="Security", keep="last"
        )
    )

    process_df[["clock_in_dupe", "clock_out_dupe"]] = process_df[
        ["clock_in_dupe", "clock_out_dupe"]
    ].fillna(False)

    if len(df) != len(process_df):
        raise ValueError("DataFrame length mismatch after processing.")

    process_df.query("~clock_in_dupe & ~clock_out_dupe", inplace=True)
    return process_df


if __name__ == "__main__":
    df = pd.read_excel("test_absen_hr.xlsx", sheet_name="Raw Data")
    remove_clock_type_dupe(df)
