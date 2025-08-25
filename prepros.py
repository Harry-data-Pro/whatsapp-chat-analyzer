import re
import pandas as pd

def preprocess(raw_text: str) -> pd.DataFrame:
    line_pat = re.compile(
        r"""^
            (?P<datetime>\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}[ \u202F\u00A0]?[ap]\.?m\.?)
            \s*-\s*
            (?P<name>[^:]+):
            \s*
            (?P<msg>.*)
            $""",
        re.VERBOSE | re.IGNORECASE,
    )

    records = []
    for line in raw_text.splitlines():
        m = line_pat.match(line)
        if m:
            records.append(m.groupdict())
        elif records:                       # multi-line continuation
            records[-1]["msg"] += "\n" + line

    df = pd.DataFrame(records, columns=["datetime", "name", "msg"])
    df["timestamp"] = pd.to_datetime(df["datetime"], dayfirst=True, errors="coerce")
    df = df.drop(columns="datetime")
    df["Year"]   = df["timestamp"].dt.year
    df['Month_num'] = df['timestamp'].dt.month
    df["Month"]  = df["timestamp"].dt.month_name()
    df["Day"]    = df["timestamp"].dt.day
    df['Day_name'] = df['timestamp'].dt.day_name()
    df["Hour"]   = df["timestamp"].dt.hour
    df["Minute"] = df["timestamp"].dt.minute

    period = []
    for i in df[['Day_name','Hour']]['Hour']:
        if i == 23:
            period.append(str(i) + '-' + str('00'))
        elif i == 0:
            period.append(str('00') + '-' + str(i+1))
        else:
            period.append(str(i) + '-' + str(i+1))
    df['period'] = period
    return df
