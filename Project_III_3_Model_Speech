import os
import glob
import ast
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from joblib import dump


# Define the directory where your data is located.
# Change this to your specific directory.
WORKING_DIR = r"E:\Your\working\direction"
INPUT_DIR = r"Your\Folder\with\all_speech_data\*.csv"


def string_to_list(s):
    """Converts a string representation of a list into an actual list."""
    return ast.literal_eval(s)


def process_data(df, ngram_range=(1, 1), list_format=False):
    """
    Preprocesses the data.

    Args:
    df: pandas DataFrame containing the raw data.
        Must include a 'processed_speech' column with string representations of lists of words.

    ngram_range: tuple (min_n, max_n), default=(1, 1)
        The lower and upper boundary of the range of n-values for different n-grams to be extracted.

    Returns:
    A tuple (X, vectorizer), where X is a matrix of TF-IDF features and vectorizer is the fitted TfidfVectorizer.
    """
    # Convert the 'processed_speech' column to actual lists if needed
    if list_format:
        df['processed_speech'] = df['processed_speech'].apply(string_to_list)

    # Join the lists of words into strings
    df['join_speech'] = df['processed_speech'].apply(lambda x: ' '.join(x))

    # Instantiate the TF-IDF vectorizer
    vectorizer = TfidfVectorizer(ngram_range=ngram_range)

    # Fit the vectorizer to the 'join_speech' data
    X = vectorizer.fit_transform(df['join_speech'])

    return X, vectorizer



def perform_kmeans(X, n_clusters=10):
    """
    Performs KMeans clustering on the data.

    Args:
    X: numpy array or scipy sparse matrix of shape (n_samples, n_features), the input data.
    n_clusters: int, optional (default=10), the number of clusters to form.

    Returns:
    A fitted KMeans instance.
    """
    # Instantiate the KMeans model
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)

    # Fit the model to the data
    kmeans.fit(X)

    return kmeans


def get_top_features_per_cluster(kmeans, vectorizer):
    """
    Gets the top features (closest to the centroid) for each cluster.

    Args:
    kmeans: a fitted KMeans instance.
    vectorizer: a fitted TfidfVectorizer instance.

    Returns:
    A pandas DataFrame where each row corresponds to a cluster and each column corresponds to a top feature for that cluster.
    """
    # Get the centroids of the clusters
    centroids = kmeans.cluster_centers_

    # Get the feature names from the vectorizer
    feature_names = vectorizer.get_feature_names_out()

    # Initialize a DataFrame to hold the top 10 words for each cluster
    top_words_df = pd.DataFrame()

    # For each cluster
    for i in range(10):
        # Get the indices of the features that are closest to the centroid
        top_feature_indices = centroids[i].argsort()[-10:][::-1]

        # Get the corresponding feature names
        top_feature_names = [feature_names[j] for j in top_feature_indices]

        # Add the feature names to the DataFrame
        top_words_df[f'Cluster {i}'] = top_feature_names

    return top_words_df


def save_to_csv(df, path):
    """Saves a DataFrame to a CSV file."""
    df.to_csv(path, index=False)


def save_model(model, path):
    """Saves a model to a file."""
    dump(model, path)


if __name__ == "__main__":
    # Set up working direction
    os.chdir(WORKING_DIR)

    # Get file paths to speech data
    files_directions = glob.glob(INPUT_DIR)

    # Load all speech files and merge them together
    df_list = []
    for i, file in enumerate(files_directions):
        df_list.append(pd.read_csv(file))
    df = pd.concat(df_list, axis=0)
    df = df.dropna(how='any')

    # Preprocess the speech data
    # If we set ngram_range=(1,2), we will have bi-gram model
    # Be really careful when trying something larger than (1,2), it may crush your computer (I've tried)
    X, vectorizer = process_data(df, ngram_range=(1, 1))

    # Perform KMeans clustering
    kmeans = perform_kmeans(X)

    # Get the top features for each cluster
    top_words_df = get_top_features_per_cluster(kmeans, vectorizer)

    # Check if the folder exists
    if not os.path.exists(r'Final'):
        # Create the folder
        os.makedirs(r'Final')

    # Save the DataFrame to a CSV file
    # You could check this file, I think it's quite interesting
    save_to_csv(top_words_df, r'Final\top_10_words_for_cluster_centroids.csv')

    # Add new column with KMeans prediction results
    df['cluster'] = kmeans.predict(X)

    # Save the speech data with KMeans cluster information to a CSV file
    save_to_csv(df, r'Final\speech_data_with_cluster.csv')

    # Save the KMeans model to a file
    save_model(kmeans, r'Final\speech_kmeans.joblib')

