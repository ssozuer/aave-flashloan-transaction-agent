# AAVE Flash Loan Transaction Agent

## Description

This agent detects flash loan transactions if the loan amount >= $30M

## Supported Chains

- Ethereum

## Alerts

The following describes the agent alert structure.

- AAVE-4
  - Fired when a flash loan transaction is bigger thant $30M
  - Severity is always set to "high" 
  - Type is always set to "suspicious" 
  - Metadata fields:
    - "transaction_amount_in_eth": Total asset amount in ETH
    - "transaction_amount_in_usd": Total assent amount in USD

