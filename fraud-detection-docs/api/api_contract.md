# API Contract

## Base URL

`/api/v1`

## Create Transaction

- **Method:** `POST`
- **Path:** `/transactions`
- **Purpose:** Stores a transaction after fraud risk evaluation

## Preview Fraud Score

- **Method:** `POST`
- **Path:** `/fraud/score`
- **Purpose:** Returns risk decision without storing the transaction

## Get Transaction By External ID

- **Method:** `GET`
- **Path:** `/transactions/{external_id}`

## Fraud Summary

- **Method:** `GET`
- **Path:** `/fraud/summary`
