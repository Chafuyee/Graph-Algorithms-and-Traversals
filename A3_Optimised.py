
import sys

#==================================
# H E L P E R  F U N C T I O N S
#==================================

def file_reader():
    data_list = []
    for line in sys.stdin:
        data_list += [line]
    return data_list

def create_digraphs(data=[]):
    # returns a list of digraph objects
    if data == []:
        data = file_reader()
    digraph_list = []
    current_index = 0

    while (current_index < len(data)):
        temp_list = []
        order = int(data[current_index].strip())
        if (order == 0 and current_index+2 > len(data)):
            break
        else:
            temp_list += [order]
            for i in range(1, order+1):
                temp_list += [data[i+current_index]]
            current_index += order+1
            digraph_list.append(Digraph(temp_list[0], temp_list[1:]))

    return digraph_list

def graph_display(data):
    for i in range(len(data)):
        for n in range(len(data[i].nodes)):
            print(str(n) + " : " + str(data[i].nodes[n].linked_indexes))

def file_reader_integrated_Q2():
    arc_str = ""
    order = None
    temp_list = []
    current_index = 0
    for line in sys.stdin:
        if (order == None):
            order = int(line.strip())
            current_index = 0
        elif current_index == order:
            temp_digraph = Digraph(order, temp_list)
            #temp_digraph.DFS()
            #temp_digraph.arc_DFS()
            temp_digraph.singleDFS()
            arc_str += temp_digraph.forward_arc + temp_digraph.cross_arc
            order = int(line.strip())
            current_index = 0
            temp_list = []
        else:
            temp_list += [line]
            current_index += 1
            
    print(arc_str)

def file_reader_integrated_Q3():
    depth_str = ""
    order = None
    temp_list = []
    current_index = 0
    for line in sys.stdin:
        if (order == None):
            order = int(line.strip())
            current_index = 0
        elif current_index == order:
            temp_digraph = Digraph(order, temp_list)
            temp_digraph.BFS()
            depth_str += str(temp_digraph.longest_path) + " " + str(temp_digraph.path_node) + "\n"
            order = int(line.strip())
            current_index = 0
            temp_list = []
        else:
            temp_list += [line]
            current_index += 1

            
    print(depth_str)

#=====================================
# A S S I G N M E N T  A N S W E R S
#=====================================

def question_one(data=[]):
    # returns a list of digraph objects
    if data == []:
        data = file_reader()
    digraph_str = ""
    current_index = 0

    while (current_index < len(data)):
        temp_list = []
        order = int(data[current_index].strip())
        if (order == 0 and current_index+2 > len(data)):
            break
        else:
            temp_list += [order]
            for i in range(1, order+1):
                temp_list += [data[i+current_index]]
            current_index += order+1
            temp_digraph = Digraph(temp_list[0], temp_list[1:])
            temp_digraph.delete_node()
            digraph_str += str(temp_digraph)
    digraph_str += "0\n"
    print(digraph_str)

def question_two(data=[]):
    if data == []:
        data = file_reader()
    arc_str = ""
    current_index = 0

    while (current_index < len(data)):
        temp_list = []
        order = int(data[current_index].strip())
        if (order == 0 and current_index+2 > len(data)):
            break
        else:
            temp_list += [order]
            for i in range(1, order+1):
                temp_list += [data[i+current_index]]
            current_index += order+1
            temp_digraph = Digraph(temp_list[0], temp_list[1:])
            temp_digraph.DFS()
            temp_digraph.arc_DFS()
            arc_str += temp_digraph.forward_arc + temp_digraph.cross_arc

    print(arc_str)

def question_three(data=[]):
    if data == []:
        data = file_reader()
    depth_str = ""
    current_index = 0

    while (current_index < len(data)):
        temp_list = []
        order = int(data[current_index].strip())
        if (order == 0 and current_index+2 > len(data)):
            break
        else:
            temp_list += [order]
            for i in range(1, order+1):
                temp_list += [data[i+current_index]]
            current_index += order+1
            temp_digraph = Digraph(temp_list[0], temp_list[1:])
            temp_digraph.BFS()
            depth_str += str(temp_digraph.longest_path) + " " + str(temp_digraph.path_node) + "\n"
    
    print(depth_str)
            

#==========================================
# N O D E  &  D I G R A P H  C L A S S E S
#==========================================

