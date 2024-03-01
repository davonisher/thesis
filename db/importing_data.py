import pandas as pd
import psycopg2
from config import config

# all code is obtained from the course Database Management Systems

# connect to the PostgreSQL database
params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

# Load dataframe from csv
finaldf = pd.read_csv("/Users/macbook/thesis/new/code/data/processed_data/op.csv", sep=",")
category_df = pd.read_csv("/Users/macbook/thesis/new/code/data/processed_data/category_db.csv", sep=",")
reviews_df = pd.read_csv("/Users/macbook/thesis/new/code/data/processed_data/reviews_data.csv", sep=",")
topics_sentiment = pd.read_csv('/Users/macbook/thesis/new/code/data/processed_data/topics_sentiment.csv')

# Unpivot the topics and sentiments
topics_df = topics_sentiment.melt(id_vars='tool_id', var_name='topic_name', value_name='topic_value')
sentiments_df = topics_sentiment.melt(id_vars='tool_id', var_name='sentiment_name', value_name='sentiment_value')

# function to insert data into the table
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


# function to insert data into the table
def insert_into_financial_info(row):

    try:
        cur.execute('''
            INSERT INTO financial_info (tool_id, price, freemium, last_funding_amount,
            last_funding_amount_usd, total_funding_amount, total_funding_amount_currency,
             number_of_investors, number_of_acquisitions, ipo_status, stock_exchange)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', 
            (row['tool_id'], row['price'], row['freemium'],
             row['last_funding_amount'], row['last_funding_amount_currency_in_usd'], row['total_funding_amount'], 
             row['total_funding_amount_currency'],  row['number_of_investors'],
             row['number_of_acquisitions'], row['ipo_status'], row['stock_exchange'])
        )
    except Exception as e:
        print(f"error adding  tool_id {row['tool_id']} in financial_info: {e}")
        conn.rollback()  # Rollback bij fout
    else:
        conn.commit()  # Commit als het succesvol is





# function to insert data into the table tool_category
def insert_into_tool_category(tool_id, category_id, category_name, description):
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


# function to insert data into the table user_reviews

def insert_into_user_reviews(row):

    try:
        cur.execute('''
            INSERT INTO user_reviews (tool_id, review_text, helpful_count)
            VALUES (%s, %s, %s)
            ''',
            (row['tool_id'], row['review_text'], row['helpful_count'])
        )

    except Exception as e:
        #print(f"Error adding review for tool_id {row['tool_id']}: {e}")
        conn.rollback()  # Rollback bij fout
    else:
        conn.commit()  # Commit als het succesvol is

# function to insert data into the table review_info
def insert_into_review_info(row):
    try:
        cur.execute('''
            INSERT INTO review_info (tool_id, all_time_score, amount_of_reviews, recent_review_score, recent_reviews_amount)
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (row['tool_id'], row['all_time_score'], row['amount_of_reviews'], row['recent_review_score'], row['recent_reviews_amount'])
)

    except Exception as e:
        #print(f"Error review_info voor tool_id {row['tool_id']}: {e}")
        conn.rollback()  # Rollback when error
    else:
        conn.commit()  # Commit if sucesssfull

# function to insert data into the table topics 
def topics_sentiments(row):
    try:
        cur.execute('''
            INSERT INTO topics (tool_id, topic_name, topic_value)
            VALUES (%s, %s, %s)
            RETURNING topic_id;
        ''', (row['tool_id'], row['topic_name'], row['topic_value']))
        topic_id = cur.fetchone()[0]
        conn.commit()

        # add the sentiment values
        sentiment_value = sentiments_df.loc[(sentiments_df['tool_id'] == row['tool_id']) & (sentiments_df['sentiment_name'] == row['topic_name']), 'sentiment_value'].values[0]
        if pd.notnull(sentiment_value):
            cur.execute('''
                INSERT INTO sentiments (tool_id, topic_id, sentiment_value)
                VALUES (%s, %s, %s);
            ''', (row['tool_id'], topic_id, sentiment_value))
            conn.commit()
    except Exception as e:
        print(f"error adding  topic voor tool_id {row['tool_id']}: {e}")
        conn.rollback()  # Rollback bij fout
    else:
        conn.commit()  # Commit als het succesvol is

