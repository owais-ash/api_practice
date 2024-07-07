# API Project: Text Analysis, Endpoint Health Check, and PDF Comparison

## Overview

This repository contains three APIs implemented in Python using Flask, each serving a specific purpose related to text analysis, endpoint health checking, and PDF comparison.

### APIs Included:

1. **Text Analysis API**
   - Analyzes input statements for incorrect spellings, profanity words, and extracts nouns in ascending order of length.

2. **Endpoint Health Check API**
   - Checks the availability of an API endpoint specified as a parameter and reports its status.

3. **PDF Comparison API**
   - Compares two versions of the same PDF document (formatted as text in blog format) to detect changes, grouping them by paragraph.

## Implementation Details

### API 01: Text Analysis API

- **Endpoint:** `/analyze_text`
- **Functionality:**
  - Identifies incorrect spellings using a spellchecker library.
  - Detects profanity words based on a predefined list.
  - Extracts and sorts nouns from the input text.

### API 02: Endpoint Health Check API

- **Endpoint:** `/check_endpoint`
- **Functionality:**
  - Checks the availability of an API endpoint provided as input.
  - Returns the queried timestamp, response code, and status (alive or not).

### API 03: PDF Comparison API

- **Endpoint:** `/compare_pdf`
- **Functionality:**
  - Compares two versions of a PDF document provided as text input.
  - Detects changes between the documents and groups them by paragraph.

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/owais-ash/api_practice
   cd api_practice

2. Run requirements.txt

   ```bash
   pip3 install requirements.txt

3. For api1.py and api3.py - Run the program and move to localhost link coming in console's output.
4. For api2.py - Run the program and paste localhost test link on browser
   ```bash
   http://127.0.0.1:5000/check_endpoint?endpoint=http://example.com

