from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    item = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)

# If you want to create the SQLite database here as well, you can include this:
# (though typically you'd let your main app do this)
if __name__ == "__main__":
    engine = create_engine('sqlite:///expensestrack.db')
    Base.metadata.create_all(engine)
