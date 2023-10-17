# Imports
from json import load
from pandas import DataFrame, read_csv, Series
from sqlalchemy import create_engine, sql
from sqlalchemy import Column, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.constants import CONFIG_PATH, DIR_PATH, SQLTYPE_MAPPING

# Variables
# Config
with open(CONFIG_PATH, 'r') as f:
    CONFIG: dict[str] = load(f)
TABLE_NAME: str = CONFIG['table_name']
SQL_LITE_ENGINE_ADDRESS: str = f'sqlite:///data-store-15-9-23.db'


# Functions
def build_column(datatype: str, nullable: str, primary_key: bool = False, autoincrement: bool = False) -> Column:
    # Format inputs
    nullable: bool = True if nullable == 'Y' else False
    sqltype: object = SQLTYPE_MAPPING[datatype] 
    # Build columns
    column: Column = Column(
        sqltype,
        nullable=nullable,
        primary_key=primary_key,
        autoincrement=autoincrement
    )
    
    return column


def build_table_inputs() -> dict:
    class_inputs: dict
    # Load metadata
    df_schema: DataFrame = read_csv(DIR_PATH / 'input' / CONFIG['input'])
    # Construct table input
    index: int
    row: Series
    columns: list[tuple[str, Column]] = []
    for index, row in df_schema.iterrows():
        primary_key: bool = True if index == 0 else False
        col: Column = build_column(row['Data Type'], row['Nullable'], primary_key=primary_key)
        columns.append(
            (row['Source Fields'], col)
        )

    class_inputs: dict = dict(columns)

    return class_inputs


def create_sql_table() -> None:
    # Create a Session
    engine = create_engine(SQL_LITE_ENGINE_ADDRESS)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()

    # Create table
    class_inputs: dict = build_table_inputs()
    class_inputs['__tablename__'] = TABLE_NAME
    Test = type(TABLE_NAME, (Base,), class_inputs)
    # Create the table if it doesn't exist
    Base.metadata.create_all(engine)
    # # Template: empty the table
    # rows_to_delete = session.query(Test).all()
    # for row in rows_to_delete:
    #     session.delete(row)

    # Pass table object to sqlalchemy session
    session.query(Test).all()
    metadata = MetaData()  # bind=self.engine)
    metadata.reflect(bind=engine)

    # Set up SQL connection and print example queries
    connection = engine.connect()

    # Add data to table
    df_data: DataFrame = read_csv(DIR_PATH / 'output' / CONFIG['output'])
    df_data.to_sql(TABLE_NAME, con=connection, if_exists='replace')

    # Print queries
    columns: list[str] = [x.name for x in metadata.tables[TABLE_NAME].columns.values()]
    analytics = connection.execute(
        sql.text(
            f"SELECT * FROM {TABLE_NAME}"
        )
    ).fetchall()  # Returns a list of rows without columns names

    print(columns)
    print(analytics)

    # Commit the changes and close the session
    session.commit()
    session.close()

    pass


def main() -> None:
    create_sql_table()
    pass


if __name__ == "__main__":
    main()
