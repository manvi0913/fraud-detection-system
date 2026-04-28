# Fraud Detection System Project Report

## Title

**Fraud Detection System Using Python, FastAPI, and MySQL**

## Abstract

Digital financial transactions have increased rapidly with the growth of e-commerce, online banking, UPI platforms, and card-based payments. Along with this growth, fraudulent activities have also become more frequent and sophisticated. The objective of this project is to design and implement a real-time fraud detection system capable of receiving financial transaction data, analyzing suspicious patterns, assigning a fraud risk score, and storing the results for monitoring and reporting.

The proposed system is built using **Python**, **FastAPI**, and **MySQL**. It performs lightweight real-time risk analysis using rule-based scoring logic that considers factors such as transaction amount, transaction velocity, device changes, country mismatch, merchant risk, and unusual transaction time. The project also includes an offline machine learning pipeline for experimentation and future enhancement.

## Objectives

- build a real-time backend system for transaction ingestion and fraud scoring
- store transactions and fraud decisions in a relational database
- design REST APIs for transaction processing and monitoring
- apply fraud indicators such as velocity and geo-location mismatch
- support future ML-based model integration

## Core APIs

1. `POST /api/v1/transactions`
2. `POST /api/v1/fraud/score`
3. `GET /api/v1/transactions/{external_id}`
4. `GET /api/v1/fraud/summary`

## Conclusion

The Fraud Detection System demonstrates how modern backend technologies can be used to build a meaningful real-time fraud monitoring platform. The project combines API development, database persistence, analytical logic, and model experimentation into a practical academic solution.
