# Hybrid Anime Recommender System

![Anime Recommender](https://img.shields.io/badge/ML-Anime%20Recommender-ff69b4)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![Azure](https://img.shields.io/badge/Azure-Cloud-0089D6)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED)

An end-to-end hybrid anime recommendation system that combines collaborative filtering and content-based approaches to provide personalized anime recommendations to users.

## 🌟 Features

- **Hybrid Recommendation Engine**: Combines collaborative filtering with content-based filtering for more accurate recommendations
- **Large-scale Data Processing**: Ingests and preprocesses millions of user-anime ratings
- **Neural Network Model**: Embedding-based architecture optimized for recommendation quality
- **Experiment Tracking**: Integration with Comet ML for model performance monitoring
- **Cloud Integration**: Data pipeline with Azure Blob Storage
- **Production Deployment**: Dockerized application deployed as Azure Web App
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Azure Blob    │───>│  Data Pipeline  │───>│ Preprocessing   │
│    Storage      │    │                 │    │                 │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └────────┬────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Azure Web     │<───│  Docker Image   │<───│  Model Training │
│      App        │    │                 │    │   (Comet ML)    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Technologies

- **Data Storage**: Azure Blob Storage
- **Data Processing**: Python, Pandas, NumPy
- **Machine Learning**: TensorFlow/PyTorch, Neural Embeddings
- **Experiment Tracking**: Comet ML
- **Deployment**: Docker, Azure Web App
- **CI/CD**: GitHub Actions
- **Development**: Jupyter Notebooks

## 📋 Prerequisites

- Python 3.7+
- Azure subscription
- Docker
- Comet ML account

## 🚀 Setup and Installation

1. Clone the repository
   ```bash
   git clone https://github.com/raw9k/hybrid-anime-recommender.git
   cd hybrid-anime-recommender
   ```

2. Set up a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables for Azure and Comet ML
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## 📊 Data Pipeline

The system ingests anime rating data from Azure Blob Storage, containing millions of user-anime interactions. The pipeline performs:

1. Data extraction from Azure Blob
2. Preprocessing and cleaning
3. Feature engineering for content-based filtering
4. Train-test splitting for model evaluation

## 🧠 Model Architecture

The recommendation system is based on a hybrid approach:

- **Collaborative Filtering**: Neural network-based matrix factorization to learn user and anime embeddings
- **Content-Based Filtering**: Leverages anime metadata (genres, studios, etc.)
- **Hybrid Model**: Combines both approaches for more robust recommendations

## 🔍 Experiment Tracking

All model training experiments are tracked using Comet ML, monitoring:

- Training and validation metrics
- Hyperparameter tuning
- Model artifacts
- Recommendation quality metrics (RMSE, MAE, Precision, Recall)

## 🐳 Deployment

The model is deployed as a REST API using:

1. Docker containerization
2. Azure Web App hosting
3. GitHub Actions for CI/CD pipeline

## 📁 Repository Structure

```
hybrid-anime-recommender/
├── data/                      # Data processing scripts
├── notebooks/                 # Jupyter notebooks for exploration and development
├── src/                       # Source code
│   ├── preprocessing/         # Data preprocessing modules
│   ├── models/                # Model architecture definitions
│   ├── training/              # Training scripts
│   └── api/                   # API for model serving
├── tests/                     # Unit and integration tests
├── .github/workflows/         # GitHub Actions CI/CD configuration
├── Dockerfile                 # Docker configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 📈 Results

The hybrid recommendation system achieves improved performance compared to single-approach systems:

- Lower MSE and MAE for rating prediction
- Higher precision and recall for anime recommendations
- Better cold-start handling for new users and items

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Data sourced from publicly available anime datasets
- Thanks to the anime community for valuable feedback
