'''
This script is used to use a NN model to embed the query and then use the pre-generated
embeddings to find the most similar embeddings in the database.
'''
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import os
import numpy as np

class Inference:
    def __init__(self, backbone='mixedbread-ai/mxbai-embed-large-v1', embed_file='embeddings.npy'):
        self.backbone = backbone
        self.embeddings = None
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.embed_path = os.path.join(self.base_path, '../data')

        self.model = SentenceTransformer(backbone)

        self.load_embeddings(embed_file)

    def transform_query(self, query: str) -> str:
        '''
        Transforms query into a form that can be used for searching relevant passages.

        Args:
        query: str: query string

        Returns:
        str: transformed query string
        '''
        return f'Represent this sentence for searching relevant passages: {query}'

    def get_search_results(self, query):
        '''
        Get the search results for the given query.

        Parameters:
        query (str): The query to search for.

        Returns:
        list: The list of search results.
        '''
        query = self.transform_query(query)

        query_embedding = self.model.encode([query])
        similarities = cos_sim(query_embedding[0], self.embeddings)
        similarities = similarities[0].cpu().numpy()
        results = np.argsort(similarities)[::-1]
        return results

    def load_embeddings(self, file_name='embeddings.npy'):
        '''
        Load the embeddings from the given path.

        Parameters:
        embed_path: str: The path to the embeddings file.
        '''
        self.embeddings = np.load(os.path.join(self.embed_path, file_name))
