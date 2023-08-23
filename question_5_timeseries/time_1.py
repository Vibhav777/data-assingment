import pandas as pd

# Load the Excel file
file_path = 'timeseries.xlsx'
data = pd.read_excel(file_path)

# Sort the data by bot and Start time
data.sort_values(by=['Name', 'Start'], inplace=True)

work_periods = []
current_bot = None
current_period = None

for index, row in data.iterrows():
    if current_bot is None or current_bot != row['Name'] or (row['Start'] - current_period[2]).seconds > 300:
        if current_period:
            work_periods.append(current_period)
        current_period = [row['Name'], row['Start'], row['End'], [row['Activity']]]
    else:
        current_period[2] = row['End']
        current_period[3].append(row['Activity'])
    
    current_bot = row['Name']

# Add the last work period
if current_period:
    work_periods.append(current_period)

# Create a DataFrame from the result
result_df = pd.DataFrame(work_periods, columns=['Name', 'Start', 'end', 'Activity'])
print(result_df)
result_df.to_csv('time.csv', index=False)