import sys, snap, os, shutil

def MoveFile(old_name, new_name):
    r_plt, r_tab = old_name[0:-4] + ".plt", old_name[0:-4] + ".tab"
    if(os.path.exists(r_plt)):
        os.remove(r_plt)
    if(os.path.exists(r_tab)):
        os.remove(r_tab) 
    shutil.move(old_name, new_name)

def MeanAndVariance(v1, v2, v3):
    mean  = (v1 + v2 + v3) / 3
    mean2 = (v1*v1 + v2*v2 + v3*v3) / 3
    variance = (mean2 - mean*mean)
    return [mean, variance]

Rnd = snap.TRnd(42)
Rnd.Randomize()
dirname = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists('plots'):
    os.makedirs('plots')
G = snap.LoadEdgeList(snap.PUNGraph,dirname + "\\subgraphs\\" + sys.argv[1], 0, 1)
print("Number of nodes:",G.GetNodes())
print("Number of edges:",G.GetEdges())
print("Number of nodes which have degree=7:",snap.CntDegNodes(G, 7))
print("Node id(s) with highest degree: ", end="")
InDegV = snap.TIntPrV()
snap.GetNodeInDegV(G, InDegV)
nodes = []
max_d = 0
for item in InDegV:
    max_d = max(max_d, item.GetVal2())
for item in InDegV:
    if(item.GetVal2() == max_d):
        nodes.append(item.GetVal1())
print(", ".join(list(map(str, sorted(nodes)))))

dFull_10   = snap.GetBfsFullDiam(G, 10, False)
dFull_100  = snap.GetBfsFullDiam(G, 100, False)
dFull_1000 = snap.GetBfsFullDiam(G, 1000, False)
m_dFull,v_dFull = map(float, MeanAndVariance(dFull_10, dFull_100, dFull_1000))
print("Approximate full diameter by sampling 10 nodes:",dFull_10)
print("Approximate full diameter by sampling 100 nodes:",dFull_100)
print("Approximate full diameter by sampling 1000 nodes:",dFull_1000)
print("Approximate full diameter (mean and variance): %.4f, %.4f" %(m_dFull,v_dFull))

dEff_10   = snap.GetBfsEffDiam(G, 10, False)
dEff_100  = snap.GetBfsEffDiam(G, 100, False)
dEff_1000 = snap.GetBfsEffDiam(G, 1000, False)
m_dEff,v_dEff = map(float, MeanAndVariance(dEff_10, dEff_100, dEff_1000))
print("Approximate effective diameter by sampling 10 nodes: %.4f" %dEff_10)
print("Approximate effective diameter by sampling 100 nodes: %.4f" %dEff_100)
print("Approximate effective diameter by sampling 1000 nodes: %.4f" %dEff_1000)
print("Approximate effective diameter (mean and variance): %.4f, %.4f" %(m_dEff,v_dEff))

print("Fraction of nodes in largest connected component: %.4f" %snap.GetMxSccSz(G))

EdgeV = snap.TIntPrV()
snap.GetEdgeBridges(G, EdgeV)
print("Number of edge bridges:", len(EdgeV))
ArtNIdV = snap.TIntV()
snap.GetArtPoints(G, ArtNIdV)
print("Number of articulation points:", len(ArtNIdV))
print("Average clustering coefficient: %.4f" %snap.GetClustCf (G, -1))
print("Number of triads:", snap.GetTriads(G, -1))
Ran_n = G.GetRndNId(Rnd)
print("Clustering coefficient of random node %d: %.4f" %(Ran_n, snap.GetNodeClustCf(G, Ran_n)))
Ran_n = G.GetRndNId(Rnd)
print("Number of triads random node %d participates: %d" %(Ran_n, snap.GetNodeTriads(G, Ran_n)))
print("Number of edges that participate in at least one triad:",snap.GetTriadEdges(G))

snap.PlotInDegDistr(G,"D_" + sys.argv[1], "Degree Distribution")
MoveFile(dirname + "\\inDeg.D_"  + sys.argv[1] + ".png", dirname + "\\plots\\" + "deg_dist_" + sys.argv[1] + ".png")

snap.PlotShortPathDistr(G, "S_" + sys.argv[1], "Shortest path Distribution")
MoveFile(dirname + "\\diam.S_" + sys.argv[1] + ".png", dirname + "\\plots\\" + "\\shortest_path_" + sys.argv[1] + ".png")

snap.PlotSccDistr(G, "C_" + sys.argv[1], "Component Size Distribution")
MoveFile(dirname + "\\scc.C_" + sys.argv[1] + ".png", dirname + "\\plots\\" + "\\connected_comp_" + sys.argv[1] + ".png")

snap.PlotClustCf(G, "C_" + sys.argv[1], "Clustering Coefficient Distribution")
MoveFile(dirname + "\\ccf.C_" + sys.argv[1] + ".png", dirname + "\\plots\\" + "\\clustering_coeff_" + sys.argv[1] + ".png")