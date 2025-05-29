# Technical Assessment Framework

Welcome to our Technical Assessment Framework! This repository contains a set of challenges designed to evaluate different aspects of software engineering skills. Each challenge focuses on a specific area of expertise, allowing candidates to demonstrate their technical knowledge, problem-solving approach, and coding practices.

## Overview

This assessment consists of four distinct challenges:

1. **TypeScript Code Review** - Review and improve a Next.js application with intentional code issues
2. **Python Algorithm Implementation** - Implement a specific algorithm within a provided API scaffold
3. **Infrastructure Fix** - Troubleshoot and resolve issues in a CDK application with DynamoDB and Lambda
4. **System Design** - Design the architecture for a mobile application based on provided requirements

## How to Proceed

1. Fork this repository to your own GitHub account
2. Create a separate branch for each challenge you attempt
3. Complete the challenges according to the instructions below
4. Create a pull request for each challenge when ready to submit
5. Ensure your code follows best practices and includes appropriate documentation

## Challenges

### 1. TypeScript Code Review Challenge

**Location:** `/typescript-review`

**Objective:** Review a Next.js application that contains several intentional code issues, anti-patterns, and performance problems. Identify and fix these issues while maintaining the application's functionality.

**Setup:**
```bash
cd typescript-review
npm install
npm run dev
```

**Requirements:**
- Identify and fix at least 5 code issues (performance issues, anti-patterns, etc.)
- Improve type safety throughout the application
- Document each issue and your solution in the PR description
- Ensure all functionality continues to work as expected

**Evaluation Criteria:**
- Thoroughness of code review
- Quality of solutions implemented
- Code clarity and maintainability
- TypeScript best practices

### 2. Python Algorithm Implementation

**Location:** `/python-algorithm`

**Objective:** Implement a specific algorithm within a provided API scaffold to solve the stated problem.

**Setup:**
```bash
cd python-algorithm
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Requirements:**
- Implement the algorithm described in the challenge details
- Ensure your solution handles all edge cases
- Optimize for both time and space complexity
- Write comprehensive tests for your implementation
- Document your approach and any trade-offs made

**Evaluation Criteria:**
- Correctness of implementation
- Algorithm efficiency
- Code organization and readability
- Test coverage
- Documentation quality

### 3. Infrastructure Fix Challenge

**Location:** `/infrastructure-fix`

**Objective:** Troubleshoot and fix issues in a CDK application that has misconfigured DynamoDB-Lambda connections and permission problems.

**Setup:**
```bash
cd infrastructure-fix
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Requirements:**
- Identify and fix all infrastructure configuration issues
- Ensure proper permissions between Lambda and DynamoDB
- Address any security concerns
- Document all issues found and fixes applied
- Make the infrastructure deployable without errors

**Evaluation Criteria:**
- Ability to identify infrastructure issues
- Quality of solutions implemented
- Security best practices
- AWS/CDK knowledge
- Documentation of changes

### 4. System Design Challenge

**Location:** `/system-design`

**Objective:** Design a scalable, maintainable architecture for a mobile application based on the provided requirements.

**Requirements:**
- Review the requirements document in the system-design folder
- Create architecture diagrams showing the system components
- Document API designs, data models, and technology choices
- Address scaling, security, and performance considerations
- Explain your design decisions and any trade-offs made

**Evaluation Criteria:**
- Architecture clarity and completeness
- Scalability considerations
- Security best practices
- Quality of documentation
- Justification of technical decisions

## Submission Guidelines

For each challenge:

1. Create a separate branch named `solution/[challenge-name]` (e.g., `solution/typescript-review`)
2. Make your changes and commit them with clear, descriptive commit messages
3. Create a pull request against the main branch
4. In the PR description, include:
   - A summary of your changes
   - Any assumptions you made
   - Challenges you encountered and how you solved them
   - Instructions for running/testing your solution (if applicable)

## Time Expectations

While there is no strict time limit, we recommend spending:
- 1-2 hours on the TypeScript challenge
- 1-2 hours on the Python algorithm
- 1-2 hours on the infrastructure fix
- 1-2 hours on the system design

You are not required to complete all challenges. Choose the ones that best showcase your skills or complete as many as you wish.

## Evaluation Process

Each challenge will be evaluated by our engineering team based on the criteria listed above. We value:
- Clean, maintainable code
- Clear documentation
- Thoughtful problem-solving
- Attention to detail
- Best practices appropriate to each technology

We're more interested in your approach and thought process than in perfect solutions. Don't hesitate to document assumptions or alternative approaches you considered.

## Questions

If you have any questions about the challenges or the submission process, please reach out to the hiring team. We're happy to provide clarification.

Good luck!
