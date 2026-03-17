# dataOperations

This folder contains scripts responsible for data collection, parsing, preprocessing, and feature engineering used in the project.

## Contents

- **collect_isw_data.py**  
  Script for automated collection of raw data from ISW (Institute for the Study of War) reports.

- **ISW_parsing.py / isw_parsing2.py**  
  Scripts for parsing raw ISW data and extracting relevant structured information.

- **ISW_processing.ipynb**  
  Notebook for initial data cleaning, formatting, and exploratory analysis of the ISW dataset.

- **features_engineering.py**  
  Contains logic for generating new features, transforming variables, and preparing data for modeling.

- **forecast24.py**  
  Script for preparing time-based features and supporting short-term (24-hour) forecasting tasks.

## Purpose

The main goal of this folder is to transform raw and unstructured data into a clean, structured dataset suitable for machine learning models. It ensures consistency, reproducibility, and proper feature preparation across the project pipeline.
