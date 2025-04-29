import os
import pandas as pd
from tqdm import tqdm
from pymilvus import connections
from pymilvus import Collection
from pymilvus import utility
from pymilvus import CollectionSchema, FieldSchema, DataType

# import configparser

# config_data = configparser.ConfigParser()
# config_data.read("config.txt")
# milvus_config = config_data["milvus"]

import os

if os.environ.get("OPENAI_API_KEY") is None:
    from dotenv import load_dotenv

    load_dotenv()

MILVUS_ALIAS = os.environ.get("MILVUS_ALIAS")
MILVUS_USER = os.environ.get("MILVUS_USER")
MILVUS_PASS = os.environ.get("MILVUS_PASS")
MILVUS_HOST = os.environ.get("MILVUS_HOST")
MILVUS_PORT = os.environ.get("MILVUS_PORT")

# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

COLL_NAME = "wp_gcashwiki_chunked_test2"
# CONN = connections.connect(
#     alias=milvus_config["alias"],
#     user=milvus_config["user"],
#     password=milvus_config["password"],
#     host=milvus_config["host"],
#     port=milvus_config["port"],
# )
CONN = connections.connect(
    alias=MILVUS_ALIAS,
    user=MILVUS_USER,
    password=MILVUS_PASS,
    host=MILVUS_HOST,
    port=MILVUS_PORT,
)

doc_id_field = FieldSchema(
    name="doc_id",
    dtype=DataType.VARCHAR,
    max_length=300,
    is_primary=True,
)
chunk_num_field = FieldSchema(
    name="chunk_num",
    dtype=DataType.INT64,
)
doc_vector_field = FieldSchema(
    name="doc_vector",
    dtype=DataType.FLOAT_VECTOR,
    dim=1536,
)
doc_text_field = FieldSchema(
    name="doc_text",
    dtype=DataType.VARCHAR,
    max_length=65535,
)
doc_name_field = FieldSchema(
    name="doc_name",
    dtype=DataType.VARCHAR,
    max_length=65535,
)
token_count_field = FieldSchema(
    name="token_count",
    dtype=DataType.INT64,
)
version_num_field = FieldSchema(
    name="version_num",
    dtype=DataType.VARCHAR,
    max_length=65535,
)
last_edited_timestamp_field = FieldSchema(
    name="last_edited_timestamp",
    dtype=DataType.INT64,
)
schema = CollectionSchema(
    fields=[
        doc_id_field,
        chunk_num_field,
        doc_vector_field,
        doc_text_field,
        doc_name_field,
        token_count_field,
        version_num_field,
        last_edited_timestamp_field,
    ],
    description="GCashWiki chunked document search",
)

fields = [
    "doc_id",
    "chunk_num",
    "doc_vector",
    "doc_text",
    "doc_name",
    "token_count",
    "version_num",
    "last_edited_timestamp",
]


async def load_pickled_dump():
    print("Starting to create collection")

    existing_collections = utility.list_collections()
    if COLL_NAME in existing_collections:
        return

    # utility.drop_collection(COLL_NAME)

    new_collection = Collection(
        name=COLL_NAME, schema=schema, using="default", shards_num=2
    )
    new_collection.create_index(
        field_name="doc_vector",
        index_params={
            "metric_type": "IP",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024},  # number of cluster units
        },
    )

    df_data = pd.read_pickle("./datas/baodr.pkl")

    # data = []
    # for field in fields:
    #     data.append(df_data[field].values.tolist())

    # new_collection.insert(data)
    # print("GCashwiki collection loaded to local Milvus!")

if __name__ == "__main__":
    load_pickled_dump()