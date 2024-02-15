import pandas as pd
import psycopg2
from config import config

# Verbind met de database
params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

# Laad je DataFrame
finaldf = pd.read_csv("/Users/macbook/thesis/new/code/data/processed_data/op.csv")
category_df = pd.read_csv("/Users/macbook/thesis/new/code/data/processed_data/category_db.csv", sep=",")

# Functie om data in te voeren in tool_info
def insert_into_tool_info(row):
    try:
        cur.execute('''
            INSERT INTO tool_info (tool_id, saves, likes, stars, name_format, url_format, url_or)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', 
            (row['tool_id'], row['saves'], row['likes'], row['stars'], 
             row['name_format'], row['url_format'], row['url'])
        )
    except Exception as e:
        print(f"Fout bij invoegen tool_id {row['tool_id']}: {e}")
        conn.rollback()
    else:
        conn.commit() 

# Functie om data in te voeren in financial_info
def insert_into_financial_info(row):
    last_funding_date = row['last_funding_date'] if not pd.isna(row['last_funding_date']) else None
    ipo_date = row['ipo_date'] if not pd.isna(row['ipo_date']) else None
    
    try:
        # Probeer de price te converteren naar een float, of gebruik None als het faalt
        price = float(row['price']) if pd.notnull(row['price']) else None
    except ValueError:
        print(f"Ongeldige prijs voor tool_id {row['tool_id']}: {row['price']}")
        price = None  # Of een standaardwaarde als dat passender is
    try:
        cur.execute('''
            INSERT INTO financial_info (tool_id, price, freemium, number_funding_rounds,
            last_funding_amount,  last_funding_amount_usd, total_funding_amount, total_funding_amount_currency,
            total_funding_amount_currency_usd, number_of_investors, number_of_acquisitions, ipo_status,
            ipo_date, stock_exchange)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', 
            (row['tool_id'], row['price'], row['freemium'], row['number_of_funding_rounds'],
             row['last_funding_amount'], row['last_funding_amount_currency_in_usd'], row['total_funding_amount'], 
             row['total_funding_amount_currency'], row['last_funding_amount_currency_in_usd'], row['number_of_investors'],
             row['number_of_acquisitions'], row['ipo_status'], row['ipo_date'], row['stock_exchange'])
        )
    except Exception as e:
        print(f"Error adding tool_id {row['tool_id']} in financial_info: {e}")
        conn.rollback()  # Rollback bij fout
    else:
        conn.commit()  # Commit als het succesvol is


# Loop door elke rij in de DataFrame en voer de invoerfunctie uit
for index, row in finaldf.iterrows():
    #insert_into_tool_info(row)
    insert_into_financial_info(row)
    #insert_into_tool_category(row)

# Functie om data in te voeren in tool_category
def insert_into_tool_category(tool_id, category_id, category_name, description):
    # Converteer alle NaN waarden naar None (wat SQL zal interpreteren als NULL)
    tool_id = tool_id if pd.notnull(tool_id) else None
    category_id = category_id if pd.notnull(category_id) else None
    category_name = category_name if pd.notnull(category_name) else None
    description = description if pd.notnull(description) else None

    try:
        cur.execute('''
            INSERT INTO tool_category (tool_id, category_id, category_name, description)
            VALUES (%s, %s, %s, %s)
            ''', (tool_id, category_id, category_name, description)
        )
    except Exception as e:
        print(f"Fout bij invoegen in tool_category voor tool_id {tool_id}: {e}")
        conn.rollback()  # Rollback bij fout
    else:
        conn.commit()  # Commit als het succesvol is
        print(f"Rij toegevoegd in tool_category voor tool_id {tool_id}.")

# Loop door elke rij in category_df en voer de invoerfunctie uit
#for index, row in category_df.iterrows():
#    insert_into_tool_category(row['tool_id'], row['category_id'], row['category_name'], row['description'])
#print("Rating Data is successfully imported")




# Sluit de cursor en verbinding
cur.close()
conn.close()
