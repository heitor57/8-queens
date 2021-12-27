
def bron_kerbosch(R, P, X, degrees, neighbors, maximal_cliques):
    if not P and not X:
        maximal_cliques.append(R)
        return

    vertexes = P.union(X)
    max_degree = degrees[next(iter(vertexes))]
    max_vertex = next(iter(vertexes))
    vertexes -= set([max_vertex])
    for vertex in vertexes:
        if degrees[vertex] > max_degree:
            max_degree = degrees[vertex]
            max_vertex = vertex
    candidates = P - neighbors[max_vertex]
    for candidate in candidates:
        bron_kerbosch(R.union(set([candidate])),
                      P.intersection(neighbors[candidate]),
                      X.intersection(neighbors[candidate]),
                      degrees, neighbors, maximal_cliques)
        P -= set([candidate])
        X = X.union(set([candidate]))
