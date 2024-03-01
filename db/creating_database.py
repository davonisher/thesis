import psycopg2
from config import config

#creating tables

create_tool_info = '''
CREATE TABLE tool_info (
    tool_id INTEGER PRIMARY KEY,
    saves NUMERIC,
    likes NUMERIC,
    stars NUMERIC,
    name_format VARCHAR(255),
    url_format VARCHAR(255),
    url_or VARCHAR(255)  -- Controleer of de naamgeving correct is
);
'''

create_tool_category = '''
CREATE TABLE tool_category (
    categories_id SERIAL PRIMARY KEY,
    tool_id INTEGER,
    task VARCHAR(255),
    task_id INTEGER,
    category_id INTEGER,
    category_name VARCHAR(255),
    description VARCHAR(1000),
    FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE
);
'''



create_financial_info = '''
CREATE TABLE financial_info (
    financial_id SERIAL PRIMARY KEY,
    tool_id INTEGER,
    price TEXT,
    freemium VARCHAR(50),
    last_funding_date DATE,
    last_funding_amount NUMERIC(15, 2),
    last_funding_amount_usd NUMERIC(15, 2),
    total_funding_amount NUMERIC(15, 2),
    total_funding_amount_currency VARCHAR(50),
    total_funding_amount_currency_usd NUMERIC(15, 2),
    number_of_investors INTEGER,
    number_of_acquisitions INTEGER,
    ipo_status VARCHAR(50),
    stock_exchange VARCHAR(50),
    FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE
);
'''


create_tool_descriptions = '''
CREATE TABLE tool_descriptions (
    description_id SERIAL PRIMARY KEY,
    tool_id INTEGER,
    description_text TEXT,
    description_old TEXT,
    FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE
);
'''

create_datetimes = '''
CREATE TABLE datetimes (
    date_id SERIAL PRIMARY KEY,
    tool_id INTEGER,
    founded_date TIMESTAMP,
    founded_date_precision VARCHAR(50),
    period VARCHAR(255),
    FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE
);
'''




create_company_info = '''
CREATE TABLE company_info (
  company_id SERIAL PRIMARY KEY,
  tool_id INTEGER,
  linkedin VARCHAR(255),
  number_of_employees VARCHAR(255),
  number_of_founders INTEGER,
  cb_rank_company VARCHAR(255),
  headquarters_regions VARCHAR(755),
  operating_status VARCHAR(255),
  company_type VARCHAR(255),
  FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE
);
'''


create_traffic_data = '''
CREATE TABLE traffic_data (
  traffic_id SERIAL PRIMARY KEY,
  tool_id INTEGER,
  average_visits NUMERIC,
  FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE
);
'''



create_topics = '''
CREATE TABLE topics (
  topic_id SERIAL PRIMARY KEY,
  tool_id INTEGER,
  topic_name VARCHAR(255),
  topic_description TEXT,
  topic_value NUMERIC,
  FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE
);
'''

create_sentiments = ''' 
CREATE TABLE sentiments (
  sentiment_id SERIAL PRIMARY KEY,
  tool_id INTEGER,
  topic_id INTEGER,
  sentiment_value NUMERIC,  
  FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE,
  FOREIGN KEY (topic_id) REFERENCES topics (topic_id) ON DELETE CASCADE
);
'''

create_reviews = '''
CREATE TABLE user_reviews (
  review_id SERIAL PRIMARY KEY,
  tool_id INTEGER,
  review_text TEXT,
  review_date DATE,
  helpful_count NUMERIC,
  FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE
);
'''

create_review_info = '''
CREATE TABLE review_info (
  review_info_id SERIAL PRIMARY KEY,
  tool_id INTEGER,
  helpful_count INTEGER,
  all_time_score NUMERIC,
  amount_of_reviews NUMERIC,
  recent_review_score NUMERIC,
  recent_reviews_amount NUMERIC,
  FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE
);
'''

create_user_ranking = '''
CREATE TABLE user_rankings (
  user_ranking_id SERIAL PRIMARY KEY,
  tool_id INTEGER,
  value NUMERIC,
  FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE
);
'''

create_financial_ranking = '''
CREATE TABLE financial_ranking (
  financial_ranking_id SERIAL PRIMARY KEY,
  tool_id INTEGER,
  value NUMERIC,
  FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE
);
'''

create_traffic_ranking = '''
CREATE TABLE traffic_ranking (
  traffic_ranking_id SERIAL PRIMARY KEY,
  tool_id INTEGER,
  value NUMERIC,
  FOREIGN KEY (tool_id) REFERENCES tool_info (tool_id) ON DELETE CASCADE
);
'''

# 
def main():
    try:        
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # run every sql command
        cur.execute(create_tool_info)
        cur.execute(create_topics)

        conn.commit()  # commit the changes
        
        # run other sql commands
        cur.execute(create_tool_category)
        cur.execute(create_financial_info)
        cur.execute(create_tool_descriptions)
        cur.execute(create_datetimes)
        cur.execute(create_company_info)
        cur.execute(create_traffic_data)
        cur.execute(create_sentiments)
        cur.execute(create_reviews)
        cur.execute(create_review_info)
        cur.execute(create_user_ranking)
        cur.execute(create_financial_ranking)
        cur.execute(create_traffic_ranking)

        conn.commit()
        print("Tabels succesfully made")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error making tables:", error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()

if __name__ == '__main__':
    # Voer het script uit
    main()
    