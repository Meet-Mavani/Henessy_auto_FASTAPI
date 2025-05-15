from Database.schema.connect import engine
from sqlalchemy import inspect

inspector = inspect(engine)
print(inspector.get_table_names())  # Expected: ['title', 'poa_blueprint', 'user_car_trade']
