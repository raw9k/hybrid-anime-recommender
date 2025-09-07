import os

########### DATA INGESTION ##################
RAW_DIR = "artifacts/raw"
CONFIG_PATH = "config/config.yaml"

########### DATA PROCESSING ##################
PROCESSED_DIR = "artifacts/processed"
WEIGHTS_DIR = "artifacts/weights"
MODEL_DIR = "artifacts/model"

ANIMELIST_CSV = os.path.join(RAW_DIR, "animelist.csv")
ANIME_CSV = os.path.join(RAW_DIR, "anime.csv")
ANIMESYNOPSIS_CSV = os.path.join(RAW_DIR, "anime_with_synopsis.csv")

# Training data paths
X_TRAIN_ARRAY = os.path.join(PROCESSED_DIR, "X_train_array.pkl")
X_TEST_ARRAY = os.path.join(PROCESSED_DIR, "X_test_array.pkl")
Y_TRAIN = os.path.join(PROCESSED_DIR, "y_train.pkl")
Y_TEST = os.path.join(PROCESSED_DIR, "y_test.pkl")

# Processed dataframes
RATING_DF = os.path.join(PROCESSED_DIR, "rating_df.csv")
DF = os.path.join(PROCESSED_DIR, "df.csv")
SYNOPSIS_DF = os.path.join(PROCESSED_DIR, "synopsis_df.csv")

# Model weights (correct paths based on your structure)
ANIME_WEIGHTS_PATH = os.path.join(WEIGHTS_DIR, "anime_weights.pkl")
USER_WEIGHTS_PATH = os.path.join(WEIGHTS_DIR, "user_weights.pkl")

# Encodings (fix the typo: anim2anime -> anime2anime)
ANIME2ANIME_ENCODED = os.path.join(PROCESSED_DIR, "anim2anime_encoded.pkl")  # Note: your file has 'anim' not 'anime'
ANIME2ANIME_DECODED = os.path.join(PROCESSED_DIR, "anim2anime_decoded.pkl")  # Note: your file has 'anim' not 'anime'
USER2USER_ENCODED = os.path.join(PROCESSED_DIR, "user2user_encoded.pkl")
USER2USER_DECODED = os.path.join(PROCESSED_DIR, "user2user_decoded.pkl")

# Model path
MODEL_PATH = os.path.join(MODEL_DIR, "model.h5")