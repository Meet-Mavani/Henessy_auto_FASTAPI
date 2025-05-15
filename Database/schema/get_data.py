from Database.schema.starting_schema import bank_statement
from Database.schema.main1 import session

def fetch_all_bank_statements():
    try:
        print("Fetching all bank statements...")
        results = session.query(bank_statement).all()
        return results

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
fetch_all_bank_statements()