import glob
import os
from cgitb import html
from dataclasses import dataclass
from distutils.command.build import build
from email import contentmanager
from itertools import product
from pydoc import Doc
from sre_constants import BRANCH
from typing import List

# from app.api.models.document import DocumentModel
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk

path = '/Users/ashishhusain/Documents/dummy_text'

@dataclass
class Product:
    repo: str
    branch: str
    build: str
    
    def __init__(self, repo:str, branch:str, build:str) -> None:
        self.repo = repo
        self.branch = branch        
        self.build = build
@dataclass
class DocumentModel:
    product: Product
    content: str
    path: str
    _id: str
    
    def __init__(self, product: Product, content: str, path:str, id:str) -> None:
        self.product = product
        self.content = content
        self.path = path
        self.id = id
        
    
    def __repr__(self) -> str:
        return (
            'DocumentModel('
            f'Product={self.product!r}, content={self.content!r}'
            f'id={self.id!r}, path={self.path}'
            )

load_dotenv()
class DatabaseService:
    es_client = None
    data = []
    def __init__(self):
        db_url = os.getenv('ELASTICSEARCH_DB_URL')
        self.es_client = Elasticsearch([db_url],request_timeout=300)
    
    def _load_dummy_data_in_index(self) -> List[DocumentModel]:
        # Id cannot have the build number since it will be hard to replace the files later
        
        for filename in glob.glob(os.path.join(path, '*.html')):
            payload_product = Product("epg", "master", "20")
            with open(os.path.join(os.getcwd(), filename), 'r') as f:
                html_doc = f.read()
                document = DocumentModel(
                    product=payload_product,
                    path=f'{filename}',
                    content=html_doc,
                    id=f'{payload_product.repo}_{payload_product.branch}{filename.replace("/","_").split(".")[0]}'
                )
                # print(document.id)
                # self.data['epg_master_20_{filename}'] = document
                self.data.append(document)
            
        result = bulk(self.es_client, self.prepare_for_bulk_upload(), index='document_collection', chunk_size=200, request_timeout=300)
        # print(self.es_client.count(index="document_collection"))
        # print(result)
        return self.data
    
    def prepare_for_bulk_upload(self):
        for val in self.data:
            yield{
                "_index": "document_collection",
                "_id": val.id,
                "_source": {
                    "branch": val.product.branch,
                    
                    "build": val.product.build,
                    "path": val.path,
                    "content": val.content    
                }    
            }
                
                
        
# For testing purpose only!
if __name__ == "__main__":
    x = DatabaseService()
    # print(x.es_client)
    result = x._load_dummy_data_in_index()
    
    
        