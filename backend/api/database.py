import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime as dt

# Define database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./doc_data.db"

# Create engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define Base
Base = declarative_base()

# Define Document model
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(DateTime, default=dt.utcnow)
    file_size = Column(BigInteger)

# Create tables
Base.metadata.create_all(bind=engine)

# Define get_db function
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import func

# Define a function to print the length of the documents table
def print_documents_table_length():
    # Open a new database session
    db = Session()

    try:
        # Execute a SELECT query to count the number of rows in the documents table
        query = db.query(func.count(Document.id))
        table_length = db.execute(query).scalar()

        # Print the length of the documents table
        print(f"Length of Documents Table: {table_length}")

    finally:
        # Close the database session
        db.close()

# Call the function to print the length of the documents table
print_documents_table_length()

# Define a function to print the column names of the documents table
def print_documents_table_columns():
    # Get the column names from the __table__ attribute of the Document class
    column_names = Document.__table__.columns.keys()

    # Print the column names
    print("Column Names of Documents Table:")
    for column_name in column_names:
        print(column_name)

# Call the function to print the column names of the documents table
print_documents_table_columns()

