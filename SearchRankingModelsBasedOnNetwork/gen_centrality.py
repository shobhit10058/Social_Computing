#libraries requied for the task
import snap, os
from functools import cmp_to_key
from queue import Queue, LifoQueue

# This function creates the graph from 
# a text file fileName. 
# Here we need to give the relative path
def CreateGRaph(G, filePathName):
    f = open(filePathName, 'r')
    # Read until we reach at EOF
    while(True):
        s = f.readline()
        if(len(s) == 0):
            break
        # Split the read line to get the nodes having edges between them
        a,b = map(int, s.split())
        # We ensure that size of our is equal to
        # required for the storing the neighbours 
        # of all nodes
        while(len(G) <= max(a,b)):
            G.append([])
        # Since it is a undirected graph
        # so b is a neighbour of a and 
        # a is a neighbour of b
        G[a].append(b)
        G[b].append(a)

# The following funtion updates the betwenness centrality of the nodes
# based on the information collected by BFS and Brandes ALgorithm.
# This update happens in O(N + E). N-> number of nodes, E-> number of edges
def updateBetweenessCentrality(G, s, P, Source, shortest_paths, CB):
    D = [0.0 for i in range(len(G))]
    while(not(s.empty())):
        ls = s.get()
        for v in P[ls]:
            D[v] += ((shortest_paths[v] / shortest_paths[ls]) * (1.0 + D[ls] )) 
        if(ls != Source):
            CB[ls] += D[ls]

# Since we know the shortest distance of the source to any node, 
# so we can find the closeness centrality of the node, which this
# function does
def updateClosenessCentrality(G, CC, Source, shortest_len):
    d = 0
    for i in range(len(G)):
        d += shortest_len[i]
    CC[Source] = (len(G) - 1) / d

# This function runs the BFS traversal starting from a particular
# node, call it source. The BFS traversal helps us to get the 
# shortest distances between the source and other node. This could also 
# be used to get the number of shortest distance paths between the source 
# and any other node and the set of the nodes that comes in the shortest
# path of a node and the source. The following function runs in O(N + E). 
# N-> number of nodes and E-> number of edges
def Bfs(G, Source, CB, CC):
    # q -> The usual queue used in the BFS traversal, whose
    # front stores the node next to processed (This node is at the 
    # minimum distance from the source as compared to the other nodes
    # present in the queue).
    q = Queue()
    
    # s-> stack which help us process the nodes in increasing distance
    # from the source.
    s = LifoQueue()
    
    # We start by putting source in the queue
    q.put(Source)

    # The following list stores the neigbours of the node which
    # come in the shortest distance of the source
    # and the node
    P = [[] for _ in range(len(G))]

    # This just stores whether a node is present
    # taken in queue aleady or not
    tk = [False for i in range(len(G))]

    # This stores the shortest distance between source
    # and other nodes. The maximum distance between any pair
    # of nodes would be 1 less than the total number of nodes 
    # in the graph. But since the graph may be disconnected 
    # so it is initialised as total nodes. Thus the nodes which have
    # no path from source to them have total nodes distance stored here
    # other valid path lengths would always be less than this.
    shortest_len = [len(G) for _ in range(len(G))]

    # This stores the number of shortest paths between source and a
    # node. This is initialised as 0 and as we find a shortest path
    # we will increment this. Again the nodes having no path between 
    # them would have 0 shortest paths.
    shortest_paths = [0 for _ in range(len(G))]

    # The shortest distance of source from itself is
    # ofcourse 0 and shortest path from source to source is 1. 
    # But this is needed as with this we update the
    # shortest_len and shortest_paths for other nodes.
    shortest_len[Source] = 0
    shortest_paths[Source] = 1

    # Since the source is already in the queue so 
    # we mark it as included in the queue i.e tk[source] = True
    tk[Source] = True

    # We continue till the queue, q is not empty
    # In the following we have used the notion of visited
    # and taken in the queue for a node. A node is called 
    # visited when we actually extract it from the queue and
    # start seeing its neighbours.
    while(not (q.empty())):
        # we extract the front of queue
        fr = q.get()

        # and we put in the stack, since the queue 
        # process the nodes in the increasing distance 
        # from the source, so the stack has farthest node
        # from the source as its top.
        s.put(fr)

        # we now check the neighbours of front whether they are
        # already in the queue or not.
        for neigh in G[fr]:
            # If the neigbours are not in the queue, put them 
            # in the queue and marked them as taken in the queue.
            if(tk[neigh] == 0):
                q.put(neigh)
                tk[neigh] = True

            # Since the BFS traverses the nodes in the order of
            # increasing distance from the source, so when the neighbour 
            # is going to be put in the queue, we get its shortest distance as shortest
            # distance of front + 1, as any distance would be less than the 
            # distance with which we initialised the shortest_len for each node.
            # Also we get some number of shortest paths 
            # from source to these neighbours, these are the number of shortest 
            # paths from  source to front. Again, when this neigbour comes in the neighbours
            # of other nodes. If the distance of fr + 1 equals the shortest distance, then we
            # can increase the shortest number of paths and include this fr as well in the P[neigbour]
            # as it comes in the shortest path of source and neighbour. When the neighbour would be 
            # visited, then already we would have visited any nodes that are nearer to source as
            # compared to this neigbour which means we would have updated the shortest distance 
            # and covered all shortest paths as after this all nodes are at either equal or more distance
            # as compared to this neighbour, so can't come in the shortest path. 
            if(shortest_len[fr] + 1 < shortest_len[neigh]):
                shortest_len[neigh] = shortest_len[fr] + 1
                shortest_paths[neigh] = shortest_paths[fr]
                P[neigh].append(fr)
            elif(shortest_len[fr] + 1 == shortest_len[neigh]):
                shortest_paths[neigh] += shortest_paths[fr]
                P[neigh].append(fr)

    # Now using the information we collected, we update the betweenness centrality 
    # of all nodes based on Brandes Algorithm.
    updateBetweenessCentrality(G, s, P, Source, shortest_paths, CB) 

    # Using the shortest distance of the source and any node, 
    # we can now calculate the closeness centrality   
    updateClosenessCentrality(G, CC, Source, shortest_len)

