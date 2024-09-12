import pandas as pd
import datetime as dt

def parse_time_str(time_str: str) -> dt.time:
    """
    Accepts strings in the format of HH:MM(a/p) and
    returns a time object representing that string
    EX: 9:30p -> 21:30:00
    """
    if(time_str == "noon"):
        return dt.time(12, 0)
    
    elif(time_str == "midnight"):
        return dt.time(0, 0)
    
    else:
        split = time_str.split(":")
        hour = int(split[0])
        minute = int(split[1][:2])
        meridiem = split[1][2:]

        if(meridiem == 'p' and hour != 12):
            hour += 12

        return dt.time(hour, minute)

def parse_date_str(date_str: str) -> dt.date:
    """
    Accepts strings in the format of MM/DD/YYY and
    returns a date object representing that string
    """
    month, day, year = date_str.split("/")
    return dt.date(int(year), int(month), int(day))

def load_df(file_name: str) -> pd.DataFrame:
    """
    Loads and formats a DataFrame from the given csv filename
    returns the DataFrame Object
    """

    cols = ["Name", "Section", "Type", "Title", "Date", "Published Start", "Published End", "Location", "Instructor / Organization"]
    df = pd.read_csv(file_name, usecols= cols)

    # format
    df = df.rename(columns={'Published Start': 'Start', 'Published End':'End'})
    df[["Start", "End"]] = df[["Start", "End"]].map(parse_time_str)
    df[["Date"]] = df[["Date"]].map(parse_date_str)

    return df

def get_now(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gets the objects of the DataFrame which are scheduled to be now
    """
    today = dt.datetime.today()
    df_now = df[(df["Date"] == today.date()) & (df["Start"] <= today.time()) & (df["End"] >= today.time())]
    return df_now