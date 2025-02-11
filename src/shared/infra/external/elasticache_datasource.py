import os
import boto3
import redis

class ElastiCacheDatasource:
    def __init__(self, region: str):
        github_ref_name = os.environ.get('GITHUB_REF_NAME', 'dev')

        self.cluster_name = f'sacachelayer{github_ref_name}'
        self.boto_client = boto3.client('elasticache', region_name=region)

        endpoint = self.get_redis_endpoint()
        
        print(endpoint)

        self.redis = redis.StrictRedis(
            host=endpoint['Address'],
            port=endpoint['Port'],
            db=0,
            socket_timeout=5,
            socket_connect_timeout=5
        )

        self.redis.ping()
        self.redis.set('mykey', 'thevalueofmykey')

        print('ELASTICACHE OK')

    def get_redis_endpoint(self) -> dict:
        try:
            response = self.boto_client.describe_cache_clusters(ShowCacheNodeInfo=True)
        
            for cluster in response['CacheClusters']:
                if cluster['CacheClusterId'].startswith(self.cluster_name) \
                    and cluster['CacheClusterStatus'].lower() != 'deleting':
                    for node in cluster['CacheNodes']:
                        return node['Endpoint']
        except:
            pass

        raise Exception('Redis cluster not found')
