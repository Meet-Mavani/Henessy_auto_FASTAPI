from Database.schema.starting_schema import poa_blueprint, user_car_trade
from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session
from Database.schema.connect import engine

session = Session(bind=engine)

def validate_data():
    print("✅ Data validation has been started\n")

    # Buyer Name Check
    buyer_names_a = set(session.scalars(
        select(poa_blueprint.buyer_name).distinct()
    ).all())

    buyer_names_b = set(session.scalars(
        select(user_car_trade.buyer_name).distinct()
    ).all())

    if buyer_names_a == buyer_names_b:
        print("✅ Buyer name test passed.")
    else:
        print("❌ Buyer names don't match.")

    # Seller Name Check
    seller_names_a = set(session.scalars(
        select(poa_blueprint.seller_name).distinct()
    ).all())

    seller_names_b = set(session.scalars(
        select(user_car_trade.seller_name).distinct()
    ).all())

    if seller_names_a == seller_names_b:
        print("✅ Seller name test passed.")
    else:
        print("❌ Seller names don't match.")

    # Signature Check
    poa_sign_checker = session.execute(
        select(poa_blueprint).where(
            poa_blueprint.buyer_signature.is_(True),
            poa_blueprint.seller_signature.is_(True)
        )
    ).first()

    user_sign_checker = session.execute(
        select(user_car_trade).where(
            user_car_trade.buyer_signature.is_(True),
            user_car_trade.seller_signature.is_(True)
        )
    ).first()

    if poa_sign_checker and user_sign_checker:
        print("✅ Signature test passed.")
    else:
        print("❌ Signature test failed.")

    # VIN Number Check
    vin_number_checker = session.execute(
        select(user_car_trade).where(
            func.length(user_car_trade.vnumber) == 17
        )
    ).first()

    if vin_number_checker:
        print("✅ VIN number test passed.")
    else:
        print("❌ VIN number test failed.")

    # STK Number Check
    stk_number_checker = session.execute(
        select(user_car_trade).where(
            and_(
                user_car_trade.stk.like('STK%'),
                func.length(user_car_trade.stk) == 11
            )
        )
    ).first()

    if stk_number_checker:
        print("✅ STK number test passed.")
    else:
        print("❌ STK number test failed.")

# Call the function
validate_data()
