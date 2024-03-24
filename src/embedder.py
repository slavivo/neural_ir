'''
Script to embed the text data using the sentence transformer model.
'''

import numpy as np
import pandas as pd
import os
import logging
import sys
import argparse
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# Set up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, '../data/')

def embed_df(df, model):
    '''
    This function is used to embed the text data in the given dataframe using the given model.
    
    Parameters:
    df (pandas.DataFrame): The dataframe containing the text data.
    model (sentence_transformers.SentenceTransformer): The sentence transformer model to be used for embedding.
    
    Returns:
    numpy.ndarray: The numpy array containing the embeddings of the text data.
    '''


    def categorize_price(price):
        if price <= 1000:
            return 'hodně levné'
        elif price <= 5000:
            return 'levné'
        elif price <= 10000:
            return 'drahé'
        else:
            return 'velmi drahé'
    try:
        sep_token = '###'
        df['price_cat'] = df['price'].apply(categorize_price)
        df['to_embed'] = 'Jméno: ' + df['name'] + sep_token + ' Cena: ' + df['price_cat'] + sep_token + ' Popis: ' + df['specification']
        to_embed = df['to_embed'].tolist()[:50] # TODO remove the slicing

        embeddings = model.encode(to_embed, show_progress_bar=True)
        return embeddings
    except Exception as e:
        logger.error('Error in embedding the data.')
        logger.error(f'Error: {e}')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, required=True, help='The input file containing the text data.')
    parser.add_argument('--output_file', type=str, required=False, help='The output file to save the embeddings.')
    parser.add_argument('--model', type=str, required=False, help='The sentence transformer model to be used for embedding.')

    args = parser.parse_args()
    input_path = os.path.join(data_path, args.input_file)
    output_path = os.path.join(data_path, args.output_file) if args.output_file else os.path.join(data_path, args.input_file.split('.')[0] + '_embeddings.npy')

    input_df = pd.read_csv(input_path)

    backbone = args.model if args.model else 'mixedbread-ai/mxbai-embed-large-v1'
    model = SentenceTransformer(backbone)
    logger.info(f'Using the model: {backbone} to embed the data...')

    embeddings = embed_df(input_df, model)

    logger.info(f'Saving the embeddings to {output_path}...')
    np.save(output_path, embeddings)

if __name__ == '__main__':
    main()