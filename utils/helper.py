import pandas as pd
import numpy as np
import joblib
from difflib import SequenceMatcher
import re
import os
from config.path_config import *

def load_dataframe(file_path):
    """Load DataFrame from file path."""
    try:
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            print(f"File not found: {file_path}")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error loading dataframe: {e}")
        return pd.DataFrame()

############# 1. GET_ANIME_FRAME

def getAnimeFrame(anime, path_df):
    df = load_dataframe(path_df)
    if isinstance(anime, int):
        return df[df.anime_id == anime]
    if isinstance(anime, str):
        return df[df.eng_version == anime]

########## 2. GET_SYNOPSIS

def getSynopsis(anime, path_synopsis_df):
    synopsis_df = load_dataframe(path_synopsis_df)
    try:
        if isinstance(anime, int):
            result = synopsis_df[synopsis_df.MAL_ID == anime].sypnopsis.values
            if len(result) > 0:
                return result[0]
        if isinstance(anime, str):
            result = synopsis_df[synopsis_df.Name == anime].sypnopsis.values
            if len(result) > 0:
                return result[0]
    except Exception as e:
        print(f"Error getting synopsis for {anime}: {e}")
    return "Synopsis not available"

########## 3. CONTENT RECOMMENDATION

def find_similar_animes(name, path_anime_weights, path_anime2anime_encoded, path_anime2anime_decoded, path_anime_df, n=10, return_dist=False, neg=False):
    try:
        # Load weights and encoded-decoded mappings
        if not os.path.exists(path_anime_weights):
            print(f"Anime weights not found: {path_anime_weights}")
            return pd.DataFrame()
            
        anime_weights = joblib.load(path_anime_weights)
        anime2anime_encoded = joblib.load(path_anime2anime_encoded)
        anime2anime_decoded = joblib.load(path_anime2anime_decoded)

        # Get the anime ID for the given name
        anime_frame = getAnimeFrame(name, path_anime_df)
        if anime_frame.empty:
            print(f"Anime not found: {name}")
            return pd.DataFrame()
            
        index = anime_frame.anime_id.values[0]
        encoded_index = anime2anime_encoded.get(index)

        if encoded_index is None:
            print(f"Encoded index not found for anime ID: {index}")
            return pd.DataFrame()

        # Compute similarity distances
        weights = anime_weights
        dists = np.dot(weights, weights[encoded_index])
        sorted_dists = np.argsort(dists)

        n = n + 1

        # Select closest or farthest based on 'neg' flag
        if neg:
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:]

        # Return distances and closest indices if requested
        if return_dist:
            return dists, closest

        # Build the similarity array
        SimilarityArr = []
        for close in closest:
            decoded_id = anime2anime_decoded.get(close)
            if decoded_id is None:
                continue

            anime_frame = getAnimeFrame(decoded_id, path_anime_df)
            if anime_frame.empty:
                continue

            anime_name = anime_frame.eng_version.values[0]
            genre = anime_frame.Genres.values[0] if not anime_frame.Genres.empty else "Unknown"
            similarity = dists[close]

            SimilarityArr.append({
                "anime_id": decoded_id,
                "name": anime_name,
                "similarity": similarity,
                "genre": genre,
            })

        # Create a DataFrame with results and sort by similarity
        if SimilarityArr:
            Frame = pd.DataFrame(SimilarityArr).sort_values(by="similarity", ascending=False)
            return Frame[Frame.anime_id != index].drop(['anime_id'], axis=1)
        else:
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error in find_similar_animes: {e}")
        return pd.DataFrame()

######## 4. FIND_SIMILAR_USERS

