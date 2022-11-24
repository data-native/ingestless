"""
Defines the JSONSchema object schemata 
expected in a given version of the code
"""

TemplateSchema = {
    "type": "object",
    "properties": {
        "version": {"type": "string"},
        "kind": {"type": "string"},
        "metadata": {"type": "object"},
        "config": {"type": "object"},
    },
    "required": ["version", "kind", "config"]
}

MetadataSchema = {
    "type": "object",
    "properties": {
        "name" : {"type": "string"},
    },
}

ConfigSchema = {
    "type" : "object",
    "properties": {
        "endpoints": {
            "type": "array",
            "items": {
                "type": "object",
                "properties":{
                    "kind" : {"type": "string"},
                    "url" : {"type": "string"},
                    "base" : {"type": "string"},
                    "relative" : {"type": "string"},
                    "params": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name" : {"type": "string"}
                            }
                        }
                    }
                }
            }
            },
        "params": {"type": "object"},
        "resolvers": {"type": "object"},
    },
    "required": ["endpoints", "params", "resolvers"]
}

#TODO: Define schema
ParamsSchema = {
    "type": "object",
    "properties": {
        "name" : {"type": "object"},
        "name" : {"type": "string"},
        "name" : {"type": "string"},
        "name" : {"type": "string"},
    },
}

#TODO: Define schema
EndpointSchema = {
    "type": "object",
    "properties": {
        "name" : {"type": "string"},
    },
}

#TODO: Define schema
ResolverSchema = {
    "type": "object",
    "properties": {
        "name" : {"type": "string"},
    },
}

# Mapping dictionary to facilitate resolution of schema to keys
schema_mapping = {
    'template': TemplateSchema,
    'metadata': MetadataSchema,
    'config': ConfigSchema,
    'endpoints': EndpointSchema,
    'params': ParamsSchema,
    'resolvers': ResolverSchema
}