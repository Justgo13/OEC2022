import random
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

def euclid_dist(x1, y1, x2, y2):
    """
    Calculate euclidean distance
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    return np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))

def get_xy(df):
    return df[['longitude','longitude']].to_numpy()
def get_combination_dist(df,df2):
    ar1 = get_xy(df)
    ar2 = get_xy(df2)
    return cdist(ar1, ar2)
def get_min(ar):
    return np.argmin(ar), np.min(ar)

def get_processing(A,B, all_objects):
    #make data frames
    df_waste = all_objects[all_objects['type'] == 'waste']
    df_local_sort = all_objects[all_objects['type'] == 'local_sorting_facility']
    df_regional_sort = all_objects[all_objects['type'] == 'regional_sorting_facility']
    df_regional_recycling = all_objects[all_objects['type'] == 'regional_recycling_facility']

    total_waste = df_waste['mass'].sum()

    distance_cost = (A + B) * get_combination_dist(df_local_sort, df_regional_sort)
    risk_matrix = A * (1 - np.outer(1 - df_local_sort['risk'].to_numpy(), 1 - df_regional_sort['risk'].to_numpy()))
    cost_matrix=risk_matrix+distance_cost
    row, column = cost_matrix.argmin() // cost_matrix.shape[1], cost_matrix.argmin() % cost_matrix.shape[1]
    selected_local_sort = df_local_sort.iloc[row]
    selected_region_sort = df_regional_sort.iloc[column]
    dist_arg1 = df_regional_recycling['longitude'].to_numpy() - selected_region_sort.longitude
    dist_arg2 = df_regional_recycling['latitude'].to_numpy() - selected_region_sort.latitude
    dist_args = np.square(dist_arg1) + np.square(dist_arg2)
    selected_recycle = df_regional_recycling.iloc[np.argmin(dist_args)]
    dist_x = df_waste['longitude'].to_numpy() - selected_recycle.longitude
    dist_y = df_waste['latitude'].to_numpy() - selected_recycle.latitude
    distances = np.square(dist_x) + np.square(dist_y)
    final_node_index = np.argmin(distances)
    final_node = df_waste.iloc[final_node_index]

    output = get_waste(final_node_index, df_waste)
    output += [selected_local_sort, selected_region_sort, selected_recycle]
    return output


def get_waste(final_waste_index, df_waste):
    # get random node index
    ids = []  # list of all ids
    for waste in df_waste.iterrows():
        id = waste[1]["id"]
        ids.append(id)
    final_node = df_waste.iloc[final_waste_index]
    df_waste = df_waste.drop(final_waste_index)
    # get first node
    current_node = df_waste.iloc[0]
    waste_node_path = []
    waste_node_path.append(current_node)
    # get distance from current node to nearest node and add to a list
    # nearest node only is added to the list if it doesn't already exist
    for index in range(0, df_waste.size):
        # remove first node from waste map
        df_waste = df_waste.drop(current_node["id"])
        current_node_lat = current_node.latitude
        current_node_long = current_node.longitude
        current_node_index = current_node.id
        # calculate distance from current node to other nodes
        dist_x = df_waste["longitude"].to_numpy() - current_node_long
        dist_y = df_waste["latitude"].to_numpy() - current_node_lat
        distances = np.sqrt(np.square(dist_x) + np.square(dist_y))
        if len(distances) == 0:
            break
        min_distance_index = np.argmin(distances)
        nearest_waste_node = df_waste.iloc[min_distance_index]
        # add this node to the list of nodes
        waste_node_path.append(nearest_waste_node)
        # nearest node is now current node
        current_node = nearest_waste_node
    waste_node_path.append(final_node)
    return waste_node_path