# The function simply calls the function
# Bfs. This runs BFS traversal starting
# from every node.
def BfsForEverySource(G,CB, CC):
    for i in range(len(G)):
        Bfs(G, i, CB, CC)

# The Betweenness Centrality that we get from Brandes Algorithm 
# is not normalised, so this function simply normalises it
def NormaliseBetweenessCentrality(CB, n):
    for i in range(n):
        CB[i] /= ((n - 1) * (n - 2))
        CB[i] *= 2

# The following function follows the power iteration method 
# to calculate the PageRank of the nodes
def calPageRank(G):
    # The number of nodes to which we want to bias to
    S = int(((len(G) - 1) / 4)) + 1

    # The teleportation list is filled in such a way 
    # that it biases the ranks towards the nodes that are divisible
    # by 4 (These are the nodes we want to bias to) 
    TM = [0 if(i % 4) else 1 / S for i in range(len(G))]

    # The PR list stores the PageRank scores for each node
    # Following the algo, it is initialised as the teleportation list
    PR = [TM[i] for i in range(len(G))]

    # Damping factor, alpha = 0.8
    alpha = 0.8

    # The maximum difference between the next state 
    # and present state till which we continue the iteration
    # This value is chosen as we need to be precise till 
    # only 6 decimals.
    lim = 1e-6

    # We continue the iteration till the point when 
    # the difference between the next state and 
    # present state becomes less than the limit 
    # i.e, we continue till the convergence is reached.
    while(True):
        # s stores the sum of the next state scores of all nodes 
        s = 0

        # old_PR list stores the score of present state for each node
        old_PR = [PR[i] for i in range(len(G))]
        
        # PageRank Algo to update the states
        for node in range(len(G)):
            ps_R = 0
            for neigh in G[node]:
                # The description of algorithm in the slides stated to calculate the next state 
                # using only the present state, but in the slides, in the implementation shown, 
                # the present states of nodes were updated simulatenously and used to calculate the
                # the next states of other nodes. I have used the same here, but to use the described
                # algorithm uncomment the following line and comment the line below it. Testing it 
                # shown that both gave nearly the same scores.
                #ps_R += ((1 / len(G[neigh])) * old_PR[neigh])
                ps_R += ((1 / len(G[neigh])) * PR[neigh])
            PR[node] = (alpha * ps_R) + (1 - alpha) * TM[node]
            s += PR[node]
        
        # Normalising the new state scores, dividing each of them by their sum. 
        PR = [(PR[i] / s) for i in range(len(G))]
        
        # b-> bolean to check whether to break or not
        b = True
        
        # If the difference of next state and present state for 
        # each node is less than the limit, then break otherwise not
        for i in range(len(G)):
            if(abs(old_PR[i] - PR[i]) > lim):
                b = False
        
        if(b):
            break
    return PR

# This function simply takes a list for the nodes
# sorts the nodes according to it and then output them
# into a text file
def printInTxtFile(V, filePathName):
    l = [i for i in range(len(G))]
    l.sort(key=cmp_to_key(lambda item1, item2: V[item2] - V[item1]))
    f = open(filePathName, "w")
    for i in l:
        f.write(str(i) + "  " + "{:.6f}".format(V[i]) + "\n")

# G->Graph
# Here we have used the adjacency list representation of the graph   
# This stores the neighbours for each nodes. This takes 2 * No_of_Edges
# if the graph is undirected and that is the case here.
G = []
# Now we create the graph from the "facebook_combined.txt"
CreateGRaph(G, "facebook_combined.txt")

# Initializing the lists which we storing the centrality measures
# of different nodes
CB = [0 for _ in range(len(G))]
CC = [0 for _ in range(len(G))]
PR = [0 for _ in range(len(G))]

# Firstly we calculate the closeness and betweenCentrality measures
# for each node. The function below runs the BFS traversal from every node.
BfsForEverySource(G, CB, CC)

# The betweenness Centrality that we get by brandes algorithm is not normalised
# so we normalise it here.
NormaliseBetweenessCentrality(CB, len(G))

# Now we proceed to calculating the PageRank scores for each node
PR = calPageRank(G)

# making the centralities folder if not present
if not os.path.exists('centralities'):
    os.makedirs('centralities')

# output the centrality ranks in text files
printInTxtFile(CC, "centralities\\" + "closeness.txt")
printInTxtFile(CB, "centralities\\" + "betweenness.txt")
printInTxtFile(PR, "centralities\\" + "pagerank.txt")