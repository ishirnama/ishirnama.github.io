---
title: "ML Approaches for Music Genre Classification"
collection: portfolio
permalink: /portfolio/portfolio-4/
excerpt: "Training and comparing four machine learning models to classify music genres using the GTZAN dataset."
---

## Machine Learning Applications Coursework : ML Approaches for Music Genre Classification

This project explores the use of machine learning algorithms to classify music into genres. Music genre classification is used by streaming services like Spotify and YouTube Music to organise and recommend content. The goal was to train, evaluate, and compare four different ML models on the same dataset, and to investigate how using pre-trained audio embeddings affects each model's performance.

## Dataset

The dataset used is GTZAN, a widely-used benchmark for music genre classification containing 1,000 audio files across 10 genres (blues, classical, country, disco, hiphop, jazz, metal, pop, reggae, rock), with 100 files per genre.

Before training, the data required several cleaning steps:
- Corrupted files were detected and removed using a try-except loop
- Sample rates were resampled from 22,050 Hz to 16,000 Hz to match VGGish's requirements
- Each audio file was trimmed to 5 seconds

The cleaned data was split into training (70%), validation (15%), and test (15%) sets, then standardised using `StandardScaler` so that all features lie on the same scale. This is important for distance-based models like kNN and gradient-descent-based models like logistic regression, where unscaled features can cause instability.

## VGGish Audio Embeddings

A key part of this project was testing each model both with and without VGGish audio embeddings. VGGish is a pre-trained neural network developed by Google that converts raw audio into compact 128-dimensional feature vectors capturing high-level patterns in sound. Using these embeddings instead of raw audio features consistently improved every model's accuracy by roughly 20%, demonstrating how important feature quality is in audio classification tasks.

## Models

### Dummy Classifier (Baseline)

The dummy classifier always predicts the most frequent class ("blues") regardless of the input. It serves as a baseline to confirm that the other models are actually learning something meaningful.

| | Test Accuracy | Validation Accuracy |
|---|---|---|
| Dummy Classifier | 10.00% | 10.01% |
| Dummy Classifier (VGGish) | 10.00% | 10.01% |

As expected, it achieves around 10% accuracy — equivalent to random guessing across 10 genres. Every other model substantially outperformed this baseline.

### Logistic Regression

Logistic regression works by iteratively adjusting weights and biases using gradient descent to minimise a loss function. It is a strong baseline for multi-class classification problems.

| | Test Accuracy | Validation Accuracy |
|---|---|---|
| Logistic Regression | 55.11% | 55.17% |
| Logistic Regression (VGGish) | 77.22% | 79.87% |

Without embeddings the model struggles with genres that share similar sonic features — rock is the weakest category, with many samples misclassified as country, disco, or reggae. Classical is the strongest, reaching a diagonal score of 85. After adding VGGish embeddings, validation accuracy jumps to nearly 80%, making it competitive with the top models.

### Gaussian Naive Bayes

Naive Bayes is a probabilistic classifier that selects the genre with the highest posterior probability given the input features. A Gaussian variant was used because audio features are continuous rather than discrete.

| | Test Accuracy | Validation Accuracy |
|---|---|---|
| Naive Bayes | 44.67% | 43.49% |
| Naive Bayes (VGGish) | 71.78% | 69.30% |

Naive Bayes performed the worst of the four proper models. The likely reason is its core assumption of conditional independence between features — in practice, audio features like spectral centroid, zero-crossing rate, and mean squared energy are correlated with each other, which violates this assumption. The confusion matrices show it struggling particularly with jazz without embeddings (diagonal score of 25), which improves dramatically to 72 after adding VGGish features.

### Neural Network (MLP)

The neural network was implemented as a multi-layer perceptron with two hidden layers of 64 neurons each, using ReLU activation and the Adam optimiser, trained for up to 500 iterations.

| | Test Accuracy | Validation Accuracy |
|---|---|---|
| Neural Network | 68.89% | 71.75% |
| Neural Network (VGGish) | 80.56% | 80.87% |

The MLP achieved the highest overall accuracy, with and without embeddings. Even without VGGish features, the diagonal of its confusion matrix is noticeably cleaner than the other models, indicating more consistent performance across genres.

### K-Nearest Neighbors

kNN classifies a sample by finding the k closest training points in feature space (using Euclidean distance) and taking the most common label among them.

| | Test Accuracy | Validation Accuracy |
|---|---|---|
| K-Nearest Neighbors | 74.11% | 75.31% |
| K-Nearest Neighbors (VGGish) | 77.67% | 80.76% |

kNN achieved the highest accuracy of any model *without* embeddings, outperforming even the neural network at that stage. With embeddings it was only narrowly beaten by the MLP in validation accuracy. It was particularly strong at classifying classical and metal, and after adding VGGish features, jazz classification also improved significantly.

## Results Summary

| Model | Test Acc. (raw) | Test Acc. (VGGish) |
|---|---|---|
| Dummy Classifier | 10.00% | 10.00% |
| Naive Bayes | 44.67% | 71.78% |
| Logistic Regression | 55.11% | 77.22% |
| Neural Network | 68.89% | **80.56%** |
| K-Nearest Neighbors | **74.11%** | 77.67% |

## Key Findings

The most consistent trend across all models was the improvement from VGGish embeddings — typically around 20 percentage points. This highlights how critical feature extraction is in audio-based ML tasks: even a relatively simple model like logistic regression can reach nearly 80% accuracy when given well-structured input features.

The two supervised learning models (NN and kNN) outperformed the others, which is expected — they can learn complex, non-linear boundaries between genres rather than relying on simplifying assumptions like conditional independence. Naive Bayes was the weakest real model for exactly this reason.

Rock was consistently the hardest genre to classify across all models, likely because it shares tempo, instrumentation, and spectral characteristics with several other genres. Classical was the easiest, with its distinctive harmonic and dynamic profile making it stand out clearly in feature space.

## Tools Used

- Python, NumPy, Pandas, Scikit-learn
- Librosa (audio processing)
- VGGish (Google pre-trained audio embedding model)
- Matplotlib, Seaborn
- GTZAN dataset
