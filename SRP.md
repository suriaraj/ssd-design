MODE: ALGORITHM  TIER: E3  ROUTED: code-specialist (GPT-5.3-Codex)  REASON: Non-trivial refactor of existing C# code to enforce Single Responsibility Principle while meeting explicit complexity/testability constraints. 

Refactor Account class for SRP

Read 

## Applying SRP to this `Account` class

**What SRP means here:** the original `Account` class had five distinct reasons to change bundled together: (1) holding state, (2) withdraw/deposit orchestration, (3) overdraft arithmetic, (4) the status-transition state machine, and (5) the individual status predicates — plus `Main` mixing domain logic invocation with console I/O. SRP means splitting each of those into its own class so each one only changes for one reason.

**Result of the split:**

| Class | Single Responsibility |
|---|---|
| `Account` | Pure state holder (balance, overdraft, status, minBalance) |
| `AccountTransactionService` | Orchestrates withdraw/deposit: guard checks + calling the calculator/evaluator |
| `OverdraftCalculator` | Pure math for how a withdrawal/deposit affects balance vs. overdraft |
| `AccountStatusEvaluator` | Status state-machine transition logic (data-driven rule table instead of nested if/else) |
| `AccountStatusPredicates` | The four boolean rules (`IsActive`, `IsSuspended`, `IsOverdue`, `IsClosedFromActive`) |
| `AccountFinancialState` | Small value type to pass balance+overdraft together without side effects |
| `Program.Main` | Composition root + console I/O only |

Behavior, exception messages, and the exact status-transition order are unchanged.

