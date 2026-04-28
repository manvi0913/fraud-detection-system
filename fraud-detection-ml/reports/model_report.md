# Model Report

## Objective

The offline model pipeline is designed to support the live fraud detection backend by providing a simple classification baseline for suspicious transaction detection.

## Features Used

- transaction amount
- transaction hour
- number of transactions in the last 1 hour
- country mismatch
- device change
- merchant risk category
- international transaction flag

## Baseline Model

- Model: Random Forest Classifier
- Purpose: fast experimentation and easy interpretation
- Role in project: offline comparison against rule-based real-time scoring
