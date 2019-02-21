import logging

from sklearn.neighbors import NearestNeighbors

class Thesaurus(object):

    def __init__(self, embedding, embedding_index_lookup, n_neighbors=25):
        # TODO Remove limited vocab
        embedding = embedding[:100000, :]
        self.n_neighbors = n_neighbors
        self.embedding = embedding
        self.embedding_index_lookup = embedding_index_lookup
        self.embedding_word_lookup = dict([[v,k] for k,v in embedding_index_lookup.items()])
        self.neighbors = self.create_nn()
        pass

    def synonyms(self, word):
        if word not in self.embedding_index_lookup.keys():
            raise ValueError('Unknown word: {}'.format(word))

        word_index = self.embedding_index_lookup[word]
        word_vector = self.embedding[word_index].reshape(1, -1)

        distances, indices = self.neighbors.kneighbors(word_vector, self.n_neighbors, True)
        distances = distances.flatten()
        indices = indices.flatten()
        words = map(lambda x: self.embedding_word_lookup[x], indices)
        return zip(words, distances)



    def create_nn(self):
        neighbors = NearestNeighbors(n_neighbors=self.n_neighbors, n_jobs=-1)

        logging.info('Training neighbors model. This may take 5-10 minutes')
        neighbors.fit(self.embedding)
        return neighbors
