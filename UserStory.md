# Account Requirements

## Input Values
- Deposit > 0
- Withdraw > 0
- Account creation opening deposit >= 500

## Account Rules
When an account is created:

- Minimum balance = ₹500
- Overdraft limit = ₹500
- Status = Active
- Opening deposit provided by customer

## Core Account Fields
- AccountNumber
- Balance
- MinimumBalance
- OverdraftAvailable
- Status:
  - Active
  - Overdue
  - Suspended
  - Closed

## Account Operations
- Deposit()
- Withdraw()
- UpdateStatus()
- GetBalance()
- GetStatus()

## Withdraw Example
- Balance = 300
- Overdraft = 500
- Withdraw 600

### Usage
- 300 from balance
- 300 from overdraft

### Remaining
- Balance = 0
- Overdraft = 200

## Status Update Rule
Deposits: call `UpdateStatus()` for one-place logic, and do it after every deposit or withdraw.

```text
If Overdraft = 0
    -> Suspended

Else if Overdraft < 500
    -> Overdue

Else if Balance >= 500
    -> Active

Else
    -> Closed
```
