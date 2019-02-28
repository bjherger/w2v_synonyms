#!/usr/bin/env python
"""
coding=utf-8

Code template courtesy https://github.com/bjherger/Python-starter-repo

"""
import logging
import pickle

import gensim

from bin import lib
from bin.Thesaurus import Thesaurus


def main():
    """
    Main function documentation template
    :return: None
    :rtype: None
    """
    logging.basicConfig(level=logging.DEBUG)
    custom_embedding = True

    # Download embeddings'
    if custom_embedding:
        embedding_path = '../data/custom_embedding.pkl'
        embedding_index_path = '../data/custom_vocab_index.pkl'
        logging.info('Pulling custom embedding from: {}, and custom vocab from: {}'.format(embedding_path, embedding_index_path))
        embedding_matrix = pickle.load(open(embedding_path, 'rb'))
        embedding_index_lookup = pickle.load(open(embedding_index_path, 'rb'))

    else:
        logging.warning('Downloading embedding. If downloading for the first time, this make take 5-10 minutes.')
        embedding_url = 'https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz'
        embedding_path = '~/nlp_example/'
        embedding_filename = 'GoogleNews-vectors-negative300.bin.gz'
        lib.download_file(embedding_url, embedding_path, embedding_filename)

        # Unpack embedding
        model = gensim.models.KeyedVectors.load_word2vec_format(embedding_path + '/' + embedding_filename, binary=True)
        embedding_matrix = model.syn0
        embedding_index_lookup = dict([(k, v.index) for k, v in model.vocab.items()])

    # Create thesaurus
    thesaurus = Thesaurus(embedding_matrix, embedding_index_lookup)

    # Find nearest neighbors for examples
    print(thesaurus.synonyms('day'))
    print(thesaurus.synonyms('top'))
    print(thesaurus.synonyms('bottom'))
    print(thesaurus.synonyms('cat'))
    print(thesaurus.synonyms('grown'))


    pass

# Main section
if __name__ == '__main__':
    main()
