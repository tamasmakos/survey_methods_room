import pandas as pd
import osmnx as ox
import networkx as nx
import requests
from collections import Counter

def data_enrichment_process(csv_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Step 1: Geocode the address column to get latitude and longitude
    def geocode(address):
        url = 'https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates'
        params = {'f': 'json', 'singleLine': address, 'outFields': 'Match_addr,Addr_type'}
        r = requests.get(url, params=params)
        if r.json()['candidates']:
            return r.json()['candidates'][0]['location']
        else:
            return None

    df['geocode'] = df['address'].apply(geocode)
    df['lon'] = df['geocode'].apply(lambda x: x['x'] if x else None)
    df['lat'] = df['geocode'].apply(lambda x: x['y'] if x else None)
    
    # Step 2: Enrich address with amenities information
    excluded_amenities = ['bench', 'waste_basket', 'bicycle_parking', 'drinking_water', 'recycling', 'telephone', 'post_box']

    def get_amenities(lat, lon, dist=200):
        url = f'https://overpass-api.de/api/interpreter?data=[out:json];node(around:{dist}, {lat}, {lon});out;'
        response = requests.get(url)
        amenities = []
        for node in response.json().get('elements', []):
            if 'tags' in node and 'amenity' in node['tags'] and node['tags']['amenity'] not in excluded_amenities:
                amenities.append(node['tags']['amenity'])
        return dict(Counter(amenities))

    amenities_data = df.apply(lambda x: get_amenities(x['lat'], x['lon']), axis=1)
    amenities_df = pd.DataFrame.from_records(amenities_data)
    amenities_df.index = df.index
    df = pd.concat([df, amenities_df], axis=1)
    
    # Step 3: Append network stats to the DataFrame
    def append_network_stats(row, dist=200):
        lat, lon = row['lat'], row['lon']
        if lat and lon:
            try:
                G = ox.graph_from_point((lat, lon), dist=dist, network_type='walk')
                nearest_node = ox.distance.nearest_nodes(G, Y=lat, X=lon)
                stats = ox.basic_stats(G, clean_int_tol=15)
                stats.update({
                    'degree_centrality': nx.degree_centrality(G).get(nearest_node, 0),
                    'closeness_centrality': nx.closeness_centrality(G).get(nearest_node, 0),
                    'betweenness_centrality': nx.betweenness_centrality(G).get(nearest_node, 0),
                    'eigenvector_centrality': nx.eigenvector_centrality(nx.DiGraph(G), max_iter=5000).get(nearest_node, 0),
                    'clustering_coefficient': nx.clustering(nx.DiGraph(G)).get(nearest_node, 0),
                    'pagerank': nx.pagerank(G).get(nearest_node, 0)
                })
                return stats
            except Exception as e:
                print(f"Error processing lat: {lat}, lon: {lon} - {e}")
        return {}

    network_stats = df.apply(append_network_stats, axis=1)
    network_stats_df = pd.DataFrame(list(network_stats))
    enriched_data = pd.concat([df, network_stats_df], axis=1)
    
    return enriched_data

enriched_data = data_enrichment_process('/Users/tamasmakos/dev/survey_methods_room/data_files/address.csv')

# Write to file
enriched_data.to_csv('/Users/tamasmakos/dev/survey_methods_room/data_files/enriched_address.csv', index=False)


