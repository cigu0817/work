# model.py
from sklearn.cluster import KMeans

def cluster_locations(df):

    X = df[['longitude', 'latitude']]
    kmeans = KMeans(n_clusters=4, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)
    

    cluster_map = {
        0: '🚀 成熟核心商圈', 
        1: '🏢 办公商务区', 
        2: '🌳 新兴潜力区', 
        3: '🏠 居民生活区'
    }
    df['zone_type'] = df['cluster'].map(cluster_map)
    return df