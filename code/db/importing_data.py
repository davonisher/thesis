
import psycopg2
import pandas as pd
from config import config


import psycopg2
import pandas as pd
from psycopg2.extras import execute_values
from config import config

def read_data(file_path):
    """
    Reads CSV data from the given file path.
    """
    return pd.read_csv(file_path, thousands=',' , low_memory=False)

def process_dataframe(df, column_mapping):
    """
    Process DataFrame to conform to the database schema.
    """
    for column, dtype in column_mapping.items():
        if dtype == 'timestamp':
            df[column] = pd.to_datetime(df[column], errors='coerce')
        elif dtype == 'bool':
            df[column] = df[column].astype(bool)
        elif dtype == 'int':
            df[column] = df[column].fillna(0).astype('int64')
        elif dtype == 'float':
            df[column] = df[column].astype('float64')
        else:  # Default to string
            df[column] = df[column].astype(str)
    return df

def bulk_insert(cur, table_name, df):
    """
    Perform a bulk insert using the execute_values function.
    """
    columns = list(df.columns)
    values = df.values.tolist()
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s ON CONFLICT DO NOTHING;"
    execute_values(cur, query, values)

def importing_data():
    try:
        # Connect to the database
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Read and process CSV files
        final_data = read_data('/Users/macbook/thesis/new/code/data/processed_data/final.csv')
        review_data = read_data('/Users/macbook/thesis/new/code/data/processed_data/reviews_data.csv')
        category_data = read_data('/Users/macbook/thesis/new/code/data/processed_data/category_db.csv')
        feature_data = read_data('/Users/macbook/thesis/new/code/data/processed_data/feature_data.csv')

        # Column mappings
        final_data_column_mapping = {
            # mappings as per final_data CSV structure
        'tool_id': 'float', 'url_format': 'string', 
            'average visits': 'float', 
                     'task': 'string', 'url': 'string', 'price': 'string', 'saves': 'float', 'likes': 'float',
                        'stars': 'float', 'period': 'string', 'url_content': 'string', 'name_format': 'string', 'organization_name': 'string', 'organization_name_url': 'string', 
                            'industries': 'string', 'headquarters_location': 'string', 'description': 'string', 'cb_rank_(company)': 'string', 'headquarters_regions': 'string',
                                'founded_date': 'string', 'founded_date_precision': 'string', 'operating_status': 'string', 'company_type': 'string', 'website': 'string', 
                                    'linkedin': 'string', 'full_description': 'string', 'industry_groups': 'string', 'number_of_employees': 'string', 'number_of_founders': 'float',
                                        'number_of_funding_rounds': 'float', 'last_funding_date': 'string', 'last_funding_amount': 'float', 'last_funding_amount_currency': 'float', 
                                            'last_funding_amount_currency_(in_usd)': 'float', 'total_funding_amount': 'float', 'total_funding_amount_currency': 'string', 
                                                'total_funding_amount_currency_(in_usd)': 'float', 'number_of_investors': 'float', 'number_of_acquisitions': 'float', 'ipo_status': 'string', 'ipo_date': 'float', 
                                                    'stock_exchange': 'float', 'tool_name': 'string', 's.n.': 'float', 'tool name': 'float', 'location': 'float', 'year founded': 'float', 'website link': 'float', 
                                                        'product description': 'float', 'business unit': 'float', 'vertical': 'float', 'application type': 'float', 'use case': 'float', 'type of output modality': 'float',
                                                            'type of data origin': 'float', 'freemium': 'float'
            }

        review_data_column_mapping = {
           'tool_id': 'int', 'review_id': 'string', 'review_text': 'string', 'review_date': 'string',
             'user_info_name': 'string', 'user_info': 'string', 'helpful_count': 'int', 'all_time_score': 'float', 'amount_of_reviews': 'float', 'tool_link': 'string', 
             'recent_review_score': 'int', 'recent_reviews_amount': 'float', 'url_format': 'string'
             }

        

        # Process DataFrames
        final_data_processed = process_dataframe(final_data, final_data_column_mapping)
        review_data_processed = process_dataframe(review_data, review_data_column_mapping)

        # Bulk insert data into tables
        bulk_insert(cur, 'tool_info', final_data_processed)  # tool_info is the table name
        bulk_insert(cur, 'review_info', review_data_processed) # review_info is the table name

        # Commit changes and close connection
        conn.commit()
    except Exception as error:
        print("Error while importing data:", error)

    finally:
        if cur is not None:
            cur.close


if __name__ == "__main__":
    importing_data()