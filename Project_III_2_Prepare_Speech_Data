# Import necessary packages
import os
import glob
import pandas as pd

# Import text processing package NLTK
# If you have issue with importing nltk
# Please first check the solution on Moodle post by Alejandra Páramo Pascual
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Define the directory where your data is located.
# Change this to your specific directory.
DATA_DIR = "E:/Your/working/direction"
INPUT_DIR = "Input/Speeches*.xlsx"

# If you've installed nltk data in a non-default path, you need to add that path.
# If you've used the default installation, you can comment this line out.
# nltk.data.path.append("E:/Software/nltk/nltk_data")


def load_speech_files(input_path):
    """
    This function loads all speech files from the directory.

    Returns:
        A list of filenames for all speech files.
    """
    os.chdir(DATA_DIR)
    speech_files = glob.glob(input_path)
    return speech_files


def prepare_speech_df(df, word_count=500):
    """
    This function prepares the speech dataset. It removes rows with any missing data in the "speechtext" and "speakername" columns,
    extracts the year from the "speechdate" column, and filters out speeches shorter than a certain word count.

    Parameters:
        df: A DataFrame containing the speeches.
        word_count: The minimum word count for a speech to be included. Default is 500.

    Returns:
        A DataFrame of the processed speeches.
    """
    # Remove rows with missing data in the "speechtext" and "speakername" columns
    df = df.dropna(subset=["speechtext", "speakername"], how="any")

    # Extract the year from the "speechdate" column
    df['year'] = df['speechdate'].str.split('-').str[0]

    # Select necessary columns and remove duplicates
    df = df[["basepk", "speechtext", "speakername", "year"]]
    df = df.drop_duplicates(subset=["speechtext"])

    # Compute speech length and filter out speeches shorter than word_count
    df["speechlength"] = df["speechtext"].str.len()
    df = df[df.speechlength > word_count]

    return df


def filter_string(string, stem=True):
    """
    This function filters a given string. It tokenizes the string, removes English stopwords, keeps only certain categories of words,
    and optionally stems the words.

    Parameters:
        string: The string to be filtered.
        stem: Whether to stem the words. Default is True.

    Returns:
        A list of filtered words.
    """
    # Tokenize the string into words
    word_list = word_tokenize(string)

    # Remove English stopwords
    stop_words = set(stopwords.words("english"))
    filtered_word_list = [x for x in word_list if not x in stop_words]

    # Keep only certain categories of words
    word_pos_pairs = nltk.pos_tag(filtered_word_list)
    selected_categories = ["NN", "NNS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "RB"]
    filtered_word_list = [word for (word, pos) in word_pos_pairs if pos in selected_categories]

    # Stem the words if stem is True
    if stem:
        stemmer = PorterStemmer()
        filtered_word_list = [stemmer.stem(word) for word in filtered_word_list]

    return filtered_word_list


def process_speech_files(speech_files):
    """
    This function processes all speech files by loading, preparing and filtering the data.

    Parameters:
        speech_files: A list of filenames for the speech files.
    """
    for file in speech_files:
        print(f"Loading {file}...")

        # Load the file into a DataFrame
        df = pd.read_excel(file)

        # Prepare the DataFrame
        data = prepare_speech_df(df)

        # Apply the filter_string function to the "speechtext" column
        data["processed_speech"] = data["speechtext"].apply(filter_string)

        print(f"Processing is finished for {file}, saving to Output folder...")

        # Save the processed data to a new file in the Output folder
        processed_file_name = file.replace(".xlsx", "_processed.csv").replace("Input", "Output")
        data.to_csv(processed_file_name, index=False)


# The main function to run the program
def main():
    # Load the speech files
    speech_files = load_speech_files(INPUT_DIR)

    # Process the speech files
    process_speech_files(speech_files)


# Execute the main function, and start to process the speech data
if __name__ == "__main__":
    main()
