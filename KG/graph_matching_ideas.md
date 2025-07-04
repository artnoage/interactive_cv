# Advanced Graph Matching Ideas for Knowledge Graph Similarity

This document outlines mathematical approaches to find subgraphs that are structurally similar to a target graph (e.g., finding subgraphs of the academic KG that match config.json's structure).

## Core Problem Statement

Given:
- **Source Graph** G₁ (large academic knowledge graph)
- **Target Graph** G₂ (smaller reference graph like config.json)

Find: **Subgraph** S ⊆ G₁ such that d(S, G₂) is minimized, where d is a graph distance metric.

---

## 1. Spectral Graph Distance

### Theory
Graphs can be characterized by the eigenvalues of their Laplacian matrices. Similar graphs have similar spectral signatures.

### Implementation
```python
def spectral_distance(G1, G2):
    """Compare graphs using Laplacian eigenvalues"""
    L1 = nx.laplacian_matrix(G1).astype(float)
    L2 = nx.laplacian_matrix(G2).astype(float)
    
    # Get eigenvalues
    eigs1 = np.linalg.eigvals(L1.toarray())
    eigs2 = np.linalg.eigvals(L2.toarray())
    
    # Sort and pad to same length
    eigs1_sorted = np.sort(eigs1)
    eigs2_sorted = np.sort(eigs2)
    
    max_len = max(len(eigs1_sorted), len(eigs2_sorted))
    eigs1_padded = np.pad(eigs1_sorted, (0, max_len - len(eigs1_sorted)))
    eigs2_padded = np.pad(eigs2_sorted, (0, max_len - len(eigs2_sorted)))
    
    return np.linalg.norm(eigs1_padded - eigs2_padded)
```

### Advantages
- Captures global graph structure
- Invariant to node labeling
- Well-established theory

### Disadvantages
- Computationally expensive for large graphs
- May miss local structural features

---

## 2. Gromov-Hausdorff Distance

### Theory
Treats graphs as metric spaces using shortest path distances. Finds optimal correspondence between node sets.

### Implementation
```python
def gromov_hausdorff_distance(G1, G2):
    """Approximate GH distance between graphs"""
    # Convert graphs to distance matrices
    dist1 = dict(nx.all_pairs_shortest_path_length(G1))
    dist2 = dict(nx.all_pairs_shortest_path_length(G2))
    
    # Convert to numpy arrays
    nodes1 = list(G1.nodes())
    nodes2 = list(G2.nodes())
    
    D1 = np.array([[dist1[i].get(j, float('inf')) for j in nodes1] for i in nodes1])
    D2 = np.array([[dist2[i].get(j, float('inf')) for j in nodes2] for i in nodes2])
    
    # Use optimal transport to find best matching
    from scipy.optimize import linear_sum_assignment
    
    # Simplified version - actual GH distance is more complex
    if len(nodes1) <= len(nodes2):
        cost_matrix = compute_distortion_matrix(D1, D2)
        return linear_sum_assignment(cost_matrix)[1].sum()
    else:
        cost_matrix = compute_distortion_matrix(D2, D1)
        return linear_sum_assignment(cost_matrix)[1].sum()

def compute_distortion_matrix(D1, D2):
    """Compute distortion between distance matrices"""
    n1, n2 = D1.shape[0], D2.shape[0]
    cost = np.zeros((n1, n2))
    
    for i in range(n1):
        for j in range(n2):
            # Simplified distortion measure
            cost[i, j] = np.linalg.norm(D1[i, :] - D2[j, :])
    
    return cost
```

### Advantages
- Theoretically rigorous metric space approach
- Considers global geometric structure
- Scale-invariant

### Disadvantages
- Computationally intensive
- Complex to implement correctly
- May require approximations

---

## 3. Optimal Transport Between Graphs

### Theory
Model graphs as probability measures over feature spaces and use Wasserstein distance to compare them.

### Implementation
```python
def graph_optimal_transport_distance(G1, G2):
    """Use optimal transport to compare graph node distributions"""
    import ot
    
    # Extract node features
    features1 = extract_node_features(G1)
    features2 = extract_node_features(G2)
    
    # Create uniform distributions
    a = np.ones(len(features1)) / len(features1)
    b = np.ones(len(features2)) / len(features2)
    
    # Compute cost matrix (Euclidean distance between features)
    C = ot.dist(features1, features2, metric='euclidean')
    
    # Compute Wasserstein distance
    return ot.emd2(a, b, C)

def extract_node_features(G):
    """Extract structural features for each node"""
    features = []
    for node in G.nodes():
        feature_vector = [
            G.degree(node),                          # Degree
            nx.clustering(G, node),                  # Clustering coefficient
            nx.betweenness_centrality(G)[node],      # Betweenness centrality
            nx.closeness_centrality(G)[node],       # Closeness centrality
            nx.pagerank(G)[node],                    # PageRank
        ]
        features.append(feature_vector)
    
    return np.array(features)
```

### Advantages
- Handles graphs of different sizes naturally
- Incorporates node-level features
- Based on solid mathematical foundation

### Disadvantages
- Requires meaningful node features
- Feature extraction can be domain-specific
- Computational complexity

---

## 4. Graph Edit Distance Optimization

### Theory
Find minimum number of operations (node/edge insertions, deletions, substitutions) to transform one graph into another.

### Implementation
```python
def graph_edit_distance(G1, G2):
    """Compute graph edit distance using NetworkX"""
    # NetworkX implementation (can be slow for large graphs)
    return nx.graph_edit_distance(G1, G2)

def approximate_graph_edit_distance(G1, G2):
    """Faster approximation using structural differences"""
    # Size differences
    node_diff = abs(len(G1.nodes()) - len(G2.nodes()))
    edge_diff = abs(len(G1.edges()) - len(G2.edges()))
    
    # Degree sequence differences
    deg_seq1 = sorted([d for n, d in G1.degree()])
    deg_seq2 = sorted([d for n, d in G2.degree()])
    
    # Pad shorter sequence
    max_len = max(len(deg_seq1), len(deg_seq2))
    deg_seq1 += [0] * (max_len - len(deg_seq1))
    deg_seq2 += [0] * (max_len - len(deg_seq2))
    
    degree_diff = sum(abs(d1 - d2) for d1, d2 in zip(deg_seq1, deg_seq2))
    
    return node_diff + edge_diff + degree_diff
```

### Advantages
- Intuitive and interpretable
- Well-defined optimization problem
- Can handle node/edge attributes

### Disadvantages
- NP-hard problem
- Exponential complexity for exact solutions
- Approximations may miss optimal solutions

---

## 5. Network Alignment Metrics

### Theory
Compare structural properties and topological features of graphs.

### Implementation
```python
def structural_similarity_score(G1, G2):
    """Comprehensive structural similarity assessment"""
    scores = {}
    
    # 1. Degree Distribution Similarity
    deg_seq1 = [d for n, d in G1.degree()]
    deg_seq2 = [d for n, d in G2.degree()]
    scores['degree_ks'] = ks_test_similarity(deg_seq1, deg_seq2)
    
    # 2. Clustering Coefficient Similarity
    clustering1 = list(nx.clustering(G1).values())
    clustering2 = list(nx.clustering(G2).values())
    scores['clustering_similarity'] = 1 - abs(np.mean(clustering1) - np.mean(clustering2))
    
    # 3. Average Path Length Similarity
    try:
        apl1 = nx.average_shortest_path_length(G1)
        apl2 = nx.average_shortest_path_length(G2)
        scores['path_length_similarity'] = 1 - abs(apl1 - apl2) / max(apl1, apl2)
    except:
        scores['path_length_similarity'] = 0
    
    # 4. Diameter Similarity
    try:
        diam1 = nx.diameter(G1)
        diam2 = nx.diameter(G2)
        scores['diameter_similarity'] = 1 - abs(diam1 - diam2) / max(diam1, diam2)
    except:
        scores['diameter_similarity'] = 0
    
    # 5. Density Similarity
    density1 = nx.density(G1)
    density2 = nx.density(G2)
    scores['density_similarity'] = 1 - abs(density1 - density2)
    
    return scores

def ks_test_similarity(seq1, seq2):
    """Kolmogorov-Smirnov test for distribution similarity"""
    from scipy import stats
    statistic, p_value = stats.ks_2samp(seq1, seq2)
    return 1 - statistic  # Convert to similarity (higher = more similar)
```

### Advantages
- Multiple complementary measures
- Each metric captures different aspects
- Computationally efficient

### Disadvantages
- May require domain knowledge for weighting
- Some measures only work for connected graphs
- Aggregation of multiple scores can be arbitrary

---

## 6. Graph Neural Network Embeddings

### Theory
Use deep learning to embed graphs into vector spaces where similar graphs are close together.

### Implementation
```python
def gnn_graph_similarity(G1, G2):
    """Use Graph Neural Networks for graph-level embeddings"""
    # Requires: torch_geometric, dgl, or similar
    
    # Convert NetworkX graphs to GNN format
    data1 = networkx_to_torch_geometric(G1)
    data2 = networkx_to_torch_geometric(G2)
    
    # Use pre-trained graph encoder or train custom one
    model = GraphSAGE(input_dim=feature_dim, hidden_dim=64, output_dim=128)
    
    # Get graph-level embeddings
    embedding1 = model(data1).mean(dim=0)  # Graph-level pooling
    embedding2 = model(data2).mean(dim=0)
    
    # Compute cosine similarity
    return F.cosine_similarity(embedding1, embedding2, dim=0)

def networkx_to_torch_geometric(G):
    """Convert NetworkX graph to PyTorch Geometric format"""
    # Implementation depends on specific GNN library
    pass
```

### Advantages
- Can learn complex structural patterns
- End-to-end learnable
- State-of-the-art performance on many tasks

### Disadvantages
- Requires training data
- Black box approach
- Computational requirements for training

---

## 7. Motif-Based Similarity

### Theory
Compare graphs based on their subgraph motif patterns (triangles, stars, cliques, etc.).

### Implementation
```python
def motif_based_similarity(G1, G2):
    """Compare graphs using common motif patterns"""
    
    # Count motifs in both graphs
    motifs1 = count_motifs(G1)
    motifs2 = count_motifs(G2)
    
    # Compute similarity based on motif distributions
    all_motifs = set(motifs1.keys()) | set(motifs2.keys())
    
    vector1 = [motifs1.get(motif, 0) for motif in all_motifs]
    vector2 = [motifs2.get(motif, 0) for motif in all_motifs]
    
    # Normalize and compute cosine similarity
    vector1 = np.array(vector1) / np.linalg.norm(vector1)
    vector2 = np.array(vector2) / np.linalg.norm(vector2)
    
    return np.dot(vector1, vector2)

def count_motifs(G):
    """Count various motif patterns"""
    motifs = {}
    
    # Triangles
    motifs['triangles'] = sum(nx.triangles(G).values()) // 3
    
    # 4-cliques
    motifs['4_cliques'] = len([c for c in nx.find_cliques(G) if len(c) == 4])
    
    # Stars (nodes with degree > 2)
    motifs['stars'] = len([n for n, d in G.degree() if d > 2])
    
    # Paths of length 3
    motifs['3_paths'] = count_3_paths(G)
    
    return motifs

def count_3_paths(G):
    """Count paths of length 3"""
    count = 0
    for node in G.nodes():
        neighbors = list(G.neighbors(node))
        for i, n1 in enumerate(neighbors):
            for n2 in neighbors[i+1:]:
                if not G.has_edge(n1, n2):  # Ensure it's a path, not triangle
                    count += 1
    return count
```

### Advantages
- Captures local structural patterns
- Interpretable features
- Relatively efficient computation

### Disadvantages
- Limited to predefined motif types
- May miss larger structural patterns
- Sensitive to graph size

---

## 8. Combined Metric Framework

### Theory
Combine multiple distance metrics with learned or domain-specific weights.

### Implementation
```python
def combined_graph_distance(G1, G2, weights=None):
    """Combine multiple graph distance metrics"""
    
    if weights is None:
        weights = {
            'spectral': 0.3,
            'edit': 0.2, 
            'structural': 0.2,
            'motif': 0.2,
            'optimal_transport': 0.1
        }
    
    distances = {}
    
    # Compute individual distances
    distances['spectral'] = normalize_distance(spectral_distance(G1, G2))
    distances['edit'] = normalize_distance(approximate_graph_edit_distance(G1, G2))
    distances['motif'] = 1 - motif_based_similarity(G1, G2)  # Convert similarity to distance
    
    structural_scores = structural_similarity_score(G1, G2)
    distances['structural'] = 1 - np.mean(list(structural_scores.values()))
    
    try:
        distances['optimal_transport'] = normalize_distance(graph_optimal_transport_distance(G1, G2))
    except:
        distances['optimal_transport'] = 1.0  # Maximum distance if computation fails
    
    # Weighted combination
    combined_distance = sum(weights[metric] * distance 
                          for metric, distance in distances.items() 
                          if metric in weights)
    
    return combined_distance, distances

def normalize_distance(distance, max_dist=None):
    """Normalize distance to [0, 1] range"""
    if max_dist is None:
        max_dist = distance * 2  # Simple heuristic
    return min(distance / max_dist, 1.0)
```

### Advantages
- Leverages strengths of multiple approaches
- Robust to individual metric failures
- Customizable for specific domains

### Disadvantages
- Requires weight tuning
- More complex to implement and debug
- Computational overhead

---

## 9. Subgraph Enumeration Strategy

### Theory
Systematically generate candidate subgraphs and evaluate their similarity to the target.

### Implementation
```python
def find_best_matching_subgraph(source_graph, target_graph, distance_func):
    """Find subgraph of source that best matches target"""
    
    target_size = len(target_graph.nodes())
    target_edges = len(target_graph.edges())
    
    best_subgraph = None
    best_distance = float('inf')
    
    # Strategy 1: Random sampling
    for _ in range(1000):  # Sample 1000 random subgraphs
        subgraph = random_subgraph(source_graph, target_size)
        if is_valid_subgraph(subgraph, target_size, target_edges):
            distance = distance_func(subgraph, target_graph)
            if distance < best_distance:
                best_distance = distance
                best_subgraph = subgraph
    
    # Strategy 2: Node importance-based sampling
    importance_scores = compute_node_importance(source_graph)
    for _ in range(500):
        subgraph = importance_based_subgraph(source_graph, target_size, importance_scores)
        if is_valid_subgraph(subgraph, target_size, target_edges):
            distance = distance_func(subgraph, target_graph)
            if distance < best_distance:
                best_distance = distance
                best_subgraph = subgraph
    
    return best_subgraph, best_distance

def random_subgraph(G, size):
    """Generate random subgraph of specified size"""
    nodes = np.random.choice(list(G.nodes()), size=size, replace=False)
    return G.subgraph(nodes).copy()

def importance_based_subgraph(G, size, importance_scores):
    """Generate subgraph based on node importance"""
    # Sample nodes with probability proportional to importance
    nodes = list(G.nodes())
    probs = [importance_scores[node] for node in nodes]
    probs = np.array(probs) / np.sum(probs)
    
    selected = np.random.choice(nodes, size=size, replace=False, p=probs)
    return G.subgraph(selected).copy()

def compute_node_importance(G):
    """Compute importance scores for nodes"""
    centrality = nx.betweenness_centrality(G)
    pagerank = nx.pagerank(G)
    
    # Combine multiple centrality measures
    importance = {}
    for node in G.nodes():
        importance[node] = 0.5 * centrality[node] + 0.5 * pagerank[node]
    
    return importance

def is_valid_subgraph(subgraph, target_size, target_edges):
    """Check if subgraph meets basic criteria"""
    size_ok = len(subgraph.nodes()) == target_size
    connected = nx.is_connected(subgraph)
    edge_count_reasonable = abs(len(subgraph.edges()) - target_edges) <= target_edges * 0.5
    
    return size_ok and connected and edge_count_reasonable
```

### Advantages
- Systematic exploration of subgraph space
- Can incorporate domain knowledge through sampling strategies
- Guarantees to find a solution (if one exists)

### Disadvantages
- Exponential search space
- May require many samples for good solutions
- No guarantee of global optimum

---

## 10. Implementation Priority and Recommendations

### Recommended Implementation Order:

1. **Start with Structural Similarity** (easiest to implement and interpret)
2. **Add Spectral Distance** (good balance of theory and practicality)  
3. **Incorporate Motif Analysis** (captures local patterns)
4. **Combine with Random Subgraph Search** (find actual matching subgraphs)

### Complete Workflow:
```python
def find_similar_subgraph_pipeline(academic_kg, config_kg):
    """Complete pipeline for finding similar subgraphs"""
    
    # Step 1: Preprocess graphs
    academic_clean = preprocess_graph(academic_kg)
    config_clean = preprocess_graph(config_kg)
    
    # Step 2: Define combined distance metric
    def distance_metric(G1, G2):
        return combined_graph_distance(G1, G2)
    
    # Step 3: Find best matching subgraph
    best_subgraph, distance = find_best_matching_subgraph(
        academic_clean, config_clean, distance_metric
    )
    
    # Step 4: Analyze and report results
    analysis = analyze_subgraph_match(best_subgraph, config_clean)
    
    return best_subgraph, distance, analysis
```

This framework provides multiple mathematically rigorous approaches to graph matching, each with different strengths and computational requirements.