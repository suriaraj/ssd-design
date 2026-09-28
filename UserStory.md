Input Values:
Deposit > 0
Withdraw > 0
Account creation Opening Deposit >= 500

Account:
When an account is created:
Minimum balance = ₹500
Overdraft limit = ₹500
Status = Active
Opening deposit provided by customer

Core:
AccountNumber
Balance
MinimumBalance
OverdraftAvailable
Status:
├─Active
├─Overdue
├─Suspended
├─Closed

Account
├─ Deposit()
├─ Withdraw()
├─ UpdateStatus()
├─ GetBalance()
└─ GetStatus()

Withdraw:
Balance = 300
Overdraft = 500
Withdraw 600
Use:
300 from balance
300 from overdraft
Remaining:
Balance = 0
Overdraft = 200

Deposits: Call UpdateStatus for one place logic, must be done after every deposit or withdraw
If Overdraft = 0
    -> Suspended

Else if Overdraft < 500
    -> Overdue

Else if Balance >= 500
    -> Active

Else
    -> Closed
