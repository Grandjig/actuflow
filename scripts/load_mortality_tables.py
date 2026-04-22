#!/usr/bin/env python
"""
Load standard mortality tables into ActuFlow.
Supports various table formats: SOA tables, CSV, custom JSON.
"""

import sys
import os
import json
import csv
from datetime import date
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.models import AssumptionSet, AssumptionTable, User
from app.models.base import get_db


# Standard mortality tables data (simplified versions)
STANDARD_TABLES = {
    "2017_CSO_Male_NS_ANB": {
        "name": "2017 CSO Male Non-Smoker ANB",
        "description": "2017 Commissioners Standard Ordinary Table - Male Non-Smoker Age Nearest Birthday",
        "type": "aggregate",
        "rates": {
            str(age): round(0.00038 + 0.00003 * (age - 20) + 0.00001 * ((age - 20) ** 1.5), 6)
            for age in range(20, 100)
        }
    },
    "2017_CSO_Male_SM_ANB": {
        "name": "2017 CSO Male Smoker ANB",
        "description": "2017 Commissioners Standard Ordinary Table - Male Smoker Age Nearest Birthday",
        "type": "aggregate",
        "rates": {
            str(age): round(0.00065 + 0.00005 * (age - 20) + 0.000015 * ((age - 20) ** 1.5), 6)
            for age in range(20, 100)
        }
    },
    "2017_CSO_Female_NS_ANB": {
        "name": "2017 CSO Female Non-Smoker ANB",
        "description": "2017 Commissioners Standard Ordinary Table - Female Non-Smoker Age Nearest Birthday",
        "type": "aggregate",
        "rates": {
            str(age): round(0.00025 + 0.00002 * (age - 20) + 0.000008 * ((age - 20) ** 1.5), 6)
            for age in range(20, 100)
        }
    },
    "2017_CSO_Female_SM_ANB": {
        "name": "2017 CSO Female Smoker ANB",
        "description": "2017 Commissioners Standard Ordinary Table - Female Smoker Age Nearest Birthday",
        "type": "aggregate",
        "rates": {
            str(age): round(0.00045 + 0.00004 * (age - 20) + 0.000012 * ((age - 20) ** 1.5), 6)
            for age in range(20, 100)
        }
    },
}


def create_standard_assumption_set(db: Session) -> AssumptionSet:
    """Create a standard mortality assumption set."""
    print("Creating standard mortality assumption set...")
    
    # Get system user or first admin
    admin = db.query(User).filter(User.is_superuser == True).first()
    
    assumption_set = AssumptionSet(
        id=str(uuid.uuid4()),
        name="Standard Mortality Tables 2017",
        version="1.0",
        description="2017 CSO Mortality Tables - Standard reference tables",
        status="approved",
        effective_date=date(2017, 1, 1),
        locked=True,
        approved_by_id=admin.id if admin else None,
        created_by_id=admin.id if admin else None,
    )
    
    db.add(assumption_set)
    db.flush()
    
    return assumption_set


def load_standard_tables(db: Session, assumption_set: AssumptionSet):
    """Load standard mortality tables."""
    print(f"Loading {len(STANDARD_TABLES)} standard mortality tables...")
    
    for table_code, table_data in STANDARD_TABLES.items():
        table = AssumptionTable(
            id=str(uuid.uuid4()),
            assumption_set_id=assumption_set.id,
            table_type="mortality",
            name=table_data["name"],
            description=table_data["description"],
            data={
                "type": table_data["type"],
                "code": table_code,
                "rates": table_data["rates"]
            },
            metadata={
                "source": "SOA",
                "effective_year": 2017,
                "age_basis": "ANB"
            }
        )
        db.add(table)
        print(f"  Added: {table_data['name']}")
    
    db.flush()


def load_from_csv(db: Session, assumption_set_id: str, csv_path: str, table_name: str):
    """Load mortality table from CSV file.
    
    Expected CSV format:
    age,male_ns,male_sm,female_ns,female_sm
    20,0.00038,0.00065,0.00025,0.00045
    ...
    """
    print(f"Loading mortality table from {csv_path}...")
    
    rates = {"male_ns": {}, "male_sm": {}, "female_ns": {}, "female_sm": {}}
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            age = row['age']
            rates['male_ns'][age] = float(row['male_ns'])
            rates['male_sm'][age] = float(row['male_sm'])
            rates['female_ns'][age] = float(row['female_ns'])
            rates['female_sm'][age] = float(row['female_sm'])
    
    table = AssumptionTable(
        id=str(uuid.uuid4()),
        assumption_set_id=assumption_set_id,
        table_type="mortality",
        name=table_name,
        description=f"Imported from {csv_path}",
        data={
            "type": "aggregate",
            "multi_decrement": True,
            "rates": rates
        }
    )
    
    db.add(table)
    db.flush()
    
    print(f"  Loaded {len(rates['male_ns'])} age rates")


def load_from_json(db: Session, assumption_set_id: str, json_path: str):
    """Load mortality table from JSON file."""
    print(f"Loading mortality table from {json_path}...")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    table = AssumptionTable(
        id=str(uuid.uuid4()),
        assumption_set_id=assumption_set_id,
        table_type="mortality",
        name=data.get('name', 'Imported Table'),
        description=data.get('description', f'Imported from {json_path}'),
        data=data.get('data', data),
        metadata=data.get('metadata', {})
    )
    
    db.add(table)
    db.flush()
    
    print(f"  Loaded: {table.name}")


def main():
    """Main function to load mortality tables."""
    print("\n" + "="*50)
    print("ActuFlow Mortality Table Loader")
    print("="*50 + "\n")
    
    db = next(get_db())
    
    try:
        # Check if standard tables already exist
        existing = db.query(AssumptionSet).filter(
            AssumptionSet.name == "Standard Mortality Tables 2017"
        ).first()
        
        if existing:
            print("Standard mortality tables already loaded.")
            print(f"  Assumption Set ID: {existing.id}")
            return
        
        # Create assumption set and load tables
        assumption_set = create_standard_assumption_set(db)
        load_standard_tables(db, assumption_set)
        
        db.commit()
        
        print("\n" + "="*50)
        print("✓ Mortality tables loaded successfully!")
        print(f"  Assumption Set ID: {assumption_set.id}")
        print("="*50 + "\n")
        
    except Exception as e:
        db.rollback()
        print(f"\nError loading mortality tables: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
