# First import urllib for downloading and uncompress the file
import urllib.request
import zipfile
import os
import pandas as pd
from statistics import mean

DEBUG = True

# # This is the URL for the public data
url = "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

# This is the working directory
working_dir = "../data/movies/"

# Destination filename
file_name = working_dir + "movies.zip"

# Download the file from `url` and save it locally under `file_name`:
if os.path.isfile(file_name):
    if DEBUG:
        print('Data is already downloaded')
else:
    if DEBUG:
        print("Downloading file")
    urllib.request.urlretrieve(url, file_name)

# We already know the expected files so:
expected_files = [
    'links.csv',
    'movies.csv',
    'ratings.csv',
    'README.txt',
    'tags.csv']

# There's an extra dir level in thwe extracted files
inner_dir = "ml-latest-small/"
# I want to know the names of the extracted files
file_names = os.listdir(working_dir + inner_dir)

if file_names == expected_files:
    print("You already have the data files, check it!")
else:
    # This is the code for uncompress hte zipfile
    path_to_zip_file = working_dir + "movies.zip"
    # Reference to zipfile
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    print("Extracting files")
    zip_ref.extractall(working_dir)
    # Is important to use .close()
    zip_ref.close()

# movie.ID mv.ID MV.ID MV_ID
movie_names = ['movie_id', 'title', 'genres']
rating_names = ['user_id', 'movie_id', 'rating', 'timestamp']

# Reading the files needed for this analysis
movies = pd.read_csv(
    working_dir +
    inner_dir +
    expected_files[1],
    sep=',',
    names=movie_names)
ratings = pd.read_csv(
    working_dir +
    inner_dir +
    expected_files[2],
    sep=',',
    names=rating_names)


# Let's print the first lines of each dataframe
if DEBUG:
    print(movies.head())
    print(ratings.head())

print("The names of our new data frames are:")
print(list(movies.columns.values))
print(list(ratings.columns.values))

print("The dimension of the dataframes are:")
print(movies.count())
print(ratings.count())

rated_movies = pd.merge(movies, ratings, on='movie_id')
rated_movies = rated_movies.sort_values('rating', ascending=False)

# Number of movies: 9126
# Number of evaluations: 100005

# Rated movies names:
# ['movie_id', 'title', 'genres', 'user_id', 'rating', 'timestamp']

# Shortcut for names
rated_movies.dtypes

# Get summary of your data
rated_movies.describe()

# Getting the Transpose
transposed_movies = rated_movies.T

# Sorting by an index
rated_movies.sort_index(axis=1, ascending=False)

# You can get the first two rows with
rated_movies[0:3]

# You can select data based in value of a column
rated_movies['rating'] = pd.to_numeric(rated_movies['rating'][1:100005])
rated_movies[rated_movies['rating'] > 4]
rated_movies[rated_movies['title'] == 'Shawshank Redemption, The (1994)']

# rated_movies = rated_movies.pop(0)

# You can aggregate data like this
grouped = rated_movies.groupby('title')
group_by_sum = grouped.aggregate(sum)
group_by_mean = grouped.aggregate(mean)
# group_by_count = grouped.aggregate(count)

# Or the short way
grouped = rated_movies.groupby('title').sum()

# Subsetting for our results
top20 = grouped.sort_values('rating', ascending=False)[0:20]
top5 = top20[0:5]
# Wee need to transform it to a dict
# so we can get the movies' titles
top5_dict = top5.to_dict()
# We need to get the items (Movies titles)
top5_items = top5_dict['rating'].items()

# A helper array for stacking the results per movie
frames = []

# A for loop for getting all the results matching a movie
for name, value in top5_items:
    frames.append(rated_movies[rated_movies['title'] == name])

# Concatenate into a single data frame
result = pd.concat(frames)
# Export to CSV
print("Exporting results to CSV")
top20.to_csv(working_dir + 'top20.csv')
top5.to_csv(working_dir + 'top5.csv')
result.to_csv(working_dir + 'final.csv')
