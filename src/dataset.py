import pandas as pd
import os

class Dataset:

    def __init__(self):
        # List of CSV files to load as dataframes
        self._dataframe_names = ['movies', 'ratings']

        self._prepare()


    def _prepare(self):
        self._dataframe: dict[int, pd.DataFrame] = {}

        self._load_dataframes()
        self._init_ratings()
        self._init_movies()
    

    def _load_dataframes(self) -> None:
        """
        Loads CSV files into pandas dataframes.
        """
        # Define project and dataset paths
        project_folder = os.path.dirname(__file__) + '/../'
        dataset_path = os.path.join(project_folder, 'dataset', 'movielens-edu')

        # Load CSV files into pandas dataframes
        for name in self._dataframe_names:
            path = os.path.join(dataset_path, name + '.csv')
            self._dataframe[name] = pd.read_csv(path)

    
    def _init_ratings(self):
        # Dictionary to store user ratings
        self._user_to_movie_ratings: dict[int, dict[int, float]] = {}

         # Group ratings dataframe by user
        df_grouped_by_user = self._dataframe['ratings'].groupby('userId')

        # Calculate mean rating for each user
        self._user_ratings_mean = df_grouped_by_user.rating.mean()

        # Initialize user ratings dictionary
        for user_id, rating_df in df_grouped_by_user:
            self._user_to_movie_ratings[user_id] = dict(zip(rating_df['movieId'], rating_df['rating']))


    def _init_movies(self):
        self.df_grouped_by_movieId = self._dataframe['movies'].groupby('movieId')
    

    def print_dataset_first_rows(self, nrows: int = 5) -> None:
        """
        Prints the first few rows of each dataframe in the dataset.

        Args:
            nrows (int, optional): Number of rows to display. Defaults to 5.
        """
        # Display the first few rows of each dataframe in the dataset
        print('Max '+ str(nrows) +' csv rows displayed per file.\n')

        for name in self._dataframe_names:
            print('Display '+ name +'.csv')
            print('Number of elements: ', len(self._dataframe[name]))
            print('First elements: ', self._dataframe[name].head(nrows))
            print('\n')


    def has_user_rated_movie(self, user_id: int, movie_id: int) -> bool:
        return self._user_to_movie_ratings[user_id].get(movie_id) != None


    def get_user_mean_rating(self, user_id: int) -> float:
        return self._user_ratings_mean[user_id]
    

    def get_rating(self, user_id: int, movie_id: int) -> float:
        return self._user_to_movie_ratings[user_id][movie_id]
    

    def get_rating_mean_centered(self, user_id: int, movie_id: int) -> float:
        return self.get_rating(user_id, movie_id) - self.get_user_mean_rating(user_id)
    

    def get_movies_rated_by_user(self, user_id: int) -> set[int]:
        return set(self._user_to_movie_ratings[user_id].keys())
    

    def get_movies_unrated_by_user(self, user_id: int) -> set[int]:
        # Calculate the difference between all movies and rated movies
        return self.get_movies() - self.get_movies_rated_by_user(user_id)
    

    def get_common_movies(self, user1_id: int, user2_id: int) -> set[int]:
        return self.get_movies_rated_by_user(user1_id) & self.get_movies_rated_by_user(user2_id)
    

    def get_users(self) -> set[int]:
        return set(self._dataframe['ratings']['userId'])
    

    def get_movies(self) -> set[int]:
        return set(self._dataframe['movies']['movieId'])
    

    def get_movie_name(self, movie_id: int) -> str:
        return self.df_grouped_by_movieId.get_group(movie_id).title[0]