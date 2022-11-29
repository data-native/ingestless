"""
Registers the Providers implementing the given interface
"""
from .AbstractBucketProvider import AbstractBucketProvider
from .AbstractTableProvider import AbstractTableProvider
from .AbstractTopicProvider import AbstractTopicProvider
from .AbstractFunctionProvider import AbstractFunctionProvider

# ProviderImports_______________
from .AWS.provider import bucket, function, table, queue, topic

# AWS Provider__________________
AbstractBucketProvider.register(bucket)
AbstractTableProvider.register(table)
AbstractFunctionProvider.register(function)
AbstractTopicProvider.register(topic)

# AZURE Provider____________
# TODO Register the Azure provider here

