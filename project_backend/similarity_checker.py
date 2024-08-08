import sentence_transformers

class SimilarityChecker:

    def __init__(self,threshold):
        '''
        This is the constructor function.
        param1 threshold:The threshold value for similarity comparison.
        param2 no_of_questions:The number of questions that should be taken from the question bank so as to make the list of mcq questions.
        '''
        self.threshold=threshold

    def get_embedder(self,mcq_list,q_taken):
        '''
        This function generates embeddings for the given question and mcq list.
        param1 mcq_list:A list of strings consisting of selected questions.
        param2 q_taken:The question for which the embedding needs to be generated.
        returns query_embedding:embedding of the question considered.
        returns corpus_embeddings:embedding of mcq list.
        '''
        embedder =sentence_transformers.SentenceTransformer("all-MiniLM-L6-v2")
        corpus_embeddings=embedder.encode(mcq_list)
        query_embedding=embedder.encode([q_taken])
        return query_embedding,corpus_embeddings
        
    def get_topmost_similarity_score(self,query_embedding,corpus_embeddings):
        '''
        This function is used to get the topmost similarity score between the question considered and the questions in mcq list.
        param1 query_embedding:embedding of the question considered.
        param2 corpus_embeddings:embedding of mcq list.
        returns similarity_score:A dictionary containing the topmost similarity score and index of the most similar question.
        '''
        similarity_score=sentence_transformers.util.semantic_search(query_embedding,corpus_embeddings,top_k=1)
        return similarity_score

    def is_similar(self,mcq_list,q_taken):
        '''
        This function checks if the given question is similar to questions already in the mcq list.
        param1 mcq_list:A list of strings consisting of selected questions.
        param2 q_taken:The question for which the embedding needs to be generated.
        returns bool:True if the question is similar to others in the mcq list,False otherwise.
        '''
        if q_taken in mcq_list:
            return False
        if not mcq_list:
            mcq_list.append(q_taken)
            return True
        query_embedding,corpus_embeddings=self.get_embedder(mcq_list,q_taken)
        similarity_score=self.get_topmost_similarity_score(query_embedding,corpus_embeddings)
        if (similarity_score[0][0]['score']<self.threshold):
            return True
        return False


