import pandas as pd
import json

# Load your JSON data
with open('nested_data.json') as json_file:
    data = json.load(json_file)

# Initialize a list to store flattened rows
flattened_rows = []

# Process each program in the JSON data
for program in data['programs']:
    flattened_row = {
        'season': program['season'],
        'orchestra': program['orchestra'],
        'programID': program['programID'],
        'id': program['id'],
    }

    for concert in program['concerts']:
        flattened_concert = flattened_row.copy()
        flattened_concert.update(concert)
        flattened_rows.append(flattened_concert)

    for work in program['works']:
        flattened_work = flattened_row.copy()
        flattened_work.update(work)
        
        # Explode 'soloists' array
        soloists_list = flattened_work.pop('soloists')
        for soloist in soloists_list:
            flattened_soloist = flattened_work.copy()
            flattened_soloist.update(soloist)
            flattened_rows.append(flattened_soloist)

        flattened_rows.append(flattened_work)

# Create a DataFrame from the flattened rows
combined_table = pd.DataFrame(flattened_rows)

# Save the combined DataFrame to a CSV file
combined_table.to_csv('combined_table.csv', index=False)
