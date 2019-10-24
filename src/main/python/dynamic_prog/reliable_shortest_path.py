"""We are given a graph G with lengths on the edges, along with two nodes s and t and an integer k, 
and we want the shortest path from s to t that uses at most k edges.
Sub-problem definition:
    for each vertex v and each integer i ≤ k, 
    dist(v, i) to be the length of the shortest path 
    from s to v that uses i edges. 
    The starting values dist(v, 0) are ∞ for all vertices except s, 
    for which it is 0. 
    The general update equation is

    dist(v, i) = min {dist(u, i − 1) + l(u, v)}
    
    where (u,v) ∈ E
"""



