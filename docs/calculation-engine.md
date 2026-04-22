# ActuFlow Calculation Engine

## Overview

The calculation engine is the core of ActuFlow's actuarial functionality. It executes deterministic, auditable calculations for reserving, pricing, cash flow projections, and valuations.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CALCULATION ENGINE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────┐   │
│  │   Celery    │────>│   Task      │────>│    Executor         │   │
│  │   Worker    │     │   Router    │     │                     │   │
│  └─────────────┘     └─────────────┘     │  • Load model def   │   │
│                                          │  • Load assumptions │   │
│                                          │  • Build calc graph │   │
│                                          │  • Execute nodes    │   │
│                                          │  • Store results    │   │
│                                          └─────────────────────┘   │
│                                                    │               │
│                                                    ▼               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    CALCULATION GRAPH                         │   │
│  │                                                              │   │
│  │   ┌─────────┐    ┌──────────┐    ┌───────────┐    ┌──────┐  │   │
│  │   │ Input   │───>│ Lookup   │───>│ Calculate │───>│Output│  │   │
│  │   │ Nodes   │    │ Nodes    │    │ Nodes     │    │Nodes │  │   │
│  │   └─────────┘    └──────────┘    └───────────┘    └──────┘  │   │
│  │                                                              │   │
│  │   Inputs:        Lookups:        Calculations:    Outputs:  │   │
│  │   • Policy data  • Mortality     • Survival prob  • Reserve │   │
│  │   • Parameters   • Lapse         • Present value  • Cashflow│   │
│  │   • Assumptions  • Discount      • Net premium    • Summary │   │
│  │                  • Expense       • Reserves                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Model Definition

Models are defined as JSON configurations that describe the calculation graph:

```json
{
  "name": "Term Life Reserve - IFRS 17 BBA",
  "model_type": "reserving",
  "line_of_business": "term_life",
  "version": "1.0.0",
  "configuration": {
    "projection_months": 720,
    "time_step": "monthly",
    "nodes": [
      {
        "id": "policy_data",
        "type": "input",
        "source": "policy",
        "fields": ["issue_age", "sex", "smoker_status", "sum_assured", "premium", "term"]
      },
      {
        "id": "mortality_lookup",
        "type": "table_lookup",
        "table_type": "mortality",
        "inputs": ["issue_age", "sex", "smoker_status", "duration"],
        "output": "qx"
      },
      {
        "id": "lapse_lookup",
        "type": "table_lookup",
        "table_type": "lapse",
        "inputs": ["duration", "product_code"],
        "output": "lapse_rate"
      },
      {
        "id": "discount_lookup",
        "type": "table_lookup",
        "table_type": "discount_rate",
        "inputs": ["projection_month"],
        "output": "discount_rate"
      },
      {
        "id": "survival_probability",
        "type": "calculation",
        "formula": "(1 - qx) * (1 - lapse_rate)",
        "inputs": ["qx", "lapse_rate"],
        "output": "px"
      },
      {
        "id": "inforce",
        "type": "calculation",
        "formula": "cumulative_product(px)",
        "inputs": ["px"],
        "output": "inforce_count"
      },
      {
        "id": "claim_cashflow",
        "type": "calculation",
        "formula": "inforce_count * qx * sum_assured",
        "inputs": ["inforce_count", "qx", "sum_assured"],
        "output": "claims"
      },
      {
        "id": "premium_cashflow",
        "type": "calculation",
        "formula": "inforce_count * premium",
        "inputs": ["inforce_count", "premium"],
        "output": "premiums"
      },
      {
        "id": "net_cashflow",
        "type": "calculation",
        "formula": "premiums - claims - expenses",
        "inputs": ["premiums", "claims", "expenses"],
        "output": "net_cashflow"
      },
      {
        "id": "discount_factor",
        "type": "calculation",
        "formula": "cumulative_product(1 / (1 + discount_rate))",
        "inputs": ["discount_rate"],
        "output": "discount_factor"
      },
      {
        "id": "present_value",
        "type": "calculation",
        "formula": "net_cashflow * discount_factor",
        "inputs": ["net_cashflow", "discount_factor"],
        "output": "pv_cashflow"
      },
      {
        "id": "reserve",
        "type": "aggregation",
        "formula": "sum(pv_cashflow)",
        "inputs": ["pv_cashflow"],
        "output": "best_estimate_liability"
      }
    ],
    "outputs": [
      "best_estimate_liability",
      "monthly_cashflows",
      "inforce_projection"
    ]
  }
}
```

## Calculation Nodes

### Input Nodes

**PolicyDataNode**: Reads policy attributes
```python
class PolicyDataNode:
    def execute(self, policy, projection_month):
        return {
            'issue_age': policy.issue_age,
            'attained_age': policy.issue_age + projection_month // 12,
            'duration': projection_month,
            'sum_assured': policy.sum_assured,
            ...
        }
```

**ParameterNode**: Reads run parameters
```python
class ParameterNode:
    def execute(self, parameters):
        return {
            'valuation_date': parameters['valuation_date'],
            'reporting_basis': parameters['reporting_basis'],
            ...
        }
```

### Lookup Nodes

**MortalityLookupNode**: Looks up qx values
```python
class MortalityLookupNode:
    def execute(self, age, sex, smoker_status, duration, mortality_table):
        return mortality_table.get_qx(
            age=age,
            sex=sex,
            smoker_status=smoker_status,
            duration=duration
        )
```

**DiscountRateLookupNode**: Looks up discount rates
```python
class DiscountRateLookupNode:
    def execute(self, projection_month, discount_curve):
        return discount_curve.get_rate(term_months=projection_month)
```

### Calculation Nodes

