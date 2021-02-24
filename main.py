import os
import math
import time


class Node:
    def __init__(self, name):
        self.name = name
        self.weight = math.inf # the cost to reach this node
        self.adj_list = []
        self.predecessor = None

        self.heap_index = None # to make it easier to implement the heap

    def add_adj(self, other, distance):
        self.adj_list.append((other, distance))

    def __gt__(self, other):
        return self.weight > other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def reset(self):
        self.weight = math.inf
        self.predecessor = None


class Graph:
    def __init__(self):
        self.nodes = {}

    def add(self, district1, district2, distance):
        node1 = None
        node2 = None

        # create/get node 1
        if district1 in self.nodes:
            node1 = self.nodes[district1]
        else:
            node1 = Node(district1)
            self.nodes[district1] = node1
        # create/get node 2
        if district2 in self.nodes:
            node2 = self.nodes[district2]
        else:
            node2 = Node(district2)
            self.nodes[district2] = node2
        
        # add nodes as adjacents
        node1.add_adj(node2, distance)

    def get_shortest_path(self, origin_str, destination_str):
        if origin_str in self.nodes and destination_str in self.nodes:
            if origin_str == destination_str:
                return origin_str +', ' + destination_str +', 0'

            ori_node = self.nodes[origin_str]
            dest_node = self.nodes[destination_str]
            self.dijkstra(ori_node)
            if dest_node.predecessor == None:
                return [], 'inf'
                
            else:
                current_node = dest_node
                output = [current_node.name]
                while current_node.predecessor != None:
                    current_node = current_node.predecessor
                    output.append(current_node.name)

                return output, dest_node.weight
        else:
            return "Invalid origin or destination", 'inf'

    def dijkstra(self, origin):
        origin.weight = 0

        heap = MinHeap(len(self.nodes))
        for key in self.nodes.keys():
            heap.add(self.nodes[key])

        # heap.build() # add already calls heapify
        while not heap.is_empty():
            min_node = heap.remove(0)
            for adj_node, distance in min_node.adj_list:
                # Relax
                if adj_node.weight > min_node.weight + distance:
                    adj_node.predecessor = min_node
                    # update the weight and the heap
                    adj_node.weight = min_node.weight + distance
                    heap.decrease_key(adj_node.heap_index, adj_node)
            

    def print(self):
        for key in self.nodes.keys():
            print(key)
            adj_string = ''
            for adj, distance in self.nodes[key].adj_list:
                adj_string += adj.name + "(" + str(distance) + "), "

            print(adj_string[0:-2])

    def reset(self):
        for key in self.nodes.keys():
            self.nodes[key].reset()

    def get_num_nodes(self):
        return len(self.nodes.keys())

    def is_valid_node(self, node1, node2):
        cond1 = node1 in self.nodes.keys()
        cond2 = node2 in self.nodes.keys()
        return cond1 and cond2
        
    def get_biggest_short_path(self, origin):
        biggest_by_leaps = None
        leaps_number = 0
        biggest_by_distance = None
        distance = 0

        i = 0
        keys = list(self.nodes.keys())
        keys.remove(origin)
        nodes_lenght = len(self.nodes.keys())-1
        start_time = time.time()
        for key2 in keys:
            i +=1
            if i%100 == 0:
                print('Progress: ' + str(i) + '/' + str(nodes_lenght))
                end_time = time.time()
                print('time: ' + str(end_time - start_time))
                start_time = end_time
            if origin != key2:
                path_list, dist = self.get_shortest_path(origin, key2)
                if dist != 'inf':
                    if dist > distance:
                        distance = dist
                        biggest_by_distance = path_list
                    if len(path_list) > leaps_number:
                        leaps_number = len(path_list)
                        biggest_by_leaps = path_list
        
        return biggest_by_distance, distance, biggest_by_leaps, leaps_number

