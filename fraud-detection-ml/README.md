# Fraud Detection ML Pipeline

This repository-style module contains the **offline experimentation pipeline** for fraud detection. It complements the FastAPI backend by preparing data, engineering features, and training a simple classification model that can later be integrated into live scoring.

## Workflow

1. Generate or load a dataset
2. Prepare features such as amount band, velocity, geo mismatch, and device change
3. Train a baseline model
4. Save the trained model and metrics
5. Compare model output with rule-based scoring used in the API module
