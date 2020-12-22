For analysis of a network run gen_structure subgraph.elist

Following is result of python3 gen_structure facebook.elist
```
Number of nodes: 3213
Number of edges: 57832
Number of nodes which have degree=7: 107
Node id(s) with highest degree: 107
Approximate full diameter by sampling 10 nodes: 14
Approximate full diameter by sampling 100 nodes: 16
Approximate full diameter by sampling 1000 nodes: 16
Approximate full diameter (mean and variance): 15.3333, 0.8889
Approximate effective diameter by sampling 10 nodes: 6.7073
Approximate effective diameter by sampling 100 nodes: 6.6075
Approximate effective diameter by sampling 1000 nodes: 6.3327
Approximate effective diameter (mean and variance): 6.5492, 0.0251
Fraction of nodes in largest connected component: 0.9935
Number of edge bridges: 96
Number of articulation points: 50
Average clustering coefficient: 0.6000
Number of triads: 863556
Clustering coefficient of random node 3907: 0.7667
Number of triads random node 3114 participates: 285
Number of edges that participate in at least one triad: 57703
```

Following is result of python3 gen_structure amazon.elist
```
Number of nodes: 57168
Number of edges: 57378
Number of nodes which have degree=7: 415
Node id(s) with highest degree: 199628
Approximate full diameter by sampling 10 nodes: 73
Approximate full diameter by sampling 100 nodes: 110
Approximate full diameter by sampling 1000 nodes: 116
Approximate full diameter (mean and variance): 99.6667, 361.5556
Approximate effective diameter by sampling 10 nodes: 58.1005
Approximate effective diameter by sampling 100 nodes: 53.8186
Approximate effective diameter by sampling 1000 nodes: 53.3956
Approximate effective diameter (mean and variance): 55.1049, 4.5167
Fraction of nodes in largest connected component: 0.2444
Number of edge bridges: 31753
Number of articulation points: 23877
Average clustering coefficient: 0.1906
Number of triads: 10294
Clustering coefficient of random node 320508: 0.0000
Number of triads random node 120368 participates: 0
Number of edges that participate in at least one triad: 21819
```
For analysing any other network put its edge list file in subgraph folder
and run python3 gen_structure.py subgraph_name.elist