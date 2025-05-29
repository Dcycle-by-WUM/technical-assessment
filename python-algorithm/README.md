# Python Algorithm Implementation Challenge

## Overview

This challenge assesses your algorithmic thinking and problem-solving skills - essential competencies for engineering managers who need to guide their teams through complex technical problems. You will implement an algorithm within the context of a Python API.

## Challenge Description

You are leading a team that needs to implement a new feature for the company's recommendation system. The feature requires an efficient algorithm to process user data and generate personalized recommendations.

Your task is to:

1. Implement an algorithm that solves the problem described below
2. Integrate it into the provided API framework
3. Ensure the solution is efficient, readable, and well-tested

## Problem Statement

**Task**: Implement a recommendation algorithm that identifies potential product matches based on user browsing history.

Given:
- A dataset of user browsing histories (provided as a JSON file)
- A set of product categories and their relationships
- A list of business rules that influence recommendations

The algorithm should:
1. Analyze a user's browsing history to identify patterns
2. Generate a ranked list of product recommendations
3. Apply business rules to filter and prioritize the recommendations
4. Return the top N recommendations for the user

## API Integration

The skeleton API has endpoints for:
- Retrieving user browsing history
- Submitting recommendations
- Accessing product category data

You need to implement the algorithm and integrate it with these endpoints.

## Evaluation Criteria

Your solution will be evaluated based on:

1. **Correctness** - Does the algorithm produce the expected results?
2. **Efficiency** - How well does it perform with large datasets?
3. **Code quality** - Is the code well-structured, readable, and maintainable?
4. **Testing** - Is the solution thoroughly tested?
5. **Documentation** - Is the implementation well-documented?
6. **Problem-solving approach** - How did you approach and solve the problem?

## Submission Guidelines

1. Implement your solution in the provided project structure
2. Include unit tests that verify the correctness of your algorithm
3. Document your approach, any assumptions made, and how to run your solution
4. Provide a brief analysis of the time and space complexity of your algorithm

## Time Expectation

We expect this challenge to take approximately 2-3 hours to complete.

## Getting Started

1. Set up a Python virtual environment
2. Install the required dependencies
3. Explore the API structure and the provided data
4. Implement your algorithm and integrate it with the API

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API server
python app.py
```

The API will be available at http://localhost:5000

