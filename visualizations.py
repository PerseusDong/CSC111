import networkx as nx


def visualize_local_game_graph(
    G: nx.Graph,
    chosen_id: str,
    id_to_name: dict,
    max_depth: int = 2,
    max_nodes: int = 20,
    title: str = "Local Game Graph",
    figure_size=(12, 9),
    node_size=600,
    node_font_size=8,
    edge_alpha=0.3,
    layout="spring"
):
    """
    Visualize a local subgraph in the NetworkX graph, centered on 'chosen_id'.
    We'll do a BFS up to 'max_depth' layers, or until we reach 'max_nodes'.
    After BFS, we REMOVE any nodes that have no actual name in 'id_to_name'
    (meaning if id_to_name[node] == node or empty).
    Then we draw this subgraph with bigger figure size, bigger node size,
    and less edge alpha for clarity.

    :param G: the full NetworkX graph
    :param chosen_id: the item_id of the chosen game
    :param id_to_name: dict mapping item_id -> app_name
    :param max_depth: how many BFS layers from the chosen_id to include
    :param max_nodes: maximum number of nodes to BFS
    :param title: plot title
    :param figure_size: figure size (width, height)
    :param node_size: node size for drawing
    :param node_font_size: font size for node labels
    :param edge_alpha: alpha (transparency) for edges
    :param layout: one of ["spring", "kamada_kawai"] etc.
    """
    import matplotlib.pyplot as plt
    from collections import deque

    if chosen_id not in G:
        print(f"Chosen game ID '{chosen_id}' not in graph, cannot visualize local subgraph.")
        return

    visited = {chosen_id}
    queue = deque([(chosen_id, 0)])  # (node, depth)

    # BFS
    while queue and len(visited) < max_nodes:
        current, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for neighbor in G.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, depth + 1))
            if len(visited) >= max_nodes:
                break

    # Remove nodes that have no real name in id_to_name
    # For instance, if id_to_name.get(n) == n or blank, skip
    def has_valid_name(n):
        nm = id_to_name.get(n, "")
        # If nm is a string and different from n (the ID),
        # we assume it's a real name
        return isinstance(nm, str) and nm.strip() != "" and nm != n

    filtered = {n for n in visited if has_valid_name(n)}

    subG = G.subgraph(filtered).copy()
    print(f"Local subgraph for '{chosen_id}' has {len(subG)} valid named nodes, visualizing...")

    # Prepare labeling
    labels = {}
    for node in subG.nodes():
        game_name = id_to_name.get(node, node)
        labels[node] = game_name

    plt.figure(figsize=figure_size)
    plt.title(title + f" (centered on {id_to_name.get(chosen_id, chosen_id)})", fontsize=node_font_size + 2)

    # Choose layout
    if layout == "spring":
        pos = nx.spring_layout(subG, k=0.2, iterations=50)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(subG)
    else:
        pos = nx.spring_layout(subG)

    nx.draw(
        subG,
        pos,
        with_labels=False,
        node_size=node_size,
        edge_color="black",
        alpha=edge_alpha
    )

    nx.draw_networkx_labels(
        subG, pos, labels,
        font_size=node_font_size
    )

    plt.axis("off")
    plt.show()
