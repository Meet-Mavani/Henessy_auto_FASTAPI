## session class use to add data in table
from Database.schema.starting_schema import user_car_trade,poa_blueprint,title
from sqlalchemy.orm import Session
from Database.schema.connect import engine
from Database.schema.main1 import session
import json
def store_data_in_DB(data,tablename):
    print("in the database")
    if tablename == 'poa_blueprint':
        poa=poa_blueprint(
            buyer_name=data["buyer_name"],
            buyer_signature=data["buyer_signature"],
            seller_name=data["seller_name"],
            seller_signature=data["seller_signature"]
        )
        session.add(poa)
        session.commit()
    
    
    elif tablename =="user_car_trade":
        user_trade=user_car_trade(
            buyer_name=data["buyer_name"],
            buyer_signature=data["buyer_signature"],
            seller_name=data["seller_name"],
            seller_signature=data["seller_signature"],
            stk=data["stk"],
            vnumber=data["Vin"]
        )
        session.add(user_trade)
        session.commit()
    
    elif tablename == "title" :
        title1=title(
            buyer_name=data["buyer_name "],
            seller_name=data["seller_name"]
        )
        session.add(title1)
        session.commit()
    
    
    
    
    
    # transaction = json.dumps(data.get("transaction_details", []))
    # account = json.dumps(data.get("account_summary", []))
    # user=bank_statement(
    #     transaction_details=transaction,
    #     statement_start_date=data["statement_start_date"],
    #     statement_end_date=data["statement_end_date"],
    #     branch_transit_number=data["branch_transit_number"],
    #     bank_name=data["bank_name"],
    #     account_type=data["account_type"],
    #     account_summary=account,
    #     account_number=data["account_number"],
    #     account_holder_name=data["account_holder_name"],
    #     account_holder_address=data["account_holder_address"]
    # )


    # session.add(user)
    # session.commit()    