class Node:

    def __init__(self, location):
        self.location = location
        self.linked_indexes = []
        self.colour = "W"
        self.predecessor = -1;
        self.seen = 0
        self.done = -1
        self.depth = None
        self.source = None

    def remove_link(self, index):
        if index in self.linked_indexes:
            self.linked_indexes.remove(index)

    def update_chain(self, index):
        for x in range(len(self.linked_indexes)):
            if (self.linked_indexes[x] > index):
                self.linked_indexes[x] -= 1

    
class Digraph:

    def __init__(self, order, data):
        #Fundamental Attributes
        self.order = order
        self.nodes = []
        self.source_nodes = []
        self.global_time = 0
        self.stack = Stack()
        self.queue = Queue()
        self.longest_path = 0
        self.path_node = 0
        self.forward_arc = "\n"
        self.cross_arc = "\n"
        self.tree_arcs = []
        #Node Initialisation
        for i in range(len(data)):
            self.nodes.append(Node(i))
            if data[i] != "\n":
                string_data = data[i].strip().split(" ")
                for num in string_data:
                    try:
                        self.nodes[i].linked_indexes += [int(num)]
                    except:
                        pass

    def delete_node(self):
        delete_index = self.order - 3
        if (delete_index < 0):
            delete_index = 0
        self.nodes.pop(delete_index)
        for i in range(len(self.nodes)):
            self.nodes[i].remove_link(delete_index)
            self.nodes[i].update_chain(delete_index)
            if (i > delete_index):
                self.nodes[i].location -= 1
        self.order -= 1

    def recursiveDFS(self):
        #Traverse the nodes
        for s in range(len(self.nodes)):
            if (self.nodes[s].colour == "W"):
                self.recursiveDFSvisit(s)
    
    def recursiveDFSvisit(self, node_index):
        current_node = self.nodes[node_index]
        current_node.colour = "G"
        current_node.seen = self.global_time
        self.global_time += 1
        for link in self.nodes[current_node.location].linked_indexes:
            link_node = self.nodes[link]
            if link_node.colour == "W":
                link_node.predecessor = current_node
                self.recursiveDFSvisit(link)
        current_node.colour = "B"
        current_node.done = self.global_time
        self.global_time += 1

    def DFS(self):
        #Traverse the nodes
        for s in range(len(self.nodes)):
            self.stack.clear()
            if (self.nodes[s].colour == "W"):
                self.source_nodes += [s]
                self.DFSvisit(s)

    def DFSvisit(self, node_index):
        current_node = self.nodes[node_index]
        current_node.colour = "G"
        current_node.seen = self.global_time
        self.global_time += 1
        self.stack.push(current_node.location)

        while not self.stack.is_empty():
            u = self.stack.peek()
            stack_node = self.nodes[u]
            temp_links = self.nodes[u].linked_indexes
            has_white = False
            for link in temp_links:
                if self.nodes[link].colour == "W":
                    has_white = True
                    white_link = link
                    break
            if (has_white == True):
                current_link = self.nodes[white_link]
                current_link.colour = "G"
                current_link.predecessor = u
                current_link.seen = self.global_time
                self.global_time += 1
                self.stack.push(current_link.location)
            else:
                self.stack.pop()
                stack_node.colour = "B"
                stack_node.done = self.global_time
                self.global_time += 1

    def arc_DFS(self):
        self.reset_colour()
        #Traverse the nodes
        for s in range(len(self.nodes)):
            self.stack.clear()
            if (self.forward_arc != "\n" and self.cross_arc != "\n"):
                break
            elif (self.nodes[s].colour == "W"):
                self.source_nodes += [s]
                self.arc_DFSvisit(s)

    def arc_DFSvisit(self, node_index):

        current_node = self.nodes[node_index]
        current_node.colour = "G"
        self.stack.push(current_node.location)

        while not self.stack.is_empty():
            if (self.forward_arc != "\n" and self.cross_arc != "\n"):
                break
            u = self.stack.peek()
            stack_node = self.nodes[u]
            temp_links = self.nodes[u].linked_indexes
            has_white = False
            for link in temp_links:
                if self.nodes[link].colour == "W":
                    has_white = True
                    white_link = link
                    break
                else:
                    v = link
                    direct_relation1 = self.is_predecessor(u, v)
                    direct_relation2 = self.is_predecessor(v, u)
                    #checking for forward arc
                    if (self.nodes[u].seen < self.nodes[v].seen < self.nodes[v].done < self.nodes[u].done):
                        if (direct_relation1 == False and direct_relation2 == False) and (self.forward_arc == "\n"):
                            self.forward_arc = str(u) + "," + str(v) + "\n"
                    #checking for cross arc
                    if (self.nodes[v].seen < self.nodes[v].done < self.nodes[u].seen < self.nodes[u].done):
                        if (self.cross_arc == "\n"):
                            self.cross_arc = str(u) + "," + str(v) + "\n"

            if (has_white == True):
                current_link = self.nodes[white_link]
                current_link.colour = "G"
                self.stack.push(current_link.location)
            else:
                self.stack.pop()
                stack_node.colour = "B"

    def singleDFS(self):
        #Traverse the nodes
        for s in range(len(self.nodes)):
            self.stack.clear()
            if (self.forward_arc != "\n" and self.cross_arc != "\n"):
                return
            elif (self.nodes[s].colour == "W"):
                self.source_nodes += [s]
                self.singleDFSvisit(s)

    def singleDFSvisit(self, node_index):
        current_node = self.nodes[node_index]
        current_node.colour = "G"
        current_node.seen = self.global_time
        self.global_time += 1
        self.stack.push(current_node.location)

        while not self.stack.is_empty():
            if (self.forward_arc != "\n" and self.cross_arc != "\n"):
                return
            u = self.stack.peek()
            stack_node = self.nodes[u]
            temp_links = self.nodes[u].linked_indexes
            has_white = False
            for link in temp_links:
                if self.nodes[link].colour != "W":
                    v = link
                    direct_relation1 = self.is_predecessor(u, v)
                    direct_relation2 = self.is_predecessor(v, u)
                    #checking for forward arc
                    seen_u = self.nodes[u].seen
                    seen_v = self.nodes[v].seen
                    done_u = self.nodes[u].done
                    done_v = self.nodes[v].done

                    #print("Node-" + str(u) + str(v) + "SEEN: u-" + str(seen_u) + " v-" + str(seen_v))
                    #print("Node-" + str(u) + str(v) + "DONE: u-" + str(done_u) + " v-" + str(done_v) + "\n")

                    if ((seen_u < seen_v < done_v < done_u) or (seen_u < seen_v and (done_u == -1 and done_v >= 0))):
                        if (direct_relation1 == False and direct_relation2 == False) and (self.forward_arc == "\n"):
                            self.forward_arc = str(u) + "," + str(v) + "\n"
                    #checking for cross arc
                    if ((seen_u > seen_v) and ((done_u > done_v) or ((done_u == -1 and done_v != -1) or (done_u != -1 and done_v == -1)))):
                        if (self.cross_arc == "\n"):
                            self.cross_arc = str(u) + "," + str(v) + "\n"
                elif self.nodes[link].colour == "W":
                    has_white = True
                    white_link = link
                    break
            if (has_white == True):
                current_link = self.nodes[white_link]
                current_link.colour = "G"
                current_link.predecessor = u
                current_link.seen = self.global_time
                self.global_time += 1
                self.stack.push(current_link.location)
            else:
                self.stack.pop()
                stack_node.colour = "B"
                stack_node.done = self.global_time
                self.global_time += 1
                

    def reset_colour(self):
        for i in range(len(self.nodes)):
            self.nodes[i].colour = "W"

    def BFS(self):
        #Traverse the nodes
        self.BFSvisit(0)

    def BFSvisit(self, node_index):
        current_node = self.nodes[node_index]
        current_node.colour = "G"
        current_node.depth = 0
        self.queue.enqueue(current_node.location)
        while not self.queue.is_empty():
            u = self.queue.peek()
            queue_node = self.nodes[u]
            temp_links = queue_node.linked_indexes
            has_white = False
            for link in temp_links:
                if self.nodes[link].colour == "W":
                    has_white = True
                    white_link = link
                    break
            if (has_white == True):
                current_link = self.nodes[white_link]
                current_link.colour = "G"
                current_link.predecessor = u
                current_link.depth = (queue_node.depth) + 1
                if (current_link.depth > self.longest_path):
                    self.longest_path = current_link.depth
                    self.path_node = current_link.location
                elif (current_link.depth >= self.longest_path and current_link.location < self.path_node):
                    self.longest_path = current_link.depth
                    self.path_node = current_link.location
                self.queue.enqueue(current_link.location)
            else:
                self.queue.dequeue()
                queue_node.colour = "B"

    def find_source_node(self, index):
        current_node = self.nodes[index]
        current_pred = current_node.predecessor
        while current_pred != -1:
            current_node = self.nodes[current_pred]
            current_pred = current_node.predecessor
        return current_node.location

    def init_node_sources(self):
        for i in range(len(self.nodes)):
            self.nodes[i].source = self.find_source_node(i)

    def init_depth_list(self):
        depth_array = []
        for x in range(len(self.nodes)):
            depth_array += [self.nodes[x].depth]
        return depth_array

    def init_pred_list(self):
        pred_array = []
        for x in range(len(self.nodes)):
            pred_array += [self.nodes[x].predecessor]
        return pred_array

    def init_seen_list(self):
        seen_array = []
        for x in range(len(self.nodes)):
            seen_array += [self.nodes[x].seen]
        return seen_array

    def init_done_list(self):
        done_array = []
        for x in range(len(self.nodes)):
            done_array += [self.nodes[x].done]
        return done_array

    def generate_arcs(self):
        arc_list = []
        for index in range(len(self.nodes)):
            links = self.nodes[index].linked_indexes
            for link in links:
                arc_list += [[index, link]]
        return arc_list

    def __str__(self):
        returnStr = str(self.order) + "\n"
        for n in range(len(self.nodes)):
            if self.nodes[n].linked_indexes == []:
                returnStr += "\n"
            for i in range(len(self.nodes[n].linked_indexes)):
                if i != len(self.nodes[n].linked_indexes)-1:
                    returnStr += (str(self.nodes[n].linked_indexes[i]) + " ")
                else:
                    returnStr += (str(self.nodes[n].linked_indexes[i]) + "\n")
        return returnStr

    def simple_representation(self):
        returnStr = ""
        for n in range(len(self.nodes)):
            returnStr += (str(n) + " : " + str(self.nodes[n].linked_indexes) + "\n")
        print(returnStr)

    def generate_forward_arc(self):
        seen_array = self.init_seen_list()
        done_array = self.init_done_list()
        arc_list = self.generate_arcs()
        found_arc = False
        for i in range(len(arc_list)):
            u = arc_list[i][0]
            v = arc_list[i][1]
            direct_relation1 = self.is_predecessor(u, v)
            direct_relation2 = self.is_predecessor(v, u)
            if (((seen_array[u] < seen_array[v]) and (done_array[u] > done_array[v]))):
                if (direct_relation1 == False and direct_relation2 == False):
                    print(arc_list[i])
                    found_arc = True
                    break
        if found_arc == False:
            print("\n")

    def generate_cross_arc(self):
        seen_array = self.init_seen_list()
        done_array = self.init_done_list()
        arc_list = self.generate_arcs()
        found_arc = False
        for i in range(len(arc_list)):
            u = arc_list[i][0]
            v = arc_list[i][1]
            if ((seen_array[u] > seen_array[v]) and (done_array[u] > done_array[v])):
                print(arc_list[i])
                found_arc = True
                break
        if found_arc == False:
            print("\n")

    def generate_forward_and_cross(self):
        
        seen_array = self.init_seen_list()
        done_array = self.init_done_list()
        arc_list = self.generate_arcs()
        found_forward_arc = False
        found_cross_arc = False

        for i in range(len(arc_list)):
            u = arc_list[i][0]
            v = arc_list[i][1]
            direct_relation1 = self.is_predecessor(u, v)
            direct_relation2 = self.is_predecessor(v, u)
            #Checking for cross arc
            if ((seen_array[u] > seen_array[v]) and (done_array[u] > done_array[v])):
                if (found_cross_arc == False):
                    cross_arc = (str(arc_list[i][0]) + " " + str(arc_list[i][1]) + "\n")
                    found_cross_arc = True
            #Checking for forward arc
            elif (((seen_array[u] < seen_array[v]) and (done_array[u] > done_array[v]))):
                if (found_forward_arc == False):
                    if (direct_relation1 == False and direct_relation2 == False):
                        forward_arc = (str(arc_list[i][0]) + " " + str(arc_list[i][1]) + "\n")
                        found_forward_arc = True

        if found_cross_arc == False:
            cross_arc = "\n"
        if found_forward_arc == False:
            forward_arc = "\n"
        return forward_arc + cross_arc
    
    # O P T I M I S E D
    #------------------
    def generate_first_occurence(self):
        found_forward_arc = False
        found_cross_arc = False
        for index in range(len(self.nodes)):
            links = self.nodes[index].linked_indexes
            for link in links:
                arc_list = [index, link]
                u = arc_list[0]
                v = arc_list[1]
                direct_relation1 = self.is_predecessor(u, v)
                direct_relation2 = self.is_predecessor(v, u)
                #checking for cross arc
                if (self.nodes[v].seen < self.nodes[v].done < self.nodes[u].seen < self.nodes[u].done):
                    if (found_cross_arc == False):
                        if ([u, v] not in self.tree_arcs):
                            cross_arc = (str(u) + "," + str(v) + "\n")
                            found_cross_arc = True
                #Checking for forward arc
                elif (self.nodes[u].seen < self.nodes[v].seen < self.nodes[v].done < self.nodes[u].done):
                    if (found_forward_arc == False):
                        if (direct_relation1 == False and direct_relation2 == False) and ([u, v] not in self.tree_arcs):
                            forward_arc = (str(u) + "," + str(v) + "\n")
                            found_forward_arc = True
                elif (found_cross_arc == True and found_forward_arc == True):
                    return forward_arc + cross_arc
        if found_cross_arc == False:
            cross_arc = "\n"
        if found_forward_arc == False:
            forward_arc = "\n"
        return forward_arc + cross_arc

    def is_predecessor(self, u, v):
        if self.nodes[u].predecessor == v:
            return True
        return False
        

