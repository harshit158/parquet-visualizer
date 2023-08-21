import streamlit as st
import pandas as pd
import json
import subprocess
import re

# Title and instructions
st.title("Parquet File Viewer")
st.write("Upload a Parquet file to view its contents.")

# Upload a Parquet file
uploaded_file = st.file_uploader("Choose a Parquet file", type=["parquet"])

def parquet_to_json(parquet_filename):
    df = pd.read_parquet(parquet_filename)
    json_obj = json.loads(df.to_json())
    return df, json_obj

if uploaded_file:
    # Load the Parquet file into a DataFrame
    json_obj = parquet_to_json(uploaded_file)
    
    # Display the DataFrame
    st.write("Preview of the Parquet file contents:")
    
    # st.write(json_obj)
    # print(json_obj[1])
    objects = sum(json_obj[1]['interfaces'].values(), [])
    filtered_objects = []
    
    for object in objects:
        new_dict = {}
        if ('lanes' in object and object['lanes']) and \
            'module_temperature' in object and \
            object['model_type'] == 'LR4':
                
            new_dict['name'] = object['name']
            new_dict['lanes'] = object['lanes']
            new_dict['module_temperature'] = object['module_temperature']
        
        if new_dict:
            filtered_objects.append(new_dict)
            
    st.write(filtered_objects)
    
# Input box for the command
command = st.text_input("Enter a terminal command:", "")

def grep(file_object, search_text):
    matching_lines = []
    for line in file_object:
        if search_text in line:
            matching_lines.append(line)
    return matching_lines

if st.button("Run Command"):
    if command:
        try:
            output = subprocess.check_output(command, shell=True, text=True)
            st.write("Command Output:")
            st.code(output)
        except subprocess.CalledProcessError as e:
            st.error(f"Command failed with error: {e}")
    else:
        st.warning("Please enter a command.")
        
        


# Example usage
search_text = "keyword"
file_content = ["Line 1 with keyword", "Line 2 without", "Another line with keyword"]

# Simulate a file object by treating a list as lines
matching_lines = grep(file_content, search_text)