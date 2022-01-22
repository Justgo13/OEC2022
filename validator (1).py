import math
import sys

# helper function to read from a csv file and return the info in a list
# can be used when: read from map & read from path (if the path file is also csv)
def read_from_csv(file_name):
    res = []
    with open(file_name + ".csv") as csv_file:
        node = [line.split(",") for line in csv_file]
        for i, info in enumerate(node):
            #print ("line{0} = {1}".format(i, info))
            #print(type(info))
            res.append(info)
    return res


def get_delta_distance(latLon1, latLon2):
    
    R = 6371
    x1_lat, y1_lon = latLon1
    x2_lat, y2_lon = latLon2
    #print(x1_lat, ",", y1_lon)
    latavg = (int(x1_lat) + int(x2_lat))/2

    x1 = R * int(y1_lon) * math.cos(latavg)
    y1 = R * int(x1_lat)

    x2 = R * int(y2_lon) * math.cos(latavg)
    y2 = R * int(x2_lat)

    return (math.hypot(abs(x1-x2), abs(y1-y2))/1000)


# return: QoR (number)
# if -1: not valid
def validator(map_file, solution_file, a, b):

    #read from map file: add nodes to list. Maybe declare custom data type to store all the info
    #id, location, fac_type, load, loss%
    map_nodes = read_from_csv(map_file)
    #read from path file: store node id# to list
    path_nodes = read_from_csv(solution_file)
    # type-label dict
    type_label = {
        "waste": "pickup",
        "local_sorting_facility": "local sorted",
        "regional_sorting_facility": "regional sorted",
        "regional_recycling_facility": "done"
    }


    is_valid = True
    #check if first node is valid
    if (map_nodes[0][0] != path_nodes[0][0]):
        #print(map_nodes[0][0])
        #print(path_nodes[0][0])
        is_valid = False
        print("The path is not valid: not starting at the right node")
        return -1
    # create waste_nodes (array of ids) to check if all waste nodes are included in solution
    waste_nodes = []
    for i in range(len(map_nodes)):
        if map_nodes[i][3] == "waste":
            waste_nodes.append(int(map_nodes[i][0]))
    # store the nodes that has been checked
    # structure: id, label, location, weight
    processed_nodes = []
    total_loss = 0
    total_distance = 0

    for i in range(len(path_nodes)):
        cur_id = int(path_nodes[i][0])
        #print("current path node info: ",path_nodes[i])

        cur_type = map_nodes[cur_id][3]
        cur_weight = float(map_nodes[cur_id][4].strip("\n"))
        cur_loss = float(map_nodes[cur_id][-1])
        cur_loc = (map_nodes[cur_id][1],map_nodes[cur_id][2])

        if cur_id in waste_nodes:
            waste_nodes.remove(cur_id)

        # based on cur_type, update the labels and carried weights of previous nodes
        # calculate the loss first then update the weights
        if len(processed_nodes) != 0:
            
            distance = get_delta_distance(cur_loc, processed_nodes[-1][2])
            total_distance += distance
            #print("new total distance: ",total_distance)
            # if cur_type is "waste": no loss and no updating labels
            # just need to append the node to the processed_nodes
            if cur_type != "waste":
                for node in processed_nodes:
                    #print("node info: ",node)

                    if node[3] > 0:
                        total_loss += node[3] * cur_loss * distance
                    # update the weights at each node
                    node[3] = max(0, (node[3] - node[3] * cur_loss * distance))
                    node_label = node[1]
                    #print("node label: ",node_label," & current type: ",cur_type)

                    # update the labels
                    if cur_type == "local_sorting_facility" and node_label == "pickup":
                        node[1] = "local sorted"
                    elif cur_type == "regional_sorting_facility" and node_label == "local sorted":
                        node[1] = "regional sorted"
                    elif cur_type == "regional_recycling_facility" and node_label == "regional sorted":
                        node[1] = "done"
                        node[3] = 0
                    #print("UPDATED node label: ",node[1])
        # append the node info to processed_nodes
        cur_label = type_label[cur_type]
        processed_node = [cur_id, cur_label, cur_loc, cur_weight]
        processed_nodes.append(processed_node)
    for node in processed_nodes:
        if waste_nodes:
            print("Not all waste nodes have been processed")
            return -1
        if node[1] != "done":
            print("The path is not valid: not all nodes are processed: ",node[1])
            return -1
    if is_valid:
        QoR = (a * total_loss + b * total_distance) #*run time
        print("QoR:", QoR)
        return QoR
