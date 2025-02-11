import os
import uuid
import boto3
from constructs import Construct

from aws_cdk import (
    CfnOutput,
    aws_ec2,
    aws_elasticache,
    RemovalPolicy
)

class ElastiCacheStack(Construct):
    def __init__(self, scope: Construct) -> None:
        super().__init__(scope, 'SAExpress_ElastiCache')

        github_ref_name = os.environ.get('GITHUB_REF_NAME', 'dev')
        
        removal_policy = RemovalPolicy.RETAIN if 'prod' in github_ref_name else RemovalPolicy.DESTROY

        self.cluster_name = f'sacachelayer{github_ref_name}'

        redis_vpc_id = f'SAExpress{github_ref_name}RedisVPC'
        redis_sg_id = f'SAExpress{github_ref_name}RedisSecurityGroup'
        redis_subnet_group_id = f'SAExpress{github_ref_name}RedisSubnetGroup'

        self.redis_vpc = aws_ec2.Vpc(
            scope=self,
            id=redis_vpc_id,
            max_azs=2
        )
        
        self.redis_sg = aws_ec2.SecurityGroup(
            scope=self,
            id=redis_sg_id,
            vpc=self.redis_vpc,
            description=redis_sg_id,
            allow_all_outbound=True
        )

        self.redis_sg.add_ingress_rule(
            peer=aws_ec2.Peer.any_ipv4(),
            connection=aws_ec2.Port.tcp(6379),
            description=f'SAExpress{github_ref_name}RedisIngress'
        )

        self.redis_subnet_group = aws_elasticache.CfnSubnetGroup(
            scope=self,
            id=redis_subnet_group_id,
            cache_subnet_group_name=redis_subnet_group_id,
            subnet_ids=[ subnet.subnet_id for subnet in self.redis_vpc.private_subnets ],
            description=redis_subnet_group_id
        )

        cluster_info = self.get_cluster_if_exists()

        self.redis_cluster = aws_elasticache.CfnCacheCluster(
            scope=self,
            id='SAExpress_Redis',
            engine='redis',
            cache_node_type='cache.t3.small',
            num_cache_nodes=1,
            cluster_name=self.get_cluster_name_with_nonce() if cluster_info is None else cluster_info['CacheClusterId'],
            vpc_security_group_ids=[ self.redis_sg.security_group_id ],
            cache_subnet_group_name=self.redis_subnet_group.cache_subnet_group_name
        )

        self.redis_cluster.add_depends_on(self.redis_subnet_group)
        self.redis_cluster.apply_removal_policy(policy=removal_policy)

        CfnOutput(
            scope=self,
            id='ElastiCacheSAExpressRedisVPC',
            value=self.redis_vpc.vpc_id,
            export_name=f'SAExpress{github_ref_name}RedisVPC'
        )

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
    
    def get_cluster_if_exists(self) -> dict | None:
        client = boto3.client('elasticache')

        try:
            response = client.describe_cache_clusters()

            for cluster_info in response['CacheClusters']:
                if cluster_info['CacheClusterId'].startswith(self.cluster_name) \
                    and cluster_info['CacheClusterStatus'].lower() != 'deleting':
                    return cluster_info

            return None
        except:
            return None

