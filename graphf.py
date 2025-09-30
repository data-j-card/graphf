from neo4j import GraphDatabase
import os
import networkx as nx
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()  # loads .env file automatically

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASS"))

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection established.")

with driver.session(database="hfc1") as session:
    record = session.run("CALL db.schema.visualization()").single()
    nodes = record["nodes"]
    rels = record["relationships"]

# Build a schema graph
G = nx.DiGraph()

# Add nodes using their label name
for node in nodes:
    label = list(node.labels)[0]   # e.g. "AUTHOR"
    G.add_node(label)

# Add edges using relationship type
for rel in rels:
    start_label = list(rel.start_node.labels)[0]
    end_label   = list(rel.end_node.labels)[0]
    G.add_edge(start_label, end_label, type=rel.type)

# Plot
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)
node_size = [len(list(G.neighbors(n))) * 800 for n in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color="lightblue")
nx.draw_networkx_labels(G, pos, font_size=8, verticalalignment="bottom")
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "name"), font_size=6)
#nx.draw(G, pos, with_labels=True, node_size=2500, node_color="lightblue", font_size=10)
#nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d["type"] for u, v, d in G.edges(data=True)}, font_size=8)
plt.show()