import streamlit as st
import pandas as pd
import json
import subprocess
from pprint import pprint
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
    df, json_obj = parquet_to_json(uploaded_file)

    # Display the DataFrame
    st.write("Preview of the Parquet file contents:")
    
    # Extracting org_ids and interface_values
    org_ids = list(json_obj['org_id'].values())
    interface_values_per_org = list(json_obj['interfaces'].values())
    assert len(org_ids) == len(interface_values_per_org), 'number of org_ids does not match with number of interfaces'
    
    # Manually adding org_id for Ultron
    if '3b1220d1-cae3-4075-baad-171e09aa9a6e' not in org_ids:
        org_ids += ['3b1220d1-cae3-4075-baad-171e09aa9a6e']
        
    options = st.multiselect(
                'Select ORG_ID',
                list(set(org_ids)),
                '3b1220d1-cae3-4075-baad-171e09aa9a6e')
    
    filtered_objects = []
    for org_id, interface_values in zip(org_ids, interface_values_per_org):
        if options and org_id not in options:
            continue
        for interface_value in interface_values:
            new_dict = {}
            if ('lanes' in interface_value and interface_value['lanes']) and \
                'module_temperature' in interface_value and \
                interface_value['model_type'] == 'LR4':
                
                new_dict['org_id'] = org_id
                new_dict['name'] = interface_value['name']
                new_dict['link'] = interface_value['link']
                new_dict['model_type'] = interface_value['model_type']
                new_dict['lanes'] = interface_value['lanes']
                new_dict['module_temperature'] = interface_value['module_temperature']
            
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