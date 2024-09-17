import pandas as pd
import datetime as dt

def parse_multiple_class_names(df:pd.DataFrame) -> pd.DataFrame:

    multiple_names = df["Name"].str.contains('\n', case=False, na=False)
    df_two_names = df[multiple_names] # isolate classes with two names
    df = df[~multiple_names] # remove those from df

    # create new df
    new_rows = []
    for _, row in df_two_names.iterrows():

        # names
        names = row["Name"].split('\n') # split the names
        titles = row["Title"].split('\n')
        sections = row["Section"].split('\n')

        for i in range(len(names)):
            new_row = row.copy()
            new_row["Name"] = names[i].lstrip().rstrip()

            if(titles[i].lstrip().rstrip() == ""):
                new_row["Title"] = titles[i-1].lstrip().rstrip()
            else:
                new_row["Title"] = titles[i].lstrip().rstrip()

            new_row["Section"] = sections[i].lstrip().rstrip().replace("*","")

            new_rows.append(new_row)

    df_two_names = pd.DataFrame(new_rows)
    return pd.concat([df, df_two_names]) # combine them back together

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

def format_instructor_str(cell: str) -> str:
    if type(cell) == float:
        return cell
    
    return cell.replace('\n', ', ')

def get_locations(df: pd.DataFrame) -> list:
    locations = sorted(df["Location"].unique())
    return locations

def get_instructors(df: pd.DataFrame) -> list:
        """
        get a list off all instructors
        """
        instructors = df[df["Instructor / Organization"].notna()]["Instructor / Organization"].unique() # get list of non nan Instructors
        instructors = [x.replace(" (Instr)", "") for x in instructors] # remove " (Instr)" substring
        instructors = [name for person in instructors for name in person.split('\n')] # split multiple names
        instructors = list(dict.fromkeys(instructors)) # remove duplicates
        instructors = [item for item in instructors if "," in item] # remove Club names
        instructors = sorted(instructors) # sort alphabetically
        return instructors

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
    df[["Instructor / Organization"]] = df[["Instructor / Organization"]].map(format_instructor_str)
    df = parse_multiple_class_names(df) # remove multiple classes in one line


    return df

def get_now(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gets the objects of the DataFrame which are scheduled to be now
    """
    today = dt.datetime.today()
    df_now = df[(df["Date"] == today.date()) & (df["Start"] <= today.time()) & (df["End"] >= today.time())]
    return df_now