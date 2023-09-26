import networkx as nx
import pandas as pd
from geopy.distance import geodesic
import logging
import requests
import json

# Phase 1: Graph Construction

# Task 1.1: Node Creation

def create_nodes(df, lat_col, lon_col):
    G = nx.Graph()
    
    for index, row in df.iterrows():
        lat = row[lat_col]
        lon = row[lon_col]
        
        G.add_node(index, latitude=lat, longitude=lon)
        
    return G

# Task 1.2: Edge Creation

def create_edges(G, df, lat_col, lon_col, threshold=1.0):
    nodes_data = [(idx, data['latitude'], data['longitude']) for idx, data in G.nodes(data=True)]
    
    for i, data_i in enumerate(nodes_data):
        for j, data_j in enumerate(nodes_data):
            if i != j:
                coord_i = (data_i[1], data_i[2])
                coord_j = (data_j[1], data_j[2])
                
                distance = geodesic(coord_i, coord_j).kilometers
                if distance <= threshold:
                    G.add_edge(data_i[0], data_j[0], weight=distance)
    
    return G

# Task 1.3: Get road information from OpenStreetMap API

def get_road_info(G):
    for edge in G.edges(data=True):
        node1 = G.nodes[edge[0]]
        node2 = G.nodes[edge[1]]
        
        lat1, lon1 = node1['latitude'], node1['longitude']
        lat2, lon2 = node2['latitude'], node2['longitude']
        
        url = f'http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false'
        
        try:
            response = requests.get(url)
            data = json.loads(response.text)
            
            if data['routes']:
                distance = data['routes'][0]['distance']
                duration = data['routes'][0]['duration']
                
                G[edge[0]][edge[1]]['distance'] = distance
                G[edge[0]][edge[1]]['duration'] = duration
        except:
            pass
    
    return G

# Main function to execute Phase 1
def main(csv, rows):
    df = pd.read_csv(csv)
    df = df.iloc[:rows]
    
    lat_col = 'lat'
    lon_col = 'lon'

    G = create_nodes(df, lat_col, lon_col)
    G = create_edges(G, df, lat_col, lon_col)
    G = get_road_info(G)

    return G

if __name__ == "__main__":
    main()

