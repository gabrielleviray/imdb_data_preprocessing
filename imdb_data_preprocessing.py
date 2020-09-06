# CMPE 255: Data Mining
# Learning Activity 1
# Author: Gabrielle Viray, SID: 012340068
# Date: 9/4/2020

import pandas as pd
import numpy as np
import ftfy as ftfy

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 50)


# 1. Open the csv with your favorite spreadsheet application (excel, google sheets,

# **2. What are the attribute types of each of the columns?**
# nominal, ordinal, interval, ratio
    #   numbers, etc.)
    #   color: nominal
    #   director_name: nominal
    #   duration: interval
    #   gross: ratio
    #   genres: nominal
    #   movie_title: nominal
    #   title_year: interval
    #   language: nominal
    #   country: nominal
    #   budget: ratio
    #   imdb_score: ratio
    #   actors: nominal
    #   movie_facebook_likes: ratio
    
def load_data(filename):
    """Given a filename of a csv load data into a Pandas dataframe.

        filename - string

        return Pandas dataframe
    """
    return pd.read_csv(filename, encoding='utf-8')

def remove_unnecersary_columns(imdb):
    imdb.drop(["language"], axis=1,inplace=True)

def fill_missing_values(imdb):
    imdb.genres.fillna('N/A', inplace=True)
    
def update_country_names(imdb):
    imdb["country"] = imdb["country"].str.upper()
    imdb["country"] = imdb["country"].str.replace('UNITED STATES', 'USA')
    
def fix_director_values(imdb):
    imdb["director_name"] = imdb["director_name"].fillna('')
    imdb["director_name"] = imdb["director_name"].replace('Null', '')

def fix_unicode_movie_title(imdb):
    for i, row in imdb.iterrows():
        imdb.at[i,'movie_title'] = ftfy.fix_encoding(row['movie_title'])
    
def fix_outliers(imdb):
    imdb.drop(imdb[imdb['title_year'] < 2010].index, inplace = True)
    imdb.drop(imdb[imdb['imdb_score'] < 1].index, inplace = True)
    imdb.drop(imdb[imdb['imdb_score'] > 10].index, inplace = True)

def main():
    
    """
    Clean up the imdb dataset
    """


    # 3. Rename filename.csv to the data filename.
    imdb = load_data('imdb.csv')
    
    # 4. Using Pandas dataframe drop function get rid of unnecessary columns (set
    # inplace=True)
    remove_unnecersary_columns(imdb)
    
    # **5. How many columns did you remove?**
    #
    #   1 column: I removed the'language' because all language values are the same.
    
    # 6. How many missing values are there within each column?**
    # hint: use isnull and the sum function
    #    ANSWER:
    #               color                   11
    #               director_name           11
    #               duration                 0
    #               gross                    8
    #               genres                   1
    #               movie_title              0
    #               title_year               0
    #               country                  0
    #               budget                   4
    #               imdb_score               0
    #               actors                   0
    #               movie_facebook_likes     0
    missing_values_count = (imdb.isnull().sum())
    print("Number of missing values within each column:")
    print(missing_values_count)
    
    # **7. What missing values can be easily filled without changing the basic statistics
    # (what columns)?**
    #
    #   ANSWER: Filling director_names and genres do not affect the basic stats. 
    
    
    # 8. Fill the columns from 7 with the fillna function (use inplace argument).

    # Replaces Missing Values with "N/A" in genres columns
    fill_missing_values(imdb)
    
    # 9. Uppercase all of the country values (hint: str.upper())
    # 9a. replace any reference to United States to USA
    update_country_names(imdb)
    
    # 10. Replace N/A, Nan, Null with an empty string
    #
    # ASSUMPTION: 'Nan' is assumed to be a valid director name because it is not 'NaN.'
    fix_director_values(imdb)
    
    # 11. Fix unicode in 'movie_title' column with import ftfy
    fix_unicode_movie_title(imdb)

    # 12. Assume a movie cannot be < 10 mins or > 300 mins. If a movie is outside those
    # bounds set the value to 0.
    imdb.loc[imdb['duration'] < 10, 'duration'] = 0
    imdb.loc[imdb['duration'] > 300, 'duration'] = 0
    
    # **13. What would be considered an outlier for imdb_score?**
    #
    #   ANSWER: The range of imdb scores are from 1 to 10. Zero, negative numbers
    #   and numbers greater than 10 are considered outliers.
    
    # 14. Fix imdb_score and title_year (no year prior to 2010) outliers.
    #      FIX: Remove rows that contain these outliers.
    fix_outliers(imdb)

    # 15. output the cleaned up file onto a new csv called clean_imdb.csv
    #
    # ASSUMPTION: Encoding utf-8 for consistency.
    imdb.to_csv('clean_imdb.csv', encoding='utf-8', index=False)
    print('\nOutput written to clean_imdb.csv')



if __name__ == '__main__':
    main()