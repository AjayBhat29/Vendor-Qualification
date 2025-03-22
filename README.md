# Vendor Qualification System

A lightweight system that processes a CSV file of software vendors, evaluates them based on feature similarity, and ranks them accordingly.

## Overview

This system allows users to find the most relevant software vendors based on:

- Software category (e.g., "Accounting & Finance Software")
- Required capabilities/features (e.g., "Budgeting")

The system uses text similarity algorithms to match vendor features with user requirements and ranks vendors based on both feature similarity and overall vendor rating.

## Features

- Data processing and ingestion from CSV files
- Multiple similarity scoring methods (TF-IDF, SBERT, OpenAI embeddings)
- Configurable similarity thresholds
- Vendor ranking based on weighted scores
- RESTful API for vendor qualification

## Project Structure

- `app.py`: Main application entry point
- `config.py`: Configuration settings
- `data/`: Directory for data files
- `src/`: Source code modules
  - `data_processing.py`: Data loading and preprocessing
  - `similarity.py`: Similarity calculation methods
  - `ranking.py`: Vendor ranking logic
  - `api.py`: API endpoints
