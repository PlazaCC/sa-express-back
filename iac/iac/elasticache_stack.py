import os
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

        self.redis_cluster = aws_elasticache.CfnCacheCluster(
            scope=self,
            id='SAExpress_Redis',
            engine='redis',
            cache_node_type='cache.t3.micro',
            num_cache_nodes=1,
            cache_security_group_names=[ 'default' ]
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
