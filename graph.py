from collections import defaultdict
# import matplotlib as plt

class Adjancency:
    '''
    The Adjancency class creates a dictionary for a directed tree or forest, an adjacency matrix, and the n^th-exponent of the adjacency matrices, representing the number of path with length n from a node to another.
    '''
    def __init__(self,vertices):
        self.vertices = vertices
        self.matrix = []
        for i in range(self.vertices):
            self.matrix.append([])
            for j in range(self.vertices):
                self.matrix[i].append(0)
        self.graph = defaultdict(list)
    
    def add_edge(self, u, v):
        self.graph[u].append(v)
    
    def generate_matrix(self):
        for i in range(self.vertices):
            for neighbor in self.graph[i]:
                self.matrix[i][neighbor] += 1
        return self.matrix

    # In both the functions dfs_color and is_cyclic, the color "white" is used to represent the initialized, unvisited vertices.
    # The color "grey" is used to represent the nodes visited but still in the searching stack with the root node at the bottom.
    # The color "black" is used to represent the nodes visited and are not in the stack. This means the paths from the root node to its maximal lengths is finished without encountering the same node from another root path.
    def dfs_color(self, u, color):
        color[u] = "grey"
        for v in self.graph[u]:
            if color[v] == "grey":
                return True
            elif color[v] == "white" and self.dfs_color(v, color):
                return True
        color[u] = "black"
        return False

    def is_cyclic(self):
        color = ["white"] * self.vertices
        for i in range(self.vertices):
            if color[i] == "white":
                if self.dfs_color(i, color):
                    return True
        return False

    def matrix_mul(self,iter):
        if not self.is_cyclic():
            matrix = self.generate_matrix()
            new_mat = matrix
            for degree in range(iter-1):
                result = []
                for i in range(self.vertices):
                    result.append([])
                    for j in range(self.vertices):
                        result[i].append(0)
                for i in range(len(matrix)):
                    for j in range(len(matrix[0])):
                        for k in range(len(matrix)):
                            result[i][j] += new_mat[i][k] * matrix[k][j]
                new_mat = result
            return new_mat
        else:
            return 'The graph cannot contain a cycle.'

class Graph:
    '''
    The Graph class generates a dictionary containing all edges and vertices in a directed tree or forest, and outputs the topological ordering of the graph by the shortest path.
    '''
    def __init__(self,vertices):
        self.graph = defaultdict(list)
        self.vertices = vertices
 
    def add_edge(self,u,v):
        self.graph[u].append(v)

    # The dfs_color function checks for backedges; in other words, if a node is already visited (colored 'grey') or it is not already visited, but starting from this vertex as root node, its DFS path will contain a revisited grey node.
    def dfs_color(self, u, color):
        color[u] = "grey"
        for v in self.graph[u]:
            if color[v] != "black" and (color[v] == "grey" or (color[v] == "white" and self.dfs_color(v, color))):
                return True
        color[u] = "black"
        return False
 
    # The is_cyclic function calls dfs_color.
    def is_cyclic(self):
        color = ["white"] * self.vertices
        for i in range(self.vertices):
            if color[i] == "white":
                if self.dfs_color(i, color):
                    return True
        return False

    # The dfs_stack function starts from a root node v, and put every neighbor of v (and every neighbor of neighbor) into the stack if it is not already in another path.
    # If a neighbor node is already visited, then it must be contained in another route from another root node.
    # This function, very similar to dfs_color function, appends vertices to a stack instead of checking.
    # I first realized DFS detection of backedges by using coloring of the nodes.
    # In the dfs_stack function, there is no need to color the nodes "black", meaning they are finished, because the topological_sort function checks for cycles using the is_cyclic function.
    def dfs_stack(self,v,color,stack):
        color[v] = "grey"
        for neighbor in self.graph[v]:
            if color[neighbor] != "grey":
                self.dfs_stack(neighbor,color,stack)
        stack.append(v)

    # The topological_sort function calls dfs_stack function and the is_cyclic function.
    def topological_sort(self):
        if not self.is_cyclic():
            color = ["white"]*self.vertices
            stack =[]
            # For each vertex in the graph, so the function also works for a forest.
            for i in range(self.vertices):
                if color[i] != "grey":
                    self.dfs_stack(i,color,stack)
            return stack[::-1]
        else:
            return "There is loop in the order of jobs given."

def gen_topological_order(job_number, job_data, paths_length):
    # Error checking
    result = dict()
    try:
        num_v = int(job_number)
    except Exception as e:
        result["message"] = "Number of jobs is not a positive number >=2."
        return result
    if num_v < 2:
        result["message"] = "Number of jobs is not >=2."
        return result
        
    try:
        paths_length = int(paths_length)
    except Exception as e:
        result["message"] = "Length of path is not an integer greater or equal to 1."
        return result
    if paths_length < 1:
        result["message"] = "Length of path is smaller than 1."
        return result

    message = None
    valid_list = []
    try:
        jobs=job_data.replace("\r", "\n").replace("\n\n", "\n").replace("\n", "$$").split("$$")
        jobs=list(map(str.strip, jobs))
        for job in jobs:
            if not job:
                continue
            job2=job.split(",")
            job2=list(map(str.strip,  job2))
            if len(job2) != 2 or int(job2[0]) >= num_v or int(job2[1]) >= num_v or int(job2[0]) < 0 or int(job2[1]) < 0:
                message = "{} is not the right format".format(job)
                break
            valid_list.append((int(job2[0]), int(job2[1])))
    except Exception as e:
        result["message"] = "job data is not conforming to the format defined: 0,1 or 1,2, and cannot be >= number of jobs:{}".format(e)
        return result
    if message:
        result["message"] = message
        return result
    if not valid_list:
        result["message"] = "No valid job data information to generate the topologic order"
        return result

    # Make the graph according to the inputs
    g = Graph(num_v)
    a = Adjancency(num_v)
    for job in valid_list:
        g.add_edge(job[0],job[1])
        a.add_edge(job[0],job[1])

    result["result"] = (g.topological_sort(), a.matrix_mul(paths_length))
    return result