#======================================
# H E L P E R  C L A S S E S 
#======================================

class Stack:
    def __init__(self):
        self.items = []
    def is_empty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)                
    def pop(self):
        if self.is_empty():
            raise IndexError('ERROR: The stack is empty!')
        return self.items.pop()
    def peek(self):
        if self.is_empty():
            raise IndexError('ERROR: The stack is empty!')
        return self.items[len(self.items) - 1]
    def size(self):
        return len(self.items)        
    def __str__(self):
        return str(self.items)[:-1] + ' <-'
    def clear(self):
        self.items = []  

class Queue:
    def __init__(self):
        self.__items = []
    def is_empty(self):
        return self.__items == []
    def enqueue(self, item):
        self.__items.insert(0,item)
    def dequeue(self):
        if self.is_empty():
            raise IndexError('Error: The queue is empty!')
        return self.__items.pop() 
    def size(self):
        return len(self.__items)
    def peek(self):
        if self.is_empty():
            raise IndexError('Error: The queue is empty!')
        return self.__items[len(self.__items)-1]
    def __str__(self):
        return '-> |' + str(self.__items)[1:-1] + '| ->'

#==============================
# M A I N ( )  C O D E
#==============================

empty_graph = ["6\n", "\n", "\n", "\n", "\n", "\n", "\n", "0\n"]
a_list1 = ["4\n", "1 3\n", "2 3\n", "0\n", "\n", "3\n", "1 2\n", "\n", "1\n", "0\n"]
big_test2 = ["325\n", '143\n', '137\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '104\n', '\n', '54 320\n', '\n', '267\n', '211\n', '213\n', '\n', '64\n', '98\n', '\n', '39\n', '217\n', '\n', '62 89 315\n', '230\n', '\n', '\n', '\n', '130\n', '241\n', '56 184\n', '89 148 161 6\n', '\n', '\n', '302\n', '181\n', '63 197\n', '257\n', '\n', '78 126\n', '179 181\n', '\n', '224\n', '244\n', '126\n', '282\n', '\n', '279\n', '\n', '190 16\n', '\n', '\n', '273 283\n', '201\n', '35\n', '58\n', '41\n', '\n', '321\n', '\n', '\n', '20\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '130 42\n', '268\n', '\n', '\n', '\n', '16\n', '\n', '\n', '\n', '\n', '59\n', '\n', '\n', '\n', '100 124\n', '123 145\n', '96\n', '140\n', '\n', '235\n', '261\n', '\n', '\n', '\n', '\n', '164 32\n', '\n', '211 50 75\n', '214 251 54\n', '\n', '\n', '303 27 77\n', '223\n', '58\n', '\n', '157 210\n', '169 204 211 88\n', '302\n', '\n', '205\n', '18\n', '8\n', '\n', '311\n', '103\n', '\n', '152 259\n', '314\n', '\n', '191 252\n', '\n', '274\n', '161\n', '75\n', '281 308\n', '\n', '4 43\n', '\n', '113\n', '\n', '187 302\n', '\n', '100\n', '\n', '\n', '\n', '324\n', '\n', '273\n', '12\n', '\n', '\n', '\n', '299 65\n', '\n', '\n', '212\n', '318\n', '\n', '\n', '268\n', '301\n', '\n', '\n', '187\n', '178 29\n', '\n', '\n', '\n', '191 219 114\n', '179\n', '316 0\n', '\n', '\n', '174\n', '199\n', '\n', '263\n', '41\n', '116\n', '\n', '\n', '197\n', '194 49 70\n', '305\n', '\n', '\n', '64\n', '\n', '\n', '\n', '200\n', '\n', '66 169\n', '72 167\n', '121\n', '\n', '26\n', '\n', '\n', '\n', '202 150\n', '\n', '190\n', '300\n', '\n', '134\n', '31\n', '232\n', '108\n', '\n', '\n', '50\n', '52\n', '113\n', '216 259\n', '\n', '\n', '\n', '224 42\n', '\n', '76\n', '187\n', '251\n', '\n', '155\n', '\n', '62\n', '\n', '\n', '259\n', '166 172\n', '209\n', '\n', '\n', '\n', '\n', '\n', '\n', '312\n', '214\n', '\n', '260 263 112 170\n', '310\n', '240 163\n', '\n', '3\n', '\n', '319 143\n', '41\n', '\n', '\n', '\n', '\n', '15 231\n', '249 283\n', '\n', '\n', '296\n', '\n', '254\n', '216\n', '\n', '\n', '320 113\n', '259\n', '140\n', '18\n', '\n', '177\n', '\n', '\n', '\n', '\n', '\n', '\n', '89\n', '\n', '281 291\n', '\n', '90 217\n', '\n', '31\n', '\n', '90\n', '52 59\n', '38\n', '90\n', '175\n', '164\n', '58\n', '\n', '175 223\n', '104\n', '\n', '181\n', '122\n', '86\n', '75\n', '\n', '\n', '150\n', '\n', '\n', '\n', '34\n', '200\n', '227\n', '155\n', '\n', '158\n', '66 172 249\n', '113\n', '\n', '20 66 191\n', '\n', '\n', '\n', '\n', '\n', '143 236\n', '\n', '\n', '\n', '\n', '47\n', '85\n', '\n', '125\n', '\n', '\n', '93\n', '\n', '263\n', '\n', '\n']
big_test1 = ["20\n", '6 15\n', '4 5 8 11 12 17\n', '3 9 19\n', '2 4 18 19\n', '7 10 11 14 16\n', '0 7 13\n', '10 19\n', '9 19\n', '5 7 9 19\n', '\n', '3 4 16 17 19\n', '0 9 13 14 16\n', '0 7 9 14\n', '0 14\n', '5 7 10 17\n', '1 6 9 13 14\n', '3 7 8 10 17\n', '4 5 6 16\n', '4 6 7 12 13\n', '5 12 15\n']

