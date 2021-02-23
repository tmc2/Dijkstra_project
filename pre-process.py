# Code to pre-process the data and build a unique file with desired information
import os
import math

current_dir = os.path.dirname(os.path.abspath(__file__))

# read nodes file
users_info = {}
with open(current_dir + '\\Data\\Brightkite_totalCheckins.txt') as file_object:
    for line in file_object:
        if line != '':
            # [user] [check-in time] [latitude] [longitude] [location id]
            try:
                user, _, latitude, longitude, _ = line[0:-2].split(' ')
            except ValueError:
                print('error while reading line:')
                print(line)
                print("line do not follow the expected pattern")
                continue

            if latitude != '0.0' and latitude != '' and\
            longitude != '0.0' and longitude != '': # this means there was an error checking in to that place
                if user in users_info.keys():
                    users_info[user].append((float(latitude), float(longitude))) # I'm keeping each value to use later if I decide to compute the closest points between links
                else:
                    users_info[user] = [(float(latitude), float(longitude))]

# compute centroids
centroids = {}
for user in users_info.keys():
    latitude_sum = 0
    longitude_sum = 0
    for latitude, longitude in users_info[user]:
        latitude_sum += latitude
        longitude_sum += longitude

    centroids[user] = (latitude_sum/len(users_info[user]), longitude_sum/len(users_info[user]))

output_file = open(current_dir + '\\Data\\trated_data.txt', 'w')
with open(current_dir + '\\Data\\Brightkite_edges.txt') as file_object:
    for line in file_object:
        node1, node2 = line[0:-2].split(' ')
        # node1 = int(node1)
        # node2 = int(node2)

        # TODO: compute closest point between two linked users and also export this information

        # export using only the centroid
        if node1 != '' and node2 != '':
            if node1 in centroids.keys() and node2 in centroids.keys(): # there are some broken links on the file (edges to users that doesnt appear on Brightkite_totalCheckins.txt)
                # TODO: exclude links that points to the same local if necessary
                distance = math.sqrt((centroids[node1][0] - centroids[node2][0])**2 + (centroids[node1][1] - centroids[node2][1])**2)
                output_file.write( "{0} {1} {2:.3f}\n".format(node1, node2, distance) )

output_file.close()
