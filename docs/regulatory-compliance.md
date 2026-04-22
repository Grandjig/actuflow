# ActuFlow Regulatory Compliance

## Overview

ActuFlow supports multiple regulatory reporting standards for insurance liabilities and solvency calculations.

## Supported Standards

### IFRS 17 - Insurance Contracts

**Effective:** January 1, 2023 (most jurisdictions)

**Measurement Models:**

1. **Building Block Approach (BBA)** - Default for most contracts
   - Best Estimate Liability (BEL)
   - Risk Adjustment (RA)
   - Contractual Service Margin (CSM)

2. **Premium Allocation Approach (PAA)** - Simplified for short-duration
   - Liability for Remaining Coverage (LRC)
   - Liability for Incurred Claims (LIC)

3. **Variable Fee Approach (VFA)** - For participating contracts
   - Variable CSM based on policyholder share

**ActuFlow Implementation:**

```
Model Templates:
├── IFRS17_BBA_Life          # Life insurance - BBA
├── IFRS17_BBA_Health        # Health insurance - BBA  
├── IFRS17_PAA_ShortTerm     # Short-term contracts - PAA
└── IFRS17_VFA_Participating # Participating contracts - VFA
```

**Key Outputs:**
- Liability for Remaining Coverage (LRC)
- Liability for Incurred Claims (LIC)
- CSM Movement Analysis
- Insurance Revenue Calculation
- Insurance Service Expenses
- Investment Component Analysis

**Reports:**
- IFRS 17 Disclosure Report
- CSM Roll-Forward
- Analysis of Changes in Insurance Contract Balances
- Reconciliation of LRC and LIC

---

### Solvency II (European Union)

**Effective:** January 1, 2016

**Pillars:**
1. **Pillar 1** - Quantitative Requirements
2. **Pillar 2** - Governance and Supervision
3. **Pillar 3** - Reporting and Disclosure

**ActuFlow Implementation:**

**Technical Provisions:**
- Best Estimate (BE)
- Risk Margin (Cost of Capital approach: 6%)

**Capital Requirements:**
- Solvency Capital Requirement (SCR)
- Minimum Capital Requirement (MCR)

**Standard Formula Modules:**
```
SCR Calculation:
├── Market Risk
│   ├── Interest Rate Risk
│   ├── Equity Risk
│   ├── Property Risk
│   ├── Spread Risk
│   └── Currency Risk
├── Counterparty Default Risk
├── Life Underwriting Risk
│   ├── Mortality Risk
│   ├── Longevity Risk
│   ├── Disability Risk
│   ├── Lapse Risk
│   ├── Expense Risk
│   └── Catastrophe Risk
└── Operational Risk
```

**Reports:**
- Quantitative Reporting Templates (QRTs)
- Solvency and Financial Condition Report (SFCR)
- Regular Supervisory Report (RSR)
- Own Risk and Solvency Assessment (ORSA)

---

### US GAAP - Long Duration Targeted Improvements (LDTI)

**Effective:** January 1, 2023 (SEC filers)

**Key Changes from Previous US GAAP:**
1. Liability remeasurement using current assumptions
2. Standardized discount rate (upper-medium grade)
3. DAC amortization on constant basis
4. Market Risk Benefits at fair value

**ActuFlow Implementation:**

**Liability Components:**
- Liability for Future Policy Benefits (LFPB)
- Deferred Acquisition Costs (DAC)
- Market Risk Benefits (MRB)

**Net Premium Ratio Calculation:**
```
NPR = PV(Expected Benefits + Expenses) / PV(Expected Premiums)
```

**Reports:**
- Liability Roll-Forward
- Net Premium Ratio Analysis
- DAC Amortization Schedule
- Discount Rate Sensitivity
- Assumption Update Impact

---

### Local GAAP / Statutory

ActuFlow supports configurable local regulatory requirements:

**Common Statutory Bases:**
- NAIC Statutory (US)
- UK Solvency II
- OSFI LICAT (Canada)
- APRA (Australia)
- MAS (Singapore)

---

## Audit Trail Requirements

### Data Lineage

Every calculation result can be traced back to:
1. **Source Data**: Which policies were included
2. **Assumptions**: Which assumption set (version) was used
3. **Model**: Which model definition (version) was used
4. **Parameters**: Valuation date, reporting basis, etc.
5. **User**: Who triggered the calculation
6. **Timestamp**: When the calculation was run

### Change Tracking

**Assumption Changes:**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "user": "jane.actuary@company.com",
  "action": "update_assumption_table",
  "resource": "assumption_tables/uuid",
  "changes": {
    "rates.age_45.male": {
      "old": 0.0025,
      "new": 0.0023
    }
  }
}
```

**Approval Workflow:**
- All assumption changes require approval before use in regulatory calculations
- Approval chain is fully logged
- Rejected changes include rejection reason

### Retention Policy

| Data Type | Retention Period |
|-----------|------------------|
| Calculation Results | 10 years |
| Audit Logs | 10 years |
| Assumption History | Permanent |
| Generated Reports | 10 years |
| Raw Policy Data | Per client policy |

---

## Control Framework

### Segregation of Duties

| Role | Create Assumptions | Approve Assumptions | Run Calculations | Approve Reports |
|------|-------------------|--------------------|--------------------|------------------|
| Analyst | ✓ | ✗ | ✓ | ✗ |
| Senior Actuary | ✓ | ✓ | ✓ | ✗ |
| Chief Actuary | ✓ | ✓ | ✓ | ✓ |
| Auditor | ✗ (view only) | ✗ | ✗ | ✗ |

### Four-Eyes Principle

- Assumption sets must be approved by someone other than the creator
- Regulatory reports require sign-off before submission
- Material assumption changes require documented justification

### Reconciliation Controls

**Built-in reconciliation checks:**
- Policy count reconciliation (source vs. calculation)
- Premium reconciliation (in-force premiums)
- Reserve movement analysis (period-over-period)
- Cashflow projection totals

---

## Reporting Calendar

### Typical Quarter-End Process

```
Day 1-5:   Data extraction and validation
Day 5-10:  Assumption review and updates
Day 10-15: Calculation runs
Day 15-18: Results review and anomaly investigation
Day 18-22: Report generation and review
Day 22-25: Management sign-off
Day 25-30: Regulatory submission
```

### Automated Reminders

ActuFlow can send automated reminders for:
- Upcoming reporting deadlines
- Pending approval tasks
- Assumption review dates
- Data submission windows

---

## Validation Rules

### Data Quality Checks

**Policy Data:**
- Required fields populated
- Date consistency (issue ≤ effective ≤ maturity)
- Premium/sum assured within product limits
- Valid status transitions

**Assumption Data:**
- Rates between 0 and 1
- Monotonicity where expected (e.g., mortality by age)
- Consistency across tables

**Calculation Results:**
- Reserve ≥ 0 (for most products)
- NPR ≤ 100% initially
- SCR ≥ MCR
- BEL + RA + CSM = Total Liability

---

## AI Features and Regulatory Calculations

**Important**: AI features are strictly separated from regulatory calculations.

**AI CAN:**
- Suggest data corrections (human must approve)
- Flag anomalies for review (human must investigate)
- Generate draft narratives (human must review and edit)
- Assist with data mapping (human must confirm)

**AI CANNOT:**
- Directly modify calculation inputs
- Override assumption values
- Auto-approve any regulatory output
- Make decisions without human confirmation

All regulatory calculations use deterministic, auditable formulas.
