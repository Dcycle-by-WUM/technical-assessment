# Repository Rules and Context

This document contains the rules and guidelines for working with this repository.

## Ignored Folders

The following folders should be ignored and not committed to the repository:
- `.venv` - Python virtual environments
- `node_modules` - Node.js dependencies
- `cdk.out` - AWS CDK output
- `build` - Build artifacts
- `dist` - Distribution artifacts

## Authentication and Access

- **AWS Authentication**: Use `awslogin` to authenticate AWS sessions and profiles.
- **Git Operations**: The preferred protocol for Git operations on GitHub is SSH.

## Repository Structure

This repository contains a technical assessment framework for engineering manager candidates with four separate challenges:

```
/
├── README.md                  # Main documentation and overview
├── CLAUDE.md                  # Repository guidelines and rules
├── .gitignore                 # Git ignore file for excluded directories and files
│
├── typescript-review/         # TypeScript code review challenge
│   ├── README.md              # Challenge description and instructions
│   ├── src/                   # Next.js application source code
│   │   ├── app/               # Next.js app directory
│   │   ├── components/        # React components with intentional issues
│   │   ├── hooks/             # Custom React hooks
│   │   └── utils/             # Utility functions
│   ├── public/                # Static assets
│   └── package.json           # Node.js dependencies
│
├── python-algorithm/          # Python algorithm implementation challenge
│   ├── README.md              # Challenge description and instructions
│   ├── app.py                 # Main Flask application
│   ├── recommendation/        # Recommendation algorithm package
│   │   ├── __init__.py
│   │   ├── algorithm.py       # Where candidates implement their solution
│   │   └── models.py          # Data models for the algorithm
│   ├── tests/                 # Unit tests for the algorithm
│   ├── data/                  # Sample data for algorithm testing
│   └── requirements.txt       # Python dependencies
│
├── infrastructure-fix/        # Infrastructure troubleshooting challenge
│   ├── README.md              # Challenge description and instructions
│   ├── infrastructure_fix/    # CDK stack definition
│   ├── lambda/                # Lambda function code with DynamoDB connection
│   ├── app.py                 # Main CDK application
│   └── requirements.txt       # Python dependencies for CDK
│
└── system-design/             # System design challenge
    ├── README.md              # Challenge description and instructions
    ├── SOLUTION_TEMPLATE.md   # Template for candidates to structure their response
    ├── CONSTRAINTS.md         # Technical constraints document
    └── references/            # Reference materials for the challenge
        ├── ARCHITECTURE_PATTERNS.md
        └── SECURITY_BEST_PRACTICES.md
```

## Challenge Configuration

Each challenge is designed to test different technical skills required for engineering managers:

1. **TypeScript Review**: Contains intentional issues related to TypeScript typing, security vulnerabilities, performance problems, and accessibility issues.

2. **Python Algorithm**: Requires implementation of a recommendation algorithm within a Flask API framework.

3. **Infrastructure Fix**: Contains deliberate IAM permission and configuration issues between a Lambda function and DynamoDB table.

4. **System Design**: Provides requirements for designing a mobile health application architecture with specific constraints.

## Technical Environment

### TypeScript Review
- Next.js 14+ with TypeScript
- Tailwind CSS for styling
- ESLint for linting

### Python Algorithm
- Python 3.9+
- Flask web framework
- pytest for testing

### Infrastructure Fix
- AWS CDK for infrastructure as code
- Python 3.9+
- AWS Lambda and DynamoDB services

### System Design
- Markdown-based documentation
- Reference architecture patterns and best practices

## Contribution Guidelines

When adding new features or making changes to this repository, please:

1. Respect the directory structure
2. Ensure all challenges have clear instructions and evaluation criteria
3. Keep README files updated with relevant information
4. Follow the rules specified in this document
5. Test challenges to ensure they work as expected
6. Document any new issues or anti-patterns that have been added intentionally
7. Maintain balance in challenge difficulty

## Maintenance

- Periodically update dependencies to keep challenges relevant
- Review and update challenge content to reflect current industry best practices
- Consider adding new challenges as technology evolves

This document will be updated as new rules or guidelines are established.