**FormulaNode**: Evaluates mathematical formulas
```python
class FormulaNode:
    def execute(self, inputs, formula):
        # Safe evaluation using NumPy
        local_vars = {**inputs, 'np': numpy}
        return eval(formula, {"__builtins__": {}}, local_vars)
```

**CumulativeProductNode**: Calculates running products
```python
class CumulativeProductNode:
    def execute(self, values):
        return numpy.cumprod(values)
```

### Output Nodes

**ResultWriterNode**: Stores results to database
```python
class ResultWriterNode:
    def execute(self, policy_id, run_id, results):
        # Batch insert results
        for month, values in results.items():
            CalculationResult.create(
                calculation_run_id=run_id,
                policy_id=policy_id,
                projection_month=month,
                result_type='cashflow',
                values=values
            )
```

## Execution Flow

```python
class CalculationExecutor:
    def execute(self, run_id):
        # 1. Load run configuration
        run = CalculationRun.get(run_id)
        model = ModelDefinition.get(run.model_definition_id)
        assumptions = AssumptionSet.get(run.assumption_set_id)
        
        # 2. Build calculation graph
        graph = CalculationGraph(model.configuration)
        
        # 3. Load assumption tables
        tables = self.load_assumption_tables(assumptions)
        
        # 4. Get policies to process
        policies = Policy.filter(run.policy_filter)
        
        # 5. Process in batches
        batch_size = 1000
        for batch in chunked(policies, batch_size):
            results = self.process_batch(batch, graph, tables, run.parameters)
            self.save_results(run_id, results)
            self.update_progress(run_id, processed=len(batch))
        
        # 6. Generate summary
        summary = self.calculate_summary(run_id)
        run.result_summary = summary
        run.status = 'completed'
        run.save()
        
        # 7. Send notification
        self.notify_completion(run)

    def process_batch(self, policies, graph, tables, parameters):
        results = []
        for policy in policies:
            policy_result = graph.execute(
                policy=policy,
                tables=tables,
                parameters=parameters
            )
            results.append((policy.id, policy_result))
        return results
```

## Assumption Tables

### Mortality Table Structure

```python
class MortalityTable:
    def __init__(self, data):
        self.table_type = data['type']  # 'select_ultimate' or 'aggregate'
        self.select_period = data.get('select_period', 0)
        self.rates = self._build_lookup(data['rates'])
    
    def get_qx(self, age, sex, smoker_status, duration):
        if self.table_type == 'select_ultimate':
            if duration <= self.select_period:
                return self.rates[(age, sex, smoker_status, duration)]
            else:
                attained_age = age + duration
                return self.rates[(attained_age, sex, smoker_status, 'ultimate')]
        else:
            attained_age = age + duration
            return self.rates[(attained_age, sex, smoker_status)]
```

### Discount Curve

```python
class DiscountCurve:
    def __init__(self, data):
        self.rates = data['rates']  # [(term_months, rate), ...]
        self.interpolation = data.get('interpolation', 'linear')
    
    def get_rate(self, term_months):
        # Linear interpolation between given points
        return numpy.interp(
            term_months, 
            [r[0] for r in self.rates],
            [r[1] for r in self.rates]
        )
    
    def get_discount_factor(self, term_months):
        rate = self.get_rate(term_months)
        return 1 / (1 + rate) ** (term_months / 12)
```

## Regulatory Standards

### IFRS 17 Building Block Approach

```python
class IFRS17BBACalculator:
    def calculate(self, cashflows, discount_curve, risk_adjustment_method):
        # Best Estimate Liability
        bel = self.present_value(cashflows['net'], discount_curve)
        
        # Risk Adjustment
        ra = self.calculate_risk_adjustment(
            cashflows, 
            method=risk_adjustment_method
        )
        
        # Contractual Service Margin (at inception)
        csm = -1 * (bel + ra)  # CSM absorbs day-1 profit
        csm = max(csm, 0)  # CSM cannot be negative
        
        return {
            'best_estimate_liability': bel,
            'risk_adjustment': ra,
            'csm': csm,
            'liability_for_remaining_coverage': bel + ra + csm
        }
```

### Solvency II

```python
class SolvencyIICalculator:
    def calculate(self, cashflows, discount_curve):
        # Best Estimate
        be = self.present_value(cashflows['net'], discount_curve)
        
        # Risk Margin (Cost of Capital approach)
        rm = self.calculate_risk_margin(cashflows, coc_rate=0.06)
        
        # Technical Provisions
        tp = be + rm
        
        return {
            'best_estimate': be,
            'risk_margin': rm,
            'technical_provisions': tp
        }
```

## Performance Optimization

### Vectorization

All calculations use NumPy for vectorized operations:

```python
# Instead of:
for month in range(projection_months):
    pv[month] = cashflow[month] * discount_factor[month]

# Use:
pv = cashflows * discount_factors  # Single vectorized operation
```

### Batch Processing

- Policies processed in configurable batches (default 1000)
- Progress updates stored in Redis for real-time UI updates
- Checkpointing for failure recovery

### Parallel Execution

- Multiple Celery workers process batches concurrently
- Each worker handles complete policy calculations
- Results aggregated after all batches complete

## Error Handling

```python
class CalculationTask:
    @celery_app.task(bind=True, max_retries=3)
    def run_calculation(self, run_id):
        try:
            executor = CalculationExecutor()
            executor.execute(run_id)
        except RecoverableError as e:
            # Retry with exponential backoff
            self.retry(countdown=2 ** self.request.retries * 60)
        except Exception as e:
            # Mark run as failed
            run = CalculationRun.get(run_id)
            run.status = 'failed'
            run.error_message = str(e)
            run.save()
            raise
```
