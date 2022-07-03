
from locale import currency
from tracemalloc import start
from turtle import st
import sys
import serial

#serial1 = serial.Serial('/dev/ttyACM0', 9600)
if __name__ == '__main__':
    serial1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    serial1.reset_input_buffer()


class Node:
    def __init__(self, label, childs, parent, cost_from_root):
        self.label = label
        self.childs = childs
        self.parent = parent
        self.cost_from_root = cost_from_root



def sort(arr):
    n = len(arr)
  
    # Traverse through all array elements
    for i in range(n):
        swapped = False
 
        # Last i elements are already
        #  in place
        for j in range(0, n-i-1):
  
            # traverse the array from 0 to
            # n-i-1. Swap if the element
            # found is greater than the
            # next element
            if arr[j].cost_from_root > arr[j+1].cost_from_root :
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
 
        # IF no two elements were swapped
        # by inner loop, then break
        if swapped == False:
            break
 
def is_in(label, list_of_nodes):
    for i in range(len(list_of_nodes)):
        if ( label == list_of_nodes[i].label):
            return True, list_of_nodes[i]
    
    return False, 0


def FindPath(start, goal, graph):
    path = []
    openList = []
    closedList= []
    openList.append(start)
    
    while True:
        sort(openList)
        if (len(openList) > 0):
            current = openList[0]
        else:
            return []

        if ( current.label == goal.label):
            while(current.parent != None):
                path.append(current.label)
                current = current.parent
            return list(reversed(path))

        for node_info in current.childs:
            new_node_label = node_info[0]
            new_node_cost_from_root = current.cost_from_root + node_info[1]

            try:
                if new_node_label == current.parent.label:
                    continue
            except:
                pass
            # check if current in closed list
            found_in_closed, closed_node = is_in(new_node_label, closedList)
            # check if current is alredy in open list
            found_in_opened, opened_node = is_in(new_node_label, openList)

            if (found_in_closed):
                if new_node_cost_from_root >= closed_node.cost_from_root:
                    continue
                
                closedList.remove(closed_node)
                closed_node.cost_from_root = new_node_cost_from_root
                closed_node.parent = current
                openList.append(closed_node)

            elif(found_in_opened):
                if new_node_cost_from_root >= opened_node.cost_from_root:
                    continue
                
                opened_node.cost_from_root = new_node_cost_from_root
                opened_node.parent = current

            else:
                new_node = Node(new_node_label, graph[new_node_label], current, new_node_cost_from_root)
                openList.append(new_node)
        openList.remove(current)
        closedList.append(current)
        


graph = {'S': [('N', 1)],
         'N': [('M', 1)],
         'M': [('N', 1), ('A', 1), ('L', 1)],
         'L': [('M', 1), ('X', 1), ('I', 1)],
         'A': [('M', 1), ('B',1)],
         'B': [('A', 1), ('C',1)],
         'C': [('B', 1), ('N',1)],
         'X': [('L', 1), ('Y',1)],
         'Y': [('X', 1), ('Z',1)],
         'Z': [('Y', 1), ('N',1)],
         'I': [('L', 1), ('J',1)],
         'J': [('I', 1), ('K',1)],
         'K': [('J', 1), ('N',1)] }


s = 'S'
args = sys.argv
pos  = args[1]  #position
raf  = args[2]  # RAF

start = Node(s, graph[s], None, 0)
goal  = Node(pos, graph[pos], None, None)
path  = FindPath(start, goal, graph)

data = ''.join(map(str,path))
data = data+"\n"

b_data = bytes(data, 'utf-8')
serial1.write(b_data)
