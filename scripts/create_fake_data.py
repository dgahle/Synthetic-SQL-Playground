# Imports
from backend.faker_schema import FakerSchema
from json import load, loads
from pandas import concat, DataFrame, isna, read_csv, Series
from pathlib import Path

from backend.constants import CONFIG_PATH, data_type_mapping, DIR_PATH

# Variables
DEFAULT_DATA_TYPE: str = 'VARCHAR'
DEFAULT_NULLABLE: str = 'N'
DEFAULT_FAKER_KWARGS: str = "{}"


# Functions and classes
def clean_input(df: DataFrame) -> DataFrame:
    # 'Data Type',
    column: str = 'Data Type'
    nan_check: Series = df[column].isna()
    df[column][nan_check]: Series = DEFAULT_DATA_TYPE
    df[column] = df[column].apply(lambda x: x.upper())
    df[column] = df[column].apply(lambda x: x.split('(')[0])
    # 'Nullable',
    column: str = 'Nullable'
    nan_check: Series = df[column].isna()
    df[column][nan_check]: Series = DEFAULT_NULLABLE
    # 'Faker Type'
    column: str = 'Faker Type'
    nan_check: Series = df[column].isna()
    df[column][nan_check]: Series = df['Data Type'][nan_check].apply(
        lambda x: data_type_mapping[x]
    )
    # 'Faker kwargs'
    column: str = 'Faker kwargs'
    if column not in df.columns:
        df[column] = DEFAULT_FAKER_KWARGS
    nan_check: Series = df[column].isna()
    df[column][nan_check] = DEFAULT_FAKER_KWARGS

    return df


def get_fake_schema(CONFIG: dict) -> dict[str, str]:
    # Controls
    RAW_SCHEMA_PATH: Path = DIR_PATH / 'input' / CONFIG['input']
    NULL_NULLABLES: bool = CONFIG['null_nullables']
    # Load the raw schema
    df: DataFrame = read_csv(RAW_SCHEMA_PATH)
    # Clean input
    df = clean_input(df)
    df.to_csv(RAW_SCHEMA_PATH, index=False)
    # Null check
    nullable_key: str = 'Nullable'
    if NULL_NULLABLES and nullable_key in df:
        # Find where nullable
        df[nullable_key]: Series = df[nullable_key] == 'Y'
        # Define faker types to null
        df['Faker Type'][df['Nullable'].isin([True])] = 'pyobject'

    # Build faker-schema dict
    faker_schema: list[tuple] = []
    for _, row in df.iterrows():
        kwargs = loads(row['Faker kwargs'])
        faker_schema.append(
            (row['Source Fields'], (row['Faker Type'], kwargs))
        )
    # Convert to dict
    faker_schema: dict[str, str] = dict(faker_schema)

    return faker_schema


def create_fake_data(config_path: Path = CONFIG_PATH) -> None:
    # Config
    with open(config_path, 'r') as f:
        CONFIG: dict[str] = load(f)
    DATA_OUTPUT_PATH: Path = DIR_PATH / 'output' / CONFIG['output']
    NUMBER_OF_ROWS: int = CONFIG['number_of_rows']
    # Get faker-schema schema
    schema: dict[str, str] = get_fake_schema(CONFIG)
    # Produce fake data
    faker: FakerSchema = FakerSchema()
    data: list[dict] = faker.generate_fake(schema, iterations=NUMBER_OF_ROWS)
    # Build output DataFrame/CSV
    _data: dict
    frames: list[DataFrame] = []
    for _data in data:
        # Format to data
        _df: DataFrame = DataFrame(
            [list(_data.values())],
            columns=list(_data.keys())
        )
        # Cache
        frames.append(_df)
    # Concat Frames
    df: DataFrame = concat(frames)
    del data, frames
    # Format output
    df.reset_index(drop=True, inplace=True)
    # Save
    df.to_csv(DATA_OUTPUT_PATH, index=False)


def main() -> None:
    create_fake_data()
    pass


if __name__ == "__main__":
    main()
