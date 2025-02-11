import os
import uuid
import boto3
from constructs import Construct

from aws_cdk import (
    CfnOutput,
    aws_elasticache,
    RemovalPolicy
)

class ElastiCacheStack(Construct):
    def __init__(self, scope: Construct) -> None:
        super().__init__(scope, 'SAExpress_ElastiCache')

        github_ref_name = os.environ.get('GITHUB_REF_NAME', 'dev')
        removal_policy = RemovalPolicy.RETAIN if 'prod' in github_ref_name else RemovalPolicy.DESTROY

        self.cluster_name = 'sacachelayer'

        if self.check_if_cluster_exists():
            print('ElastiCache layer already exists. Skipping deploy...')
            return

        self.redis_cluster = aws_elasticache.CfnCacheCluster(
            scope=self,
            id='SAExpress_Redis',
            engine='redis',
            cache_node_type='cache.t3.small',
            num_cache_nodes=1,
            cache_security_group_names=[ 'default' ],
            cluster_name=self.get_cluster_name_with_nonce()
        )
        
        self.redis_cluster.apply_removal_policy(policy=removal_policy)

        CfnOutput(
            scope=self,
            id='ElastiCacheSAExpressRedisCluster',
            value=self.redis_cluster.attr_redis_endpoint_address,
            export_name=f'SAExpress{github_ref_name}RedisCluster'
        )

        CfnOutput(
            scope=self, 
            id='ElastiCacheSAExpressRemovalPolicy',
            value=removal_policy.value,
            export_name=f'SAExpress{github_ref_name}ElastiCacheRemovalPolicy'
        )

    def get_cluster_name_with_nonce(self):
        nonce = str(uuid.uuid4()).split('-')[0]

        return self.cluster_name + nonce

    def check_if_cluster_exists(self):
        client = boto3.client('elasticache')

        try:
            response = client.describe_cache_clusters()

            for cluster in response['CacheClusters']:
                if cluster['CacheClusterId'].startswith(self.cluster_name) \
                    and cluster['CacheClusterStatus'].lower() != 'deleting':
                    return True

            return False
        except:
            return False