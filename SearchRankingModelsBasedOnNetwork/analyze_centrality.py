# libraries
import snap, os
from functools import cmp_to_key

# The function below takes the filePathName, Graph and type of centrality measure
# Type 1-> closeness centrality
# Type 2-> betweenness centrality
# Type 3-> pagerank centrality
def GetOverlap(filePathName, Graph, t):
    # l is here the final ranking of the nodes
    # Intially, we just put all the nodes in this
    # and afterwards we sort it
    l = [i for i in range(Graph.GetNodes())]

    # The reference vector whose information is used to sort l
    ref_vect = [0 for i in range(Graph.GetNodes())]

    # if Type 1, then fill ref_vect with closeness centrality measure
    if(t == 1):
        for NI in Graph.Nodes():
            ref_vect[NI.GetId()] = snap.GetClosenessCentr(Graph, NI.GetId())

    # if Type 2, then fill ref_vect with betweenness centrality measure
    if(t == 2):
        Nodes = snap.TIntFltH()
        Edges = snap.TIntPrFltH()

        # Setting NodeFrac parameter as 0.8 as instructed
        snap.GetBetweennessCentr(Graph, Nodes, Edges, 0.8)
        for node in Nodes:
            ref_vect[node] = Nodes[node]

    # if Type 3, then fill ref_vect with PageRank scores
    if(t == 3):
        PRankH = snap.TIntFltH()

        # Taking the limit as 1e-6 as used in gen_centrality.py
        snap.GetPageRank(Graph, PRankH, 0.8, 1e-6, 100)
        for item in PRankH:
            ref_vect[item] = PRankH[item]

    # Now we sort l using the ref_vect
    l.sort(key=cmp_to_key(lambda item1, item2: ref_vect[item2] - ref_vect[item1]))
    
    # make a set containing top 100 nodes of l
    S1 = set(l[:100])

    # make another set containing top 100 nodes from the text files
    S2 = set()
    f = open(filePathName, 'r')
    for _ in range(100):
        s = f.readline()
        a,b = s.split()
        S2.add(int(a))

    # return the number of overlaps in S1 and S2
    return len(S1.intersection(S2))

# Graph -> Graph of the facebook network
Graph = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1)

# Printing the overlaps 
print("#overlaps for Closeness Centrality:", GetOverlap("centralities\\" + "closeness.txt", Graph, 1))

print("#overlaps for Betweenness Centrality:", GetOverlap("centralities\\" + "betweenness.txt", Graph, 2))

print("#overlaps for PageRank Centrality:", GetOverlap("centralities\\" + "pagerank.txt", Graph, 3))