class MinHeap:
    def __init__(self, size):
        self.buffer = [None]*size
        self.length = size
        self.occupied_size = 0

    def top(self):
        return self.buffer[0]

    def build(self):
        for i in range(len(self.buffer)//2, 1, -1):
            self.min_heapify(i)

    def min_heapify(self, index):
        left_child = 2*(index+1) - 1 # transforms into a 1-indexing vector to do the math then subtract 1 to bring it back to 0-indexing
        right_child = 2*(index+1)    # the right child is 2*i+1, thus, the +1 cancels with the -1 from bringing it back to 0-index
        smaller_node = None
        if(left_child < self.occupied_size and self.buffer[left_child] < self.buffer[index]):
            smaller_node = left_child
        else:
            smaller_node = index

        if(right_child < self.occupied_size and self.buffer[right_child] < self.buffer[smaller_node]):
            smaller_node = right_child
        
        if(smaller_node != index):
            temp = self.buffer[index]
            self.buffer[index] = self.buffer[smaller_node]
            self.buffer[smaller_node] = temp
            # updating the indexes values inside the objects
            self.buffer[index].heap_index = index
            self.buffer[smaller_node].heap_index = smaller_node
            self.min_heapify(smaller_node)

    def decrease_key(self, index, new_node):
        if new_node > self.buffer[index]:
            print('nodes: ' + new_node.name + " --> " + self.buffer[index].name)
            print('wieghts: ' + str(new_node.weight) + " --> " + str(self.buffer[index].weight))
            raise Exception("new key is bigger then current key")
        self.buffer[index] = new_node
        self.buffer[index].heap_index = index
        father_idx = ((index+1)//2)-1 # transforming from 1-index to 0-index
        while index > 0 and self.buffer[father_idx] > self.buffer[index]: # while index is not the first position and the parent -floor(index/2)- is less then the current node
            temp = self.buffer[father_idx]
            self.buffer[father_idx] = self.buffer[index]
            self.buffer[index] = temp
            # updating the indexes values inside the objects
            self.buffer[index].heap_index = index
            self.buffer[father_idx].heap_index = father_idx
            # move on to the father node
            index = father_idx
            father_idx = ((index+1)//2)-1

    def add(self, new_node):
        self.occupied_size += 1
        self.buffer[self.occupied_size-1] = Node('')
        self.decrease_key(self.occupied_size-1, new_node)

    def replace(self, index, new_node): # returns the removed node
        removed = self.remove(index)
        self.add(new_node)
        return removed

    def remove(self, index): # returns the removed node
        removed_node = self.buffer[index]
        self.buffer[index] = self.buffer[self.occupied_size-1]
        self.buffer[self.occupied_size-1] = None # so there is no risk of a dangling reference
        self.occupied_size -= 1
        # updating the indexes values inside the objects
        if(index <= self.occupied_size-1):
            self.buffer[index].heap_index = index
        
        self.min_heapify(0)
        return removed_node

    def is_empty(self):
        return self.occupied_size == 0


def main():
    graph = Graph()

    print('LOADING THE DATA')
    print('please wait')

    # load the data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    i = 0
    with open(current_dir + '\\Data\\treated_data.txt') as file_object:
        for line in file_object:
            if line != '':
                i += 1
                user1, user2, distance = line.split(' ')
                graph.add(user1.strip(), user2.strip(), float(distance.strip()))

    print('Loading done.')
    # print('Please inform which type of search do you want:')
    # print('1 - Links only (all edges have weight equal to 1)')
    # print('2 - Use centroid (edges are weighted by the physical distance between users)')
    # user_input = input('Please inform your choice: ')

    # use_centroid = True # TODO: implement something that makes the edges have weight 1 only
    # if user_input == '1':
    #     use_centroid = False

    compute_stats = input('Do you want to check whats the largest distance? y/n?')
    # print('(note that this may take a while as each pair of nodes is checked')
    
    if compute_stats == 'y':
        origin = input('Which user do you want to check?')
        print('Crunching some data here... please wait')
        biggest_by_distance, distance, biggest_by_leaps, leaps_number = graph.get_biggest_short_path(origin)
        path = ''
        for user in biggest_by_distance:
            path = user + '==>>' + path

        print('The biggest path by distance is: ' + path[0:-4])
        print('Total distance: ' + str(distance))
        path = ''
        for user in biggest_by_leaps:
            path = user + '==>>' + path
        print('The highest number of leaps to reach a user is: ' + str(leaps_number))
        print('Which goes by: ' + path)

    print()
    print('Configuration done. Here are some stats:')
    print('Number of nodes: ' + str(graph.get_num_nodes()))
    print('Number of edges: ' + str(i))
    # print("Use centroid? " + str(use_centroid))
    print()

    origin = ''
    dest = ''
    while origin != 'q' and dest != 'q':
        print('Now, inform the users you want to check. Press "q" to quit.')
        origin = input('Please inform the first user: ')
        dest = input('Please inform the second user: ')
        if graph.is_valid_node(origin, dest):
            print('The shortest path between {0} and {1} is:'.format(origin, dest))
            path_list, distance = graph.get_shortest_path(origin.strip(),dest.strip()) # TODO: get each output individually and print in a better way
            if path_list != []:
                path = ''
                for user in path_list:
                    path = user + '==>>' + path

                print('Path to follow: ' + path[0:-4])
                print('Total distance: ' + str(distance))
            else:
                print("Sorry, you can't reach " + dest + ' from ' + origin)

            # clean up for the next search
            print()
            print('Wait a little while we clean things up!') # it may take a while on slower pcs
            graph.reset()
        elif origin != 'q' and dest != 'q':
            print('Sorry, one of the users is not valid.')

    print()
    print('PROGRAM TERMINATED')
    print('See you soon! o/')

if __name__ == '__main__':
    main()