def find_similar_users(item_input, path_user_weights, path_user2user_encoded, path_user2user_decoded, n=10, return_dist=False, neg=False):
    try:
        if not os.path.exists(path_user_weights):
            print(f"User weights not found: {path_user_weights}")
            return pd.DataFrame()
            
        user_weights = joblib.load(path_user_weights)
        user2user_encoded = joblib.load(path_user2user_encoded)
        user2user_decoded = joblib.load(path_user2user_decoded)

        index = item_input
        encoded_index = user2user_encoded.get(index)

        if encoded_index is None:
            print(f"User not found in encoding: {index}")
            return pd.DataFrame()

        weights = user_weights
        dists = np.dot(weights, weights[encoded_index])
        sorted_dists = np.argsort(dists)

        n = n + 1

        if neg:
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:]

        if return_dist:
            return dists, closest
        
        SimilarityArr = []

        for close in closest:
            similarity = dists[close]

            if isinstance(item_input, int):
                decoded_id = user2user_decoded.get(close)
                if decoded_id is not None:
                    SimilarityArr.append({
                        "similar_users": decoded_id,
                        "similarity": similarity
                    })
                    
        if SimilarityArr:
            similar_users = pd.DataFrame(SimilarityArr).sort_values(by="similarity", ascending=False)
            similar_users = similar_users[similar_users.similar_users != item_input]
            return similar_users
        else:
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error in find_similar_users: {e}")
        return pd.DataFrame()

################## 5. GET USER PREF

def get_user_preferences(user_id , path_rating_df , path_anime_df ):
    rating_df = pd.read_csv(path_rating_df)
    df = pd.read_csv(path_anime_df)

    animes_watched_by_user = rating_df[rating_df.user_id == user_id]

    user_rating_percentile = np.percentile(animes_watched_by_user.rating , 75)

    animes_watched_by_user = animes_watched_by_user[animes_watched_by_user.rating >= user_rating_percentile]

    top_animes_user = (
        animes_watched_by_user.sort_values(by="rating" , ascending=False).anime_id.values
    )

    anime_df_rows = df[df["anime_id"].isin(top_animes_user)]
    anime_df_rows = anime_df_rows[["eng_version","Genres"]]


    return anime_df_rows



######## 6. USER RECOMMENDATION


def get_user_recommendations(similar_users , user_pref ,path_anime_df , path_synopsis_df, path_rating_df, n=10):
    recommended_animes = []
    anime_list = []

    for user_id in similar_users.similar_users.values:
        pref_list = get_user_preferences(int(user_id) , path_rating_df, path_anime_df)

        pref_list = pref_list[~pref_list.eng_version.isin(user_pref.eng_version.values)]

        if not pref_list.empty:
            anime_list.append(pref_list.eng_version.values)

    if anime_list:
            anime_list = pd.DataFrame(anime_list)

            sorted_list = pd.DataFrame(pd.Series(anime_list.values.ravel()).value_counts()).head(n)

            for i,anime_name in enumerate(sorted_list.index):
                n_user_pref = sorted_list[sorted_list.index == anime_name].values[0][0]

                if isinstance(anime_name,str):
                    frame = getAnimeFrame(anime_name,path_anime_df)
                    anime_id = frame.anime_id.values[0]
                    genre = frame.Genres.values[0]
                    synopsis = getSynopsis(int(anime_id),path_synopsis_df)

                    recommended_animes.append({
                        "n" : n_user_pref,
                        "anime_name" : anime_name,
                        "Genres" : genre,
                        "Synopsis": synopsis
                    })
    return pd.DataFrame(recommended_animes).head(n)

def fuzzy_match_anime(query, anime_list, threshold=0.4):
    """
    Find anime names that match the query using fuzzy string matching.
    """
    query = query.lower().strip()
    matches = []
    
    for anime in anime_list:
        if anime and isinstance(anime, str):
            anime_lower = anime.lower()
            
            # Exact substring match gets highest priority
            if query in anime_lower:
                matches.append((anime, 1.0))
            else:
                # Calculate similarity ratio
                similarity = SequenceMatcher(None, query, anime_lower).ratio()
                if similarity >= threshold:
                    matches.append((anime, similarity))
    
    # Sort by similarity (descending) and return names only
    matches.sort(key=lambda x: x[1], reverse=True)
    return [name for name, _ in matches]

def find_best_anime_match(query, df_path):
    """
    Find the best matching anime name from the dataset.
    """
    df = load_dataframe(df_path)
    if df.empty:
        return None
        
    anime_names = df['eng_version'].dropna().unique().tolist()
    matches = fuzzy_match_anime(query, anime_names, threshold=0.3)
    
    if matches:
        return matches[0]  # Return the best match
    return None