# function to insert data into the table tool_descriptions
def insert_into_tool_descriptions(tool_id, description_old):
    tool_id = tool_id if pd.notnull(tool_id) else None
    description_old = description_old if pd.notnull(description_old) else None

    try:
        cur.execute('''
            INSERT INTO tool_descriptions (tool_id, description_old)
            VALUES (%s, %s)
            ''', (tool_id, description_old)
        )
    except Exception as e:
        print(f"erro adding description voor tool_id {tool_id}: {e}")
        conn.rollback()  # Rollback when error
    else:
        conn.commit()  # Commit 
        print(f"Description added for tool_id {tool_id}.")



def insert_into_company_info(tool_id, linkedin, number_of_employees, number_of_founders, cb_rank_company, headquarters_regions):
    tool_id = tool_id if pd.notnull(tool_id) else None
    linkedin = linkedin if pd.notnull(linkedin) else None
    number_of_employees = number_of_employees if pd.notnull(number_of_employees) else None
    number_of_founders = number_of_founders if pd.notnull(number_of_founders) else None
    cb_rank_company = cb_rank_company if pd.notnull(cb_rank_company) else None
    headquarters_regions = headquarters_regions if pd.notnull(headquarters_regions) else None

    try:
        cur.execute('''
            INSERT INTO company_info (tool_id, linkedin, number_of_employees, number_of_founders, cb_rank_company, headquarters_regions)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (tool_id, linkedin, number_of_employees, number_of_founders, cb_rank_company, headquarters_regions)
        )
    except Exception as e:
        print(f"Fout bij invoegen in company_info voor tool_id {tool_id}: {e}")
        conn.rollback()  # Rollback bij fout
    else:
        conn.commit()  # Commit als het succesvol is
        print(f"Rij toegevoegd in company_info voor tool_id {tool_id}.")


def insert_into_traffic_data(tool_id, average_visits):
    # Controleer of de waarden geldig zijn
    tool_id = tool_id if pd.notnull(tool_id) else None
    average_visits = average_visits if pd.notnull(average_visits) else None

    try:
        # Voer de invoeroperatie uit
        cur.execute('''
            INSERT INTO traffic_data (tool_id, average_visits)
            VALUES (%s, %s)
        ''', (tool_id, average_visits))
    except Exception as e:
        print(f"error adding {tool_id}: {e}")
        conn.rollback()  # Rollback bij fout
    else:
        conn.commit()  # Commit als het succesvol is
        print(f"row added for tool_id {tool_id}.")


def insert_into_datetimes(tool_id, founded_date, founded_date_precision, period):
    # Validate the values
    tool_id = tool_id if pd.notnull(tool_id) else None
    founded_date = pd.to_datetime(founded_date, errors='coerce') if pd.notnull(founded_date) else None
    founded_date_precision = founded_date_precision if pd.notnull(founded_date_precision) else None
    period = period if pd.notnull(period) else None

    try:
        # Perform the insert operation
        cur.execute('''
            INSERT INTO datetimes (tool_id, founded_date_precision, period)
            VALUES (%s, %s, %s, %s)
        ''', (tool_id, founded_date, founded_date_precision, period))
    except Exception as e:
        print(f"Error inserting into datetimes for tool_id {tool_id}: {e}")
        conn.rollback()  # Rollback in case of error
    else:
        conn.commit()  # Commit if successful
        print(f"Row added in datetimes for tool_id {tool_id}.")


# loop through each row in the finaldf and execute the insert function
for index, row in finaldf.iterrows():
    insert_into_tool_info(row)
    insert_into_financial_info(row)
print("Data is successfully imported")
# loop through each row in finaldf  and execute the insert function
for index, row in finaldf.iterrows():
    insert_into_tool_descriptions(row['tool_id'], row['full_description'])
    insert_into_company_info(row['tool_id'], row['linkedin'], row['number_of_employees'], row['number_of_founders'], row['cb_rank_(company)'], row['headquarters_regions'])
    insert_into_traffic_data(row['tool_id'], row['average_visits'])
    insert_into_datetimes(row['tool_id'], row['founded_date'], row['founded_date_precision'], row['period'])
print("Data is successfully imported")


# loop through each row in the category_df and execute the insert function
for index, row in category_df.iterrows():
    insert_into_tool_category(row['tool_id'], row['category_id'], row['category_name'], row['description'])
print("Rating Data is successfully imported")


# loop through each row in the reviews_df and execute the insert function
for index, row in reviews_df.iterrows():
    insert_into_user_reviews(row)
    insert_into_review_info(row)
print("Data is successfully imported")

# loop through each row in the topics_df and execute the insert function
for index, row in topics_df.iterrows():
    topics_sentiments(row)

# close the connection and cursor
cur.close()
conn.close()
