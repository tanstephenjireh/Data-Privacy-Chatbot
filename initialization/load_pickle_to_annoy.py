from langchain_community.vectorstores import Annoy
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
import pandas as pd
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input-filename", type=str, required=True,
                    help="The filename of the pickle file containing the documents")
parser.add_argument("-o", "--output-foldername", type=str, required=True,
                    help="The output folder of the annoy dump")
parser.add_argument("-m", "--model", type=str, required=True, choices=["azure", "openai"],
                    help="The output folder of the annoy dump")

args = parser.parse_args()

SAVE_PATH = f"{args.output_foldername}"

def check_env_vars(env_var_list):
    IS_REQUIRED_ENV_VARS_COMPLETE = all(
        [env_var in os.environ for env_var in env_var_list]
    )

    return IS_REQUIRED_ENV_VARS_COMPLETE

def check_api_keys(env_var_list):
    if not check_env_vars(env_var_list):
        from dotenv import load_dotenv
        load_dotenv()
        assert check_env_vars(env_var_list)!=False, f"Incomplete Environment Variables. Please check {env_var_list}"

def load_api_keys():
    env_var_list = []
    if args.model == "openai":
        env_var_list = ["OPENAI_API_KEY"]
    elif args.model == "azure":
        env_var_list = ["AZURE_OPENAI_API_KEY","AZURE_OPENAI_ENDPOINT","AZURE_OPENAI_EMBEDDING_API_VERSION","AZURE_OPENAI_CHAT_EMBEDDING_DEPLOYMENT_NAME"]

    check_api_keys(env_var_list)
     
def load_pickled_dump(save_path):
    """Function for loading document artifacts and creating an annoy vector db out of it"""
    print("Starting to create collection")
    docs = pd.read_pickle(f"{args.input_filename}")
    embedding_func = None
    if args.model == "openai":
        embedding_func =  OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=os.environ.get("OPENAI_API_KEY"))
    elif args.model == "azure":
        embedding_func =  AzureOpenAIEmbeddings(
                                azure_deployment=os.environ["AZURE_OPENAI_CHAT_EMBEDDING_DEPLOYMENT_NAME"],
                                openai_api_version=os.environ["AZURE_OPENAI_EMBEDDING_API_VERSION"],
                                azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                                api_key=os.environ["AZURE_OPENAI_API_KEY"],
                            )

    vector_db = Annoy.from_documents(
                    docs,
                    embedding_func,
                    metric='angular'
                )
    vector_db.save_local(save_path)

    print(f"Documents saved to {save_path}")


if __name__ == "__main__":
    load_api_keys()
    load_pickled_dump(SAVE_PATH)
