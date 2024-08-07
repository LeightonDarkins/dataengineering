import glob
import pandas as pd
import json
import os
import sys

# function to extract the column names from a Dict called 'schemas'
def get_column_names(schemas, dataset_name, sorting_key='column_position'):
    column_details = schemas[dataset_name]
    columns = sorted(column_details, key = lambda col: col[sorting_key])
    return [col['column_name'] for col in columns]

def get_file_details(file):
    file_path_tokens = file.split('/')
    file_details = {
        'dataset_name': file_path_tokens[-2],
        'file_name': file_path_tokens[-1]
    }
    return file_details

# read a given csv, applying the given schema, return a dataframe presenting the file
def read_csv(file, schemas):
    print(f'Reading: {file}')
    file_details = get_file_details(file)
    
    column_names = get_column_names(schemas, file_details['dataset_name'])
    return pd.read_csv(file, names=column_names)

def write_json(data, output_base_dir, file):
    file_details = get_file_details(file)

    json_folder_path = f'{output_base_dir}/{file_details['dataset_name']}' 
    json_file_path = f'{json_folder_path}/{file_details['file_name']}'

    print(f'Writing: {json_file_path}')

    os.makedirs(f'{json_folder_path}', exist_ok=True)
    data.to_json(json_file_path, orient='records', lines=True)

def file_converter(input_base_dir, output_base_dir, schemas, dataset_name):
    files = glob.glob(f'{input_base_dir}/{dataset_name}/part-*')

    if len(files) == 0:
        raise NameError(f'No files found for {dataset_name}')
    
    for file in files:
        data = read_csv(file, schemas)
        write_json(data, output_base_dir, file)

def process_files(dataset_names=None):
    input_base_dir = 'data/retail_db'
    output_base_dir = 'data/retail_db_json'
    schemas = json.load(open(f'{input_base_dir}/schemas.json'))

    if not dataset_names:
        dataset_names = schemas.keys()

    for dataset_name in dataset_names:
        try:
            print(f'Processing: {dataset_name}')
            file_converter(input_base_dir, output_base_dir, schemas, dataset_name)
        except NameError as ne:
            print(ne)
            print(f'Error Processing {dataset_name}')
            pass

if __name__ == '__main__':
    process_files()