file_reader_integrated_Q2() 

#=============================
# D I S C A R D E D  C O D E
#=============================
"""
    def BFS(self):
        #Traverse the nodes
        for s in range(len(self.nodes)):
            if (self.nodes[s].colour == "W"):
                self.BFSvisit(s)

    def BFSvisit(self, node_index):
        current_node = self.nodes[node_index]
        current_node.colour = "G"
        current_node.depth = 0
        self.queue.enqueue(current_node.location)
        while not self.queue.is_empty():
            u = self.queue.peek()
            queue_node = self.nodes[u]
            temp_links = queue_node.linked_indexes
            has_white = False
            for link in temp_links:
                if self.nodes[link].colour == "W":
                    has_white = True
                    white_link = link
                    break
            if (has_white == True):
                current_link = self.nodes[white_link]
                current_link.colour = "G"
                current_link.predecessor = u
                current_link.depth = (queue_node.depth) + 1
                self.queue.enqueue(current_link.location)
            else:
                self.queue.dequeue()
                queue_node.colour = "B"
"""
"""
def question_three(data=[]):
    if data == []:
        data = file_reader()
    depth_str = ""
    current_index = 0

    while (current_index < len(data)):
        temp_list = []
        order = int(data[current_index].strip())
        if (order == 0 and current_index+2 > len(data)):
            break
        else:
            temp_list += [order]
            for i in range(1, order+1):
                temp_list += [data[i+current_index]]
            current_index += order+1
            temp_digraph = Digraph(temp_list[0], temp_list[1:])
            temp_digraph.BFS()
            depth_list = temp_digraph.init_depth_list()
            #need to make it so that is checks if source node is 0
            longest_path = 0
            path_node = 0
            for x in range(len(depth_list)):
                if (depth_list[x] > longest_path and temp_digraph.find_source_node(x) == 0):
                    longest_path = depth_list[x]
                    path_node = x
            depth_str += str(longest_path) + " " + str(path_node) + "\n"
    
    print(depth_str)
"""