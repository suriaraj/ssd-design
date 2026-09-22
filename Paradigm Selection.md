## Banking Transaction System

A banking application manages accounts, balances, deposits, withdrawals, and fund transfers. Multiple transactions can happen simultaneously, and incorrect handling of shared state could result in financial inconsistencies.

### Question:
How would you structure the program to manage state, business rules, and concurrent operations safely?

## Real-Time Event Processing

A system receives thousands of events per second from different sources. Each event may trigger multiple independent actions. The system must continue processing new events even when one action fails or takes longer than expected.

### Question:
How would you structure the application to process these events efficiently and independently?

## Infrastructure as Code

An organization manages hundreds of servers, databases, networks, and cloud resources. Engineers define the desired infrastructure configuration in source-controlled files. The system determines what needs to be created, modified, or removed to reach the desired state.

### Question:
How would you design the programming model for this system? What should the user's configuration describe, and how should the system translate that description into actual infrastructure changes?

## Cross-Cutting Concerns

A large application contains hundreds of business operations. The organization now requires the following behavior across many operations:

Log method entry and exit
Measure execution time
Perform authorization checks
Record audit information
Handle specific exceptions consistently

Adding this code manually to every method has resulted in duplicated code and inconsistent implementation.

### Question:
How would you design the application so that these concerns can be applied consistently across relevant operations without embedding the same logic into every business method?

Look for concepts such as:

Cross-cutting concerns
Aspects
Join points
Pointcuts
Advice
Interception
Separation of business logic from infrastructure concerns

## Frequently Changing Business Rules

A pricing system contains hundreds of business rules. New rules are introduced frequently, existing rules change regularly, and different customers may be subject to different combinations of rules.

### Question:
How would you design the program so that business rules can evolve without requiring significant changes to the core application?

## Large Data Processing

A system needs to process 10 million independent records. Each record goes through several steps:

Read → Validate → Transform → Filter → Calculate → Store

The processing of one record does not depend on another record.

### Question:
How would you structure the processing flow to make it reusable, testable, and capable of taking advantage of parallel execution?
