import random

import numpy as np
import pandas as pd


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



if __name__ == '__main__':
    all_objects = pd.read_csv('test_100_recycle.csv', names=['id', 'latitude', 'longitude', 'type', 'mass', 'risk'])
    df_waste = all_objects[all_objects['type'] == 'waste']

    # convert waste node into dictionary
    # each entry looks like
    # 0: {'id': 0, 'latitude': -6, 'longitude': 113, 'type': 'waste', 'mass': 3405592, 'risk': 0.0}
    waste_map = dict([(id, {"id": id, "latitude": latitude, "longitude": longitude, "type": type, "mass": mass, "risk": risk}) for id, latitude, longitude, type, mass, risk in zip(df_waste["id"], df_waste["latitude"], df_waste["longitude"], df_waste["type"], df_waste["mass"], df_waste["risk"])])
    #print(waste_map)

    # get random node index
    ids = []  # list of all ids
    for waste in df_waste.iterrows():
        id = waste[1]["id"]
        ids.append(id)

    # get random node
    random_waste_index = random.randint(0, ids[-1])

    random_waste_node = df_waste.iloc[random_waste_index]

    print("Random node", random_waste_node)

    df_waste = df_waste.drop(random_waste_index)

    # get first node
    current_node = df_waste.iloc[0]
    #print("First waste node", current_node)

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

    print("waste path", waste_node_path)

    waste_node_path.append(random_waste_node)