# helper
def convert_str_node(node_str):
    node_list = node_str.split(",")
    node = []
    #print(node_list)
    for i in range(len(node_list)):
        node.append(int(node_list[0]))
        lat = int(node_list[1])
        lon = int(node_list[2])
        node.append([lat, lon])
        node.append(node_list[3])
        node.append(int(node_list[4]))
        node.append(float(node_list[5]))
    return node
    
# #initialize pickup load states, to track which loads have been processed
# load_states_list = ["pickup", "local sort", "regional sort", "done"]
# pickup_load_states = [] #pickup, local sort, regional sort, done
# pickup_load_ids = []
# pickup_load_kg = []
# #initialize total distance and total loss (kg)
# total_distance = 0
# total_loss = 0

# valid_flag = True

# #check if first node is valid
# if (map_nodes[0][0] != path_nodes[0]):
#     valid_flag = False
# prev_loc = map_nodes[0][1]
# #FOR EACH node in path:
# for node in path_nodes:
#     mass = 0
# #   if type = pickup: update pickup load states
#     if (map_nodes[node][2] == "waste" and valid_flag):
#         pickup_load_states.append("pickup")
#         pickup_load_ids.append(node)
#         pickup_load_kg.append(map_nodes[node][3])

# #   if type = process fac: update pickup load states, calculate loss amount and delta distance

#     delta_distance = node[1] - prev_loc

#     for i in range (1, type_facilities.length-1): #for each fac type
#         if map_nodes[node][2] == type_facilities[i]: #if current node fac type = array fac type
#             load_id = pickup_load_states.find(load_states_list[i-1]) #find package # that needs to be processed
#             if (load_id >= 0): #if package # is found
#                 pickup_load_states[load_id] = load_states_list[i] #update this pacakge status
#                 #mass = pickup_load_kg[load_id] #update mass being processed
#             if (type_facilities.length-1 == i): #final fac
#                 total_loss += delta_distance*pickup_load_kg[load_id]*node[4]
#                 pickup_load_kg[load_id] = 0

#     #delta_distance = node[1] - prev_loc
#     total_distance += delta_distance
#     prev_loc = node[1]
#     mass = sum(pickup_load_kg)
#     total_loss += delta_distance*mass*node[4]
#     pickup_load_kg = [element * (1-node[4]) for element in pickup_load_kg]
    

#     # elif (map_nodes[node][2] == "local sorting facility" and valid_flag):

#     #     for load_id in range (0, pickup_load_ids.length-1):
#     #         if pickup_load_states[load_id] == "pickup":
#     #             pickup_load_states[load_id] = "local sort"
#     #             mass += pickup_load_kg[load_id]

#     # elif (map_nodes[node][2] == "regional sorting facility" and valid_flag):

#     #     for load_id in range (0, pickup_load_ids.length-1):
#     #         if pickup_load_states[load_id] == "local sort":
#     #             pickup_load_states[load_id] = "regional sort"
#     #             mass += pickup_load_kg[load_id]

#     # elif (map_nodes[node][2] == "regional recycling facility" and valid_flag):

#     #     for load_id in range (0, pickup_load_ids.length-1):
#     #         if pickup_load_states[load_id] == "regional sort":
#     #             pickup_load_states[load_id] = "done"
#     #             mass += pickup_load_kg[load_id]
    
#     # else:
#     #     valid_flag = False

#     # if (valid_flag):
#     #     delta_distance = node[1] - prev_loc
#     #     total_distance += delta_distance
#     #     prev_loc = node[1]
#     #     total_loss += delta_distance*mass*node[4]
# #   if no action available: return invalid

# #check if all pickup load states are considered finished
# for load_state in pickup_load_states:
#     if (load_state != "done"):
#         valid_flag = False
#         break

# #if not all finished, return invalid

# #if all finished, calculate and return QOR
# #QoR = (a*amount of plastic in ocean + b*distance) * run time (minutes)
# if (valid_flag):
#     QoR = (total_loss + total_distance) #*run time
#     print(QoR)


