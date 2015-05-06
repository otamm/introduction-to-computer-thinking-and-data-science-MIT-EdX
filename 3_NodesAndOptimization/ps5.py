# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

# Problem 1:
# Create a class to represent a weighted edge and another to represent a weighted digraph.
#

class WeightedEdge(Edge):
    """
    Provides a WeightedEdge which inherits from regular Edge but also affected by a weight attribute.
    """

    def __init__(self, src, dest, totalD, outdoorD):
        self.src = src
        self.dest = dest
        self.totalD = totalD
        self.outdoorD = outdoorD

    def getTotalDistance(self):
        return self.totalD

    def getOutdoorDistance(self):
        return self.outdoorD

    def __str__(self):
        return self.src.getName() + "->" + self.dest.getName() + " (" + str(self.getTotalDistance()) + "," + str(self.getOutdoorDistance()) + ")"

class WeightedDigraph(Digraph):
    """
    Creates a Digraph which takes the weights of its nodes' edges into account.
    """

    def __init__(self):
        self.nodes = set([])
        self.edges = {}

    def addNode(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []

    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append([Node(str(dest)), (edge.getTotalDistance(), edge.getOutdoorDistance()) ] )

    def childrenOf(self, node):
        nodes = []
        for i in self.edges[Node(str(node))]:
            nodes.append(int(str(i[0])))
        return nodes

    def getDistances(self, node, dest):
        for destination in self.edges[Node(str(node))]:
            #print destination
            if str(destination[0]) == str(dest):
                #print destination
                return (destination[1][0], destination[1][1])
        raise ValueError('Nodes are not related.')

    def __str__(self):
        res = ''
        for node in self.edges:
            for dists in self.edges[node]:
                #res += k.getName() + "->" + self.edges[k][0].getName() + " (" + str(float(self.edges[str(k)][1][0])) + ", " + str(float(self.edges[str(k)][1][0])) + ")\n"
                res += "{0}->{1} ({2}, {3})\n".format(node, dists[0], float(dists[1][0]), float(dists[1][1]))
        return res[:-1]

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    # TODO
    print "Loading map from file..."

    graph = WeightedDigraph()

    # 'with open()' closes the file when the block ends.
    with open(mapFilename,"rU") as mapFile:
        for thisline in mapFile.readlines():
            line = thisline.split()
            nodeA = Node(line[0])
            nodeB = Node(line[1])
            try:
                graph.addNode(nodeA)
            except ValueError:
                pass
            try:
                graph.addNode(nodeB)
            except ValueError:
                pass
            edge = WeightedEdge(nodeA, nodeB, int(line[2]), int(line[3]))
            graph.addEdge(edge)
        return graph
        

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#
# Generate all possible combinations.
# Select all combinations in which the start node's path finishes in the specific end node.
# Choose solution that best fit the constraints.

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    totalDist = 0
    totalOutDist = 0
    paths = []
    fit_paths = []
    path = [start]

# Helper method intended to use with the method above.

def getAllNodePossibilities(node, graph, endNode):
    graph.childrenOf(node)
#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #global total_paths
    #total_paths = []
    global tpaths
    tpaths = []
    tries = 0
    a = dfsShortest(digraph, int(start), int(end), [], None, maxTotalDist, maxDistOutdoors, 1000000, 100000, [])
    #print a
    #print tpaths
    ##print "IDSJISJISJ"
    if (tpaths != []):
        best = []
        bb = 1000000000
        for path in tpaths:
            if path[1] <= bb:
                bb = path[1]
                best = path[0]
        #print tpaths
        print best
        formatted = []
        for b in best:
            formatted.append(str(b))
        return formatted
    else:
        raise ValueError('No existing path satisfies these constraints.')


def dfsShortest(graph, start, end, path, shortest, maxTotalDist, maxDistOutdoors, smDist, smOut, paths):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    path = path + [start]
    #print 'Current dfs path:', path
    if start == end:
        #print "a"
        a = isValid(path, maxTotalDist, maxDistOutdoors, graph, end)
        if (a):
            tpaths.append(a)
        return path
    for node in graph.childrenOf(start):
        if node not in path: #avoid cycles
            if shortest == None or len(path)<len(shortest):
                newPath = dfsShortest(graph,node,end,path,shortest,maxTotalDist, maxDistOutdoors, smDist, smOut, paths)
                if newPath != None:
                    a = isValid(path, maxTotalDist, maxDistOutdoors, graph, end)
                    if (a):
                        tpaths.append(a)
                    shortest = newPath
        else:
            pass
    #print "b"
    a = isValid(path, maxTotalDist, maxDistOutdoors, graph, end)
    if (a):
        #print "AAAAFKSFIDJFH"
        #print a
        tpaths.append(a)
        #print tpaths
    #else:
        #print "jfosjsojds"

    return shortest

def isValid(path, maxTotal, maxOut, graph, end):
    #print "AAAA"
    totalDist = 0
    totalOut = 0
    #if path[-1] == end:
    for n in range(1, len(path)):
        #print "H"
        #print path[n - 1]
        #print path[n]
        nDists = graph.getDistances(path[n - 1], path[n])
        #print nDists
        totalDist += int(str(nDists[0]))
        totalOut += int(str(nDists[1]))
        if n == len(path) - 1:
            break
    if (totalDist <= maxTotal and totalOut <= maxOut):
        #print "PATH"
        #print path[len(path) - 1]
        #print "CHILDREN"
        #print graph.childrenOf(path[0])
        #print (path, totalDist + totalOut)
        if end in path:
            return (path, totalDist)
    #else:
    return False

# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
#     Test cases
     mitMap = load_map("mit_map.txt")
     print isinstance(mitMap, Digraph)
     print isinstance(mitMap, WeightedDigraph)
     print 'nodes', mitMap.nodes
     print 'edges', mitMap.edges


     LARGE_DIST = 1000000

#     Test case 1
     print "---------------"
     print "Test case 1:"
     print "Find the shortest-path from Building 32 to 56"
     expectedPath1 = ['32', '56']
     brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
     dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
     print "Expected: ", expectedPath1
     print "Brute-force: ", brutePath1
     print "DFS: ", dfsPath1
     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

#     Test case 2
     print "---------------"
     print "Test case 2:"
     print "Find the shortest-path from Building 32 to 56 without going outdoors"
     expectedPath2 = ['32', '36', '26', '16', '56']
     brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
     dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
     print "Expected: ", expectedPath2
     print "Brute-force: ", brutePath2
     print "DFS: ", dfsPath2
     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
     print "---------------"
     print "Test case 3:"
     print "Find the shortest-path from Building 2 to 9"
     expectedPath3 = ['2', '3', '7', '9']
     brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
     dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
     print "Expected: ", expectedPath3
     print "Brute-force: ", brutePath3
     print "DFS: ", dfsPath3
     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
     print "---------------"
     print "Test case 4:"
     print "Find the shortest-path from Building 2 to 9 without going outdoors"
     expectedPath4 = ['2', '4', '10', '13', '9']
     brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
     dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
     print "Expected: ", expectedPath4
     print "Brute-force: ", brutePath4
     print "DFS: ", dfsPath4
     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
     print "---------------"
     print "Test case 5:"
     print "Find the shortest-path from Building 1 to 32"
     expectedPath5 = ['1', '4', '12', '32']
     brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
     dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
     print "Expected: ", expectedPath5
     print "Brute-force: ", brutePath5
     print "DFS: ", dfsPath5
     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
     print "---------------"
     print "Test case 6:"
     print "Find the shortest-path from Building 1 to 32 without going outdoors"
     expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
     brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
     dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
     print "Expected: ", expectedPath6
     print "Brute-force: ", brutePath6
     print "DFS: ", dfsPath6
     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
     print "---------------"
     print "Test case 7:"
     print "Find the shortest-path from Building 8 to 50 without going outdoors"
     bruteRaisedErr = 'No'
     dfsRaisedErr = 'No'
     try:
         bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
     except ValueError:
         bruteRaisedErr = 'Yes'
    
     try:
         directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
     except ValueError:
         dfsRaisedErr = 'Yes'
    
     print "Expected: No such path! Should throw a value error."
     print "Did brute force search raise an error?", bruteRaisedErr
     print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
     print "---------------"
     print "Test case 8:"
     print "Find the shortest-path from Building 10 to 32 without walking"
     print "more than 100 meters in total"
     bruteRaisedErr = 'No'
     dfsRaisedErr = 'No'
     try:
         bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
     except ValueError:
         bruteRaisedErr = 'Yes'
    
     try:
         directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
     except ValueError:
         dfsRaisedErr = 'Yes'
    
     print "Expected: No such path! Should throw a value error."
     print "Did brute force search raise an error?", bruteRaisedErr
     print "Did DFS search raise an error?", dfsRaisedErr

map1 = load_map("mit_map.txt")
directedDFS(map1, "3", "1", 50, 20)
