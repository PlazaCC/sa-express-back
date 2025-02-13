import os
import boto3
import redis
from typing import Any
from redis.commands.json.path import Path

from src.shared.environments import Environments

class ElastiCacheDatasource:
    def __init__(self, region: str):
        github_ref_name = os.environ.get('GITHUB_REF_NAME', 'dev')

        self.cluster_name = f'sacachelayer{github_ref_name}'
        self.boto_client = boto3.client('elasticache', region_name=region)

        endpoint = self.get_redis_local_endpoint() if Environments.persist_local else self.get_redis_endpoint()

        self.redis = redis.StrictRedis(
            host=endpoint['Address'],
            port=endpoint['Port'],
            db=0,
            socket_timeout=3,
            socket_connect_timeout=3
        )

    def get_redis_local_endpoint(self) -> dict:
        return { 'Address': '127.0.0.1', 'Port': 6379 }

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
    
    def exec(self, cmd: list[str]) -> Any:
        return self.redis.execute_command(*cmd)
    
    def get_json(self, key: str, path: str = Path.root_path()) -> dict | None:
        return self.redis.json().get(key, path, no_escape=False)
    
    def set_json(self, key: str, data: dict, path: str = Path.root_path()) -> None:
        self.redis.json().set(key, path, data)

    def expire(self, key: str, seconds: int) -> None:
        self.redis.expire(key, seconds)

    def evalsha(self, script_hash: str, keys: list[str]):
        return self.redis.evalsha(script_hash, len(keys), *keys)
