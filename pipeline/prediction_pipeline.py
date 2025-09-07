from config.path_config import *
from utils.helper import *

def anime_based_recommendation(anime_name, n=10):
    """
    Content (item) based recommendation starting from an anime title.
    """
    try:
        similar_animes = find_similar_animes(
            anime_name,
            ANIME_WEIGHTS_PATH,
            ANIME2ANIME_ENCODED,
            ANIME2ANIME_DECODED,
            DF,
            n=n
        )
        if similar_animes is None or similar_animes.empty:
            return []
        return similar_animes["name"].head(n).tolist()
    except Exception as e:
        print(f"Anime recommendation error: {e}")
        return []

def hybrid_recommendation(user_id, user_weight=0.5, content_weight=0.5):
    """
    Hybrid recommendation combining user-based and content-based approaches.
    """
    try:
        # User Recommendation
        similar_users = find_similar_users(user_id, USER_WEIGHTS_PATH, USER2USER_ENCODED, USER2USER_DECODED)
        user_pref = get_user_preferences(user_id, RATING_DF, DF)
        user_recommended_animes = get_user_recommendations(similar_users, user_pref, DF, SYNOPSIS_DF, RATING_DF)
        
        user_recommended_anime_list = user_recommended_animes["anime_name"].tolist()

        # Content recommendation
        content_recommended_animes = []

        for anime in user_recommended_anime_list:
            similar_animes = find_similar_animes(anime, ANIME_WEIGHTS_PATH, ANIME2ANIME_ENCODED, ANIME2ANIME_DECODED, DF)

            if similar_animes is not None and not similar_animes.empty:
                content_recommended_animes.extend(similar_animes["name"].tolist())
        
        combined_scores = {}

        for anime in user_recommended_anime_list:
            combined_scores[anime] = combined_scores.get(anime, 0) + user_weight

        for anime in content_recommended_animes:
            combined_scores[anime] = combined_scores.get(anime, 0) + content_weight  

        sorted_animes = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

        return [anime for anime, score in sorted_animes[:10]]
    
    except Exception as e:
        print(f"Hybrid recommendation error: {e}")
        return []

def recommend(query, top_n=10):
    """
    Flexible entry point: query can be user_id (int) or anime title (str).
    """
    if query is None or str(query).strip() == "":
        return []
    
    query = str(query).strip()
    
    # Try user-based first
    try:
        user_id = int(query)
        return hybrid_recommendation(user_id)
    except ValueError:
        # It's an anime title - find best match first
        best_match = find_best_anime_match(query, DF)
        
        if best_match:
            return anime_based_recommendation(best_match, n=top_n)
        else:
            return []

