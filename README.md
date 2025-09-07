# 🎌 Hybrid Anime Recommendation System

An end-to-end hybrid anime recommendation system that combines collaborative and content-based filtering to provide personalized anime recommendations. The system ingests large-scale user-anime ratings from Azure Blob Storage, processes and encodes the data, trains an embedding-based neural network model, and deploys via Dockerized Azure Web App with CI/CD using GitHub Actions.

---

## 🛠 Project Overview

This project implements a full machine learning pipeline including:

1. **Data Ingestion**  
   - Downloads multiple CSV datasets from **Azure Blob Storage**.  
   - Handles large files efficiently and ensures robust error handling.

2. **Data Processing**  
   - Filters users with insufficient ratings.  
   - Normalizes ratings and encodes users/animes.  
   - Splits data into training and testing sets.  
   - Saves artifacts for training and recommendation.

3. **Model Development**  
   - Embedding-based neural network using **Keras**.  
   - Combines collaborative filtering with content-based recommendations.  
   - Model configuration managed via YAML.

4. **Model Training**  
   - Training with **callbacks**: ModelCheckpoint, LearningRateScheduler, EarlyStopping.  
   - Experiment tracking with **Comet ML**.  
   - Saves model weights and embeddings for users and animes.

5. **Recommendation Engine**  
   - Content-based recommendation using anime embeddings.  
   - User-based recommendation using similarity among user embeddings.  
   - Fuzzy string matching for anime name queries.  

6. **Deployment**  
   - Dockerized **Azure Web App** deployment.  
   - CI/CD pipeline implemented via **GitHub Actions** for automated builds and updates.

---

## 🚀 Features

- Personalized anime recommendations based on user history and anime content.  
- Handles millions of records efficiently.  
- Interactive recommendation via user or anime input.  
- Continuous model updates with CI/CD.  

---

## 💻 Tech Stack

**Python, Comet ML, GitHub Actions, Docker, Azure Web App and Containers**  

Libraries used: `pandas`, `numpy`, `tensorflow`, `keras`, `joblib`, `difflib`,`azure-storage-blob`