```csharp
using System;
using System.Collections.Generic;

namespace ConsoleApp3
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.ReadLine();

            var account = new Account(1000);
            var predicates = new AccountStatusPredicates();
            var statusEvaluator = new AccountStatusEvaluator(predicates);
            var overdraftCalculator = new OverdraftCalculator();
            var transactionService = new AccountTransactionService(overdraftCalculator, statusEvaluator);

            transactionService.Withdraw(account, 1100);

            Console.WriteLine(
                "Account Balance is: " + account.GetBalance() +
                " AND Account Status is : " + account.GetStatus() +
                " AND Account OD balance now is : " + account.GetOverdueAmount());

            Console.ReadLine();
        }
    }

    public sealed class Account
    {
        internal int CurrentBalance { get; private set; }
        internal int CurrentOverdueAmount { get; private set; }
        internal int MinBalance { get; }
        internal AccountStatus CurrentStatus { get; private set; }

        public Account(int openingBalance)
        {
            CurrentBalance = openingBalance;
            CurrentOverdueAmount = 500;
            MinBalance = 500;
            CurrentStatus = AccountStatus.Active;
        }

        internal void ApplyFinancialState(AccountFinancialState state)
        {
            CurrentBalance = state.Balance;
            CurrentOverdueAmount = state.OverdueAmount;
        }

        internal void ApplyStatus(AccountStatus status) => CurrentStatus = status;

        internal int GetBalance() => CurrentBalance;
        internal AccountStatus GetStatus() => CurrentStatus;
        internal int GetOverdueAmount() => CurrentOverdueAmount;
    }

    public sealed class AccountTransactionService
    {
        private readonly OverdraftCalculator overdraftCalculator;
        private readonly AccountStatusEvaluator statusEvaluator;

        public AccountTransactionService(OverdraftCalculator overdraftCalculator, AccountStatusEvaluator statusEvaluator)
        {
            this.overdraftCalculator = overdraftCalculator;
            this.statusEvaluator = statusEvaluator;
        }

        internal void Withdraw(Account account, int amount)
        {
            if (account.CurrentStatus == AccountStatus.Closed)
                throw new Exception("Cannot Withdraw the amount requested...Account is CLOSED state");

            if (amount > account.CurrentBalance + account.CurrentOverdueAmount)
                throw new Exception("Cannot Withdraw the amount requested...");

            var next = overdraftCalculator.ApplyWithdrawal(account.CurrentBalance, account.CurrentOverdueAmount, amount);
            account.ApplyFinancialState(next);
            account.ApplyStatus(statusEvaluator.Evaluate(account));
        }

        internal void Deposit(Account account, int amount)
        {
            if (account.CurrentStatus == AccountStatus.Closed)
                throw new Exception("Cannot Withdraw the amount requested...Account is CLOSED state");

            var next = overdraftCalculator.ApplyDeposit(account.CurrentBalance, account.CurrentOverdueAmount, amount);
            account.ApplyFinancialState(next);
            account.ApplyStatus(statusEvaluator.Evaluate(account));
        }
    }

    public sealed class OverdraftCalculator
    {
        internal AccountFinancialState ApplyWithdrawal(int balance, int overdueAmount, int amount)
        {
            if (balance > amount)
                return new AccountFinancialState(balance - amount, overdueAmount);

            return new AccountFinancialState(0, overdueAmount + (balance - amount));
        }

        internal AccountFinancialState ApplyDeposit(int balance, int overdueAmount, int amount)
        {
            if (overdueAmount < 500)
            {
                var updatedOverdue = overdueAmount + amount;
                return new AccountFinancialState(updatedOverdue - 500, 500);
            }

            return new AccountFinancialState(balance + amount, overdueAmount);
        }
    }

    public sealed class AccountStatusEvaluator
    {
        private readonly Dictionary<AccountStatus, StatusRule[]> rulesByState;

        public AccountStatusEvaluator(AccountStatusPredicates predicates)
        {
            // Rule tables encode the exact original if/else transition order per state.
            rulesByState = new Dictionary<AccountStatus, StatusRule[]>
            {
                { AccountStatus.Active, new[]
                    {
                        new StatusRule(a => predicates.IsClosedFromActive(a.CurrentBalance, a.MinBalance, a.CurrentOverdueAmount), AccountStatus.Closed),
                        new StatusRule(a => predicates.IsOverdue(a.CurrentOverdueAmount), AccountStatus.Overdue),
                        new StatusRule(a => predicates.IsSuspended(a.CurrentOverdueAmount), AccountStatus.Suspended),
                        new StatusRule(_ => true, AccountStatus.Active)
                    }
                },
                { AccountStatus.Suspended, new[]
                    {
                        new StatusRule(a => predicates.IsActive(a.CurrentBalance, a.MinBalance), AccountStatus.Active),
                        new StatusRule(a => predicates.IsOverdue(a.CurrentOverdueAmount), AccountStatus.Overdue),
                        new StatusRule(_ => true, AccountStatus.Suspended)
                    }
                },
                { AccountStatus.Overdue, new[]
                    {
                        new StatusRule(a => predicates.IsActive(a.CurrentBalance, a.MinBalance), AccountStatus.Active),
                        new StatusRule(a => predicates.IsSuspended(a.CurrentOverdueAmount), AccountStatus.Suspended),
                        new StatusRule(_ => true, AccountStatus.Overdue)
                    }
                }
            };
        }

        internal AccountStatus Evaluate(Account account)
        {
            if (!rulesByState.TryGetValue(account.CurrentStatus, out var rules))
                return account.CurrentStatus;

            return EvaluateRules(rules, account);
        }

        private static AccountStatus EvaluateRules(StatusRule[] rules, Account account)
        {
            foreach (var rule in rules)
            {
                if (rule.IsMatch(account))
                    return rule.NextStatus;
            }

            return account.CurrentStatus;
        }
    }

    public sealed class AccountStatusPredicates
    {
        internal bool IsActive(int balance, int minBalance) => balance > minBalance;
        internal bool IsSuspended(int overdueAmount) => overdueAmount == 0;
        internal bool IsOverdue(int overdueAmount) => overdueAmount < 500;
        internal bool IsClosedFromActive(int balance, int minBalance, int overdueAmount) => balance < minBalance + overdueAmount;
    }

    public sealed class StatusRule
    {
        public StatusRule(Func<Account, bool> isMatch, AccountStatus nextStatus)
        {
            IsMatch = isMatch;
            NextStatus = nextStatus;
        }

        public Func<Account, bool> IsMatch { get; }
        public AccountStatus NextStatus { get; }
    }

    public readonly struct AccountFinancialState
    {
        public AccountFinancialState(int balance, int overdueAmount)
        {
            Balance = balance;
            OverdueAmount = overdueAmount;
        }

        public int Balance { get; }
        public int OverdueAmount { get; }
    }

    public enum AccountStatus { Active, Closed, Suspended, Overdue }
}
```

**Complexity check** (all methods ≤ 3):
- `AccountTransactionService.Withdraw` = 3, `.Deposit` = 2
- `OverdraftCalculator.ApplyWithdrawal` = 2, `.ApplyDeposit` = 2
- `AccountStatusEvaluator.Evaluate` = 2, `.EvaluateRules` = 3
- Predicates, constructors, accessors = 1 each

**Testability gained:** `OverdraftCalculator`, `AccountStatusEvaluator`, and `AccountStatusPredicates` are now pure/stateless and unit-testable without touching `Console` or constructing a full `Account` transaction flow — you can test the state machine and math independently of I/O.
