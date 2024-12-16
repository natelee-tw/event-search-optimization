from sklearn.metrics.pairwise import cosine_similarity


def get_embedding(client, text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def find_k_nearest_neighbors(df, query_embedding, k=30):
    # Compute cosine similarity between query embedding and all embeddings in the DataFrame
    score = cosine_similarity([query_embedding], list(df['ada_embedding'].values))[0]

    # Find indices of the top K most similar embeddings
    top_indices = score.argsort()[-k:][::-1]

    # Extract the sentences corresponding to the top indices
    top_k_df = df.iloc[top_indices]

    # give top_k_df a score column normalised to 0-1
    top_k_df['score_semantics'] = (score[top_indices] - score[top_indices].min()) / (score[top_indices].max() - score[top_indices].min())

    return top_k_df

def semantics_search(client, embedding_df, question, n=30):
    print("Question:", question)
    question_embedding = get_embedding(client, question)

    k_nearest_neighbors = find_k_nearest_neighbors(embedding_df, question_embedding, k=n)
    print("K Nearest Neighbors:")

    return k_nearest_neighbors
