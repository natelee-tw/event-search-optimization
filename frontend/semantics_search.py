from sklearn.metrics.pairwise import cosine_similarity



def get_embedding(client, text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def find_k_nearest_neighbors(df, query_embedding, k=5):
    # Compute cosine similarity between query embedding and all embeddings in the DataFrame
    similarities = cosine_similarity([query_embedding], list(df['ada_embedding'].values))[0]

    # Find indices of the top K most similar embeddings
    top_indices = similarities.argsort()[-k:][::-1]

    # Extract the sentences corresponding to the top indices
    top_k_df = df.iloc[top_indices]

    return top_k_df

def semantics_search(client, embedding_df, question, n=5):
    print("Question:", question)
    question_embedding = get_embedding(client, question)

    k_nearest_neighbors = find_k_nearest_neighbors(embedding_df, question_embedding, k=n)
    print("K Nearest Neighbors:")

    # for neighbor in k_nearest_neighbors:
    #     print(neighbor)

    # return a dataframe with top 5 nearest neighbors
    return k_nearest_neighbors

    
