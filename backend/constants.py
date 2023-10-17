# Imports
from pathlib import Path
from sqlalchemy import BIGINT, CHAR, DATETIME, DECIMAL, NVARCHAR, TIME
from sqlalchemy import Date, Integer, Numeric, SmallInteger, String

# Paths
DIR_PATH: Path = Path(__file__).parent.parent
CONFIG_PATH: Path = DIR_PATH / 'config.json'
INPUT_PATH: Path = DIR_PATH / 'input'
OUTPUT_PATH: Path = DIR_PATH / 'output'

# Mapping
data_type_mapping: dict[str, str] = dict(
    CHAR='pystr',
    VARCHAR='pystr',
    SMALLINT='pyint',
    DATETIME='date_time',
    BIGINT='pyint',
    DECIMAL='pyfloat',
    INT='pyint',
    TINYINT='pyint',
    DATE='date',
    NVARCHAR='pystr',
    NUMERIC='pyint',
    SMALLDATETIME='date_time',
    UNIQUEIDENTIFIER='ean',
)

SQLTYPE_MAPPING: dict[str, object] = dict(
    BIGINT=BIGINT,
    BIT=Integer,
    CHAR=CHAR,
    DATE=Date,
    DATETIME=DATETIME,
    DATETIME2=DATETIME,
    DECIMAL=DECIMAL,
    INT=Integer,
    NUMERIC=Numeric,
    NVARCHAR=NVARCHAR,
    SMALLINT=SmallInteger,
    TIME=TIME,
    TINYINT=Integer,
    VARCHAR=String,
)
