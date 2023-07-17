import os
import glob
import pandas as pd
import re

# Define constants
BASE_DIR = r"E:/Your/working/direction"
MP_DATA_PATH = os.path.join(BASE_DIR, 'Final/MPData.csv')
ELEC_DATA_PATH = os.path.join(BASE_DIR, 'Final/ElecData.csv')
FINAL_PATH = os.path.join(BASE_DIR, "Final/Final.csv")

# Function to extract year from date string
def extract_year(date_str):
    return date_str.str.extract('(\d+)').fillna(0).astype('int')


# Function to append table files (excel and csv) under a given path
# This function is used twice for both mp_data and election_data
def append_table_files(file_pattern, sep):
    df_appended = pd.DataFrame()

    # Get all files by matching the file pattern
    files = glob.glob(file_pattern)
    for file in files:
        try:
            if 'csv' in file_pattern:
                df = pd.read_csv(file, sep=sep)
            else:
                df = pd.read_excel(file)
            print("Successfully load file")
            # Extract MP ID from the file name
            df['MP_ID'] = re.findall(r'(\d+)(?!.*\d)', file)[0]
            df_appended = pd.concat([df_appended, df])
        except:
            print(f"Failed to process file {file}")
    return df_appended


# Function to process and append FED files
def append_fed_files(file_pattern, sep):
    df_appended = pd.DataFrame()
    files = glob.glob(file_pattern)
    for file in files:
        try:
            df = pd.read_csv(file, sep=";", header=None).T
            cols = df.shape[1]
            df2 = df.iloc[:, 0]
            for i in range(cols):
                # print(i)
                if i > 0:
                    df3 = df.iloc[:, i]
                    frame = [df2, df3]
                    df2 = pd.concat(frame)
                else:
                    print("only one column")
            df = df2.to_frame()
            df.columns = ['entry']
            df['entry'] = df['entry'].astype(str)
            df = df[df['entry'].str.contains('OrganizationId')]
            ID = df['entry'].str.extract('(\d+)').fillna(0).astype('int')
            NAME = df['entry'].to_frame()
            NAME = NAME['entry'].str.split(">", n=1, expand=True)
            NAME.columns = ['e1', 'e2']
            NAME = NAME['e2'].str.split("<", n=1, expand=True)
            frame = [ID, NAME]
            final = pd.concat(frame, axis=1)
            final.columns = ['FED_ID', 'Name', 'rest']
            final = final[['FED_ID', 'Name']]
            final = final.drop_duplicates()
            frame = [df_append, final]
            df_append = pd.concat(frame, ignore_index=True)
        except:
            print(f"Failed to process file {file}")
    return df_appended.drop_duplicates()

# Change working directory
os.chdir(BASE_DIR)

# Append all MP_ID Files and process
df_mp_data = append_table_files('Output/MP_ID_[0-9]*csv', ';')
df_mp_data = df_mp_data[['MP_ID'] + [col for col in df_mp_data.columns if col != 'MP_ID']]
df_mp_data.rename(columns={'Date of Birth (yyyy-mm-dd):': 'DateBirth'}, inplace=True)
df_mp_data['DateBirth'] = df_mp_data['DateBirth'].astype(str)
df_mp_data['birthyear'] = extract_year(df_mp_data['DateBirth'])
df_mp_data.to_csv(MP_DATA_PATH, index=False, sep=";")

# Append the Electoral History files and process
df_election_data = append_table_files('Output/ElectoralHistory_[0-9]*xlsx', ',')
df_election_data = df_election_data[['MP_ID'] + [col for col in df_election_data.columns if col != 'MP_ID']]
df_election_data.sort_values(['MP_ID', 'Parliament'])
df_election_data.rename(columns={'Election Date': 'ElectionDate'}, inplace=True)
df_election_data['ElectionDate'] = df_election_data['ElectionDate'].astype(str)
df_election_data['electionyear'] = extract_year(df_election_data['ElectionDate'])
df_election_data.to_csv(ELEC_DATA_PATH, index=False, sep=';')

# Process and append FED files
df_fed = append_fed_files('Output/MP_ID_FED_[0-9]*csv', ';')

# Merge data
df_election = pd.read_csv(ELEC_DATA_PATH, sep=";")
df_mp = pd.read_csv(MP_DATA_PATH, sep=";")
final = df_election.merge(df_fed, left_on="Constituency", right_on="Name", how='left')
final = final.merge(df_mp, on="MP_ID", how='left')
final['Age_at_Election'] = final['electionyear'] - final['birthyear']

# Save final data
final.to_csv(FINAL_PATH, index=False, sep=";")
