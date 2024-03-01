
#importing the required libraries
import pandas as pd
import requests
import json

# file path
file_path1 = '/Users/macbook/thesis/new/code/data/raw_data/df_merged2.csv'

# loading dataset 
data = pd.read_csv(file_path1, encoding='ISO-8859-1', sep=',')

#data = data.copy()

# Function to interact with classifier model
#code retrieved from mberman84 (2024)
def generate_response(description):
    # Replace with classifier API endpoint
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": "cs14", 
        "prompt": description,
        "stream": False,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print("Response Text:", response.text)  # Debugging line

    if response.status_code == 200:
        response_data = json.loads(response.text)
        return response_data["response"].strip()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
# Select the rows
example_data = data.head(1000)

# Apply the generate_response function to each description
example_data['llm_response'] = example_data['full_description'].apply(generate_response)

# Display the results
print(example_data[['tool_id', 'full_description','llm_response']])

# Save the modified DataFrame to a CSV file
output_file_path = '/Users/macbook/thesis/new/code/data/processed_data/cd2.csv'
example_data.to_csv(output_file_path, index=False)

print(f"Data saved to {output_file_path}")

# mberman84 (2024) (https://gist.github.com/mberman84/a1291cfb08d0a37c3d439028f3bc5f26)