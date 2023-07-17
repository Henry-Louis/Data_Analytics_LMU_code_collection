# Data_Analytics_LMU_code_collection
This project aims to share the python codes covered in LMU Data Analytics Course, in a clearly structured and carefully commented manner, for learning and communicating purpose.

# Why this course is useful? And Why this course may be hard?
The reason I put these two answers together is they can be answered in a same fact: Real-World Data is Messy. It comes in different formats, from different sources, and often contains missing values, inconsistencies, and problems you may never expected. But as the flip side of this coin, if we can handle the data source with the most evel nature, we have a huge advantage to understand phenomenon that others may not.

As previously suggested, the main focus of this course is data preparation. Dr. Mathias only used a fraction of lecture to cover the actual statistic inference results, perhaps the things matter are the data themselves. Enjoy~

# Course Structure
The main course of Data Analytics is composed by 3 projects: 
1. Agriculture Datasets Merging 
2. Missing Value Filling with the Dataset Scraped from Clergy Database
3. Canada Parliament Election Analysis with Dynamic Website Scraping and Text Processing

# Brief Introduction of the 3 Projects
- Agriculture Datasets Merging
  1. Download the 46 subdatasets (the variable names in each subdatasets are inconsistent)
  2. Choose a list of interested variables (later use then to construct a DV called Farm_Performance)
  3. Pick the list of variables from each subdataset (You may choose different time period to work on)
  4. Merge the interested variables into one dataframe (name it "agriculture_df")
  5. Merge agriculture_df with the election_df (election_df can be downloaded from Moodle)
  6. Done
- Missing Value Filling with the Dataset Scraped from Clergy Database
  1. Scrape the Clergy Database website to get many html files
  2. Parse the html files and turn them into to CSV files
  3. Extract appointments data from the CSV files
  4. Merge the appointment data with england_population_df (england_population_df can be downloaded from Moodle)
  5. Predict the missing values in england_population_df with the appointment data
  6. Done
- Canada Parliament Election Analysis with Dynamic Website Scraping and Text Processing
  1. Scrape the Canada Parliament data from a dynamic website
  2. Get many CSV files and merge them for later usage (then we use people's speech to augment the data)
  3. Download raw speech data from Moodle
  4. Clean and prepare the speech text
  5. Extract features from the prepared speech text (using vectorizer and clustering algorithm)
  6.   ( continue... )


# Notes:
This is still a working project, I will try my best to make the codes I share as systematic and easy-to-read as possible. If you find or have any questions, please concact me. Let's learn together~
email: liuqihang1999@outlook.com

Sincerely,
Henry
