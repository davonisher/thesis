import pandas as pd
import requests
import json
import numpy as np

file_path1 = '/Users/macbook/thesis/new/code/data/processed_data/final.csv'
data = pd.read_csv(file_path1, sep=',', encoding='utf-8', dtype='unicode')

#code retrieved from mberman84 (2024)
# 
url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}
conversation_history = []
# function to generate response
def generate_response(prompt):
    conversation_history.append(prompt)
    full_prompt = "\n".join(conversation_history)
    data = {
        "model": "mistral",
        "stream": False,
        "prompt": full_prompt,
        "temperature": 0.7,
        "max_tokens": 50,
    }
    # post request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)
        return actual_response
    else:
        print("Error:", response.status_code, response.text)
        return None

# generate new descriptions
#code retrieved from ChatGPT (2024)
def generate_new_descriptions(data):
    data['desc'] = data[['product description', 'full_description', 'description']].apply(lambda x: ' '.join(x.dropna()), axis=1)
    descriptions = data['desc'].tolist()
    tool_ids = data['tool_id'].tolist()
#    loop through the data
    generated_data = []
    for tool_id, description in zip(tool_ids, descriptions[:2]):  # Limit to the first five for testing
        try:
            prompt = "Create a compelling product description based on the following information: " + description
            generated_description = generate_response(prompt)
            generated_data.append({'tool_id': tool_id, 'new_description': generated_description})
        except Exception as e:
            print(f"An error occurred: {e}")
            generated_data.append({'tool_id': tool_id, 'new_description': ""})
#   return generated data
    return generated_data

# function calling generate new descriptions
generated_data = generate_new_descriptions(data)
generated_df = pd.DataFrame(generated_data)

# function calling
#generated_descs = generate_new_descriptions(data)

# Vul de lijst aan tot de lengte van de DataFrame
generated_descs += [np.nan] * (len(data) - len(generated_descs))

# update the data
data['new_description'] = generated_descs

#print sample of new descriptions
print(data['new_description'].head(5))