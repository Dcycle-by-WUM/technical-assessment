# Engineering Manager Technical Assessment Framework

This repository contains a comprehensive technical assessment framework designed to evaluate candidates for Engineering Manager positions. The assessment covers key technical competencies required for effective engineering leadership.

## Purpose

The goal of this framework is to provide a standardized, comprehensive, and fair way to assess technical competencies of Engineering Manager candidates. Rather than relying solely on traditional interviews, this framework allows candidates to demonstrate their technical skills in realistic scenarios that reflect the challenges they would face in the role.

The assessment is designed to evaluate:
- Technical depth and breadth of knowledge
- Problem-solving abilities
- Communication and documentation skills
- Decision-making and prioritization
- Understanding of best practices and tradeoffs

## Assessment Structure

The framework consists of four distinct challenges, each testing different aspects of engineering management:

### 1. TypeScript Code Review (`/typescript-review`)
A Next.js application with intentionally included issues for candidates to identify and provide feedback on. Tests code review skills, attention to detail, and ability to communicate technical concerns effectively.

**Key skills evaluated:**
- Identifying code quality issues
- Recognizing security vulnerabilities
- Spotting performance problems
- Providing constructive feedback
- Prioritizing issues by importance

### 2. Python Algorithm Implementation (`/python-algorithm`)
A Python API framework where candidates need to implement a specific algorithm. Tests problem-solving abilities, coding skills, and understanding of algorithmic complexity.

**Key skills evaluated:**
- Problem-solving approach
- Code organization and structure
- Algorithm efficiency and optimization
- Error handling and edge cases
- Testing methodology

### 3. Infrastructure Fix (`/infrastructure-fix`) 
A CDK application with a connection issue between DynamoDB and Lambda that needs to be identified and fixed. Tests cloud infrastructure knowledge, troubleshooting skills, and AWS expertise.

**Key skills evaluated:**
- Debugging infrastructure issues
- Understanding cloud services and their interactions
- Implementing security best practices
- Infrastructure as code competency
- Documentation of troubleshooting process

### 4. System Design Challenge (`/system-design`)
A challenge to design a mobile application architecture based on specific requirements. Tests system design knowledge, architectural thinking, and ability to make technology decisions.

**Key skills evaluated:**
- Architecture design principles
- Scalability and performance considerations
- Security and compliance awareness
- Technology selection rationale
- Trade-off analysis and decision making

## Instructions for Interviewers

### Preparation

1. Clone this repository to your local environment.
2. Review all challenges to understand the expected solutions and evaluation criteria.
3. Select the appropriate challenge(s) based on the specific role requirements and the candidate's background.
4. Ensure you have the necessary environment to review submissions (e.g., Node.js for the TypeScript challenge, Python for the algorithm challenge).

### Administration

1. **Initial Communication:**
   - Clearly explain the selected challenge(s) to the candidate
   - Provide a deadline for submission (typically 3-7 days)
   - Clarify expectations around time commitment
   - Communicate the evaluation criteria

2. **Providing the Challenge:**
   - Create a private copy of the selected challenge(s) for the candidate
   - Remove solution hints if present
   - Provide clear instructions for submission

3. **During the Challenge Period:**
   - Be available to answer clarifying questions
   - Do not provide technical guidance that would give away solutions

4. **Receiving Submissions:**
   - Accept submissions via your preferred method (email, private repository, etc.)
   - Confirm receipt and set expectations for feedback timeline

### Evaluation

1. Review the submission using the specific criteria in each challenge's README.md file.
2. Complete the evaluation rubric provided for each challenge.
3. Prepare specific questions based on the submission for follow-up discussion.
4. Schedule a follow-up interview to discuss the submission and your evaluation.

## Evaluation Guidelines

### General Scoring Approach

Each challenge includes a detailed scoring rubric in its README.md file. In general, evaluate submissions on a scale of 1-5 in each criterion:

1. **Unsatisfactory** - Does not meet basic requirements
2. **Needs Improvement** - Meets some requirements with significant gaps
3. **Satisfactory** - Meets basic requirements adequately
4. **Strong** - Exceeds requirements in some areas
5. **Exceptional** - Demonstrates mastery and exceeds requirements

### Holistic Evaluation

In addition to specific technical criteria, consider these aspects across all challenges:

- **Communication Quality:** How clearly does the candidate explain their approach?
- **Attention to Detail:** How thorough and precise is the submission?
- **Engineering Judgment:** Does the candidate make reasonable tradeoffs and prioritize effectively?
- **Best Practices:** Does the solution follow industry standards and best practices?

### Red Flags

Watch for these concerning patterns across submissions:

- Solutions that appear to be AI-generated without critical thinking
- Lack of explanation for key decisions
- Dismissing non-functional requirements (security, scalability, etc.)
- Inability to prioritize issues by importance
- Over-engineering simple problems or under-engineering complex ones

## Customization

This framework is designed to be customizable based on your organization's specific needs:

- Modify challenge difficulty based on role seniority
- Add or remove challenges based on specific technical domains
- Adjust evaluation criteria to align with your organization's values and priorities

## Contribution

When contributing to this framework, please refer to the CLAUDE.md file for guidelines and rules.

## License

[Include appropriate license information here]

