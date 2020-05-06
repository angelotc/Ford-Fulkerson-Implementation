
import sys
import os
import pydot

class FlowNetwork(object):
    def __init__(self, num_vertices):
        '''
        Initialize graph using an integer for the number of vertices and an edge list.
        '''
        self.num_vertices = int(num_vertices)
        self.edges = {}
 
    def add_edge(self, u, v, w=0):
        if u == v:
            return
        if u not in self.edges:
            self.edges[u] = {}
        if v not in self.edges[u]:
            self.edges[u][v] = 0
        self.edges[u][v] += w

    def find_path(self, source, target, visited):
        visited.add(source)
        if source not in self.edges:
            return None
        for other in self.edges[source]:
            if other in visited:
                continue
            weight = self.edges[source][other]
            if weight <= 0:
                continue
            if other != target:
                result = self.find_path(other, target, visited)
                if result is not None:
                    return [source,] + result
            else:
                return [source, target]
        return None
 
    def max_flow(self, source, target):
        '''
        Ford-Fulkerson algorithm to find max flow. 
        '''
        flow = 0
        path = self.find_path(source, target, set())
        while path is not None:
            min_w = -1
            for i in range(len(path)-1):
                s = path[i]
                t = path[i+1]
                w = self.edges[s][t]
                if min_w < 0:
                    min_w = w
                else:
                    min_w = min(w, min_w)
            for i in range(len(path)-1):
                s = path[i]
                t = path[i+1]
                w = self.edges[s][t]
                self.edges[s][t] -= min_w
                self.add_edge(t,s,min_w)
            flow += min_w
            path = self.find_path(source, target, set())

        return flow

if __name__ == '__main__' :
    
    cur_dir = os.path.abspath(os.getcwd())
    input_path = os.path.abspath((os.path.join(cur_dir,'input')))
    output_path = os.path.abspath((os.path.join(cur_dir,'output')))
    
    with open(  os.path.join(input_path, "graph1.txt")) as f:
        
        # Gather number of instances
        num = int(f.readline())
        counts = []
        # Gather edge per instance 
        # Sample line of "1 2 3" : an edge from node 1 to node 2 with a weight of 3
        for i in range(num):
            graph = pydot.Dot(graph_type='digraph', 
                            rankdir="LR")
            intervals = []
            take_input = f.readline()
            take_input = take_input.split(" ")
            num_vertices = int(take_input[0])
            num_edges = int(take_input[1])

            fn = FlowNetwork(num_vertices)

            n_dict = {}
            for x in range(1,num_vertices+1):
                n_dict[str(x)] = pydot.Node(str(x))

    
            for j in range(num_edges):
                inp = f.readline()
                inp = inp.split(" ")

                source = str(inp[0])
                destination = str(inp[1])
                capacity = int(inp[2])
                if source == destination:
                    flag = True
                fn.add_edge(source, destination, capacity)

                color = "blue"
            # After gathering, sort them in ascending order by finish time
                r_edge = pydot.Edge(
                        n_dict[source],
                        n_dict[destination],
                        label=str(capacity),
                        labelfontcolor="#009933",
                        fontsize="10.0",
                        color=color)
                #r_edge.obj_dict['attributes']['minlen'] = "1"
                graph.add_edge(r_edge)

                

            val = fn.max_flow('1',str(num_vertices))
            counts.append(val)
            graph.write_png(f'{i}.png')
        for cnt in counts:
            sys.stdout.write(str(cnt) +'\n')