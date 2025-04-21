# Contract Pricing Model
This project implements a contract pricing model to calculate various financial metrics, including prepay, POD (Point of Delivery), average cost per ton, cash flows, and IRR (Internal Rate of Return) for corporate contracts. The model uses data from an SQLite database and performs calculations based on user-defined parameters.

## Features
- Discount Rate Calculation: Calculates top and bottom discount rates based on contract length, spread type, and overall rating.
- RA Price Calculation: Computes the Risk Adjustment (RA) price for contracts.
- Prepay and POD Calculations: Determines prepay volumes, POD volumes, and average costs per ton.
- Cash Flow Calculation: Computes yearly cash flows for contracts, including ROFR (Right of First Refusal) costs and revenues.
- IRR Calculation: Calculates the Internal Rate of Return (IRR) for contracts over a 10-year period.
- Data Loading: Loads contract pricing and spread data from an SQLite database.

## Installation

1. Install the required Python packages:
`pip install pandas numpy-financial openpyxl`

2. Ensure the SQLite database (`risk_model.db`) is located in the data directory.

## Usage
Execute the contract_pricing.py script to calculate financial metrics:
`python contract_pricing.py`

## Output

- Results are printed to the console.
- Results are saved as an Excel file in the output directory with a timestamped filename.