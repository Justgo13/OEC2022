
import numpy as np
import pandas as pd
# constants to be replaced later
CSV_FILE = 'test_100_recycle.csv'
A=1
B=1

if __name__ == "__main__":
    # seperate types
    all_objects = pd.read_csv('test_100_recycle.csv', names=['id', 'longitude', 'lattitude', 'type', 'mass', 'risk'])
    df_waste = all_objects[all_objects['type'] == 'waste']
    df_local_sort = all_objects[all_objects['type'] == 'local_sorting_facility']
    df_regional_sort = all_objects[all_objects['type'] == 'regional_sorting_facility']
    df_regional_recycling = all_objects[all_objects['type'] == 'regional_recycling_facility']

    pass