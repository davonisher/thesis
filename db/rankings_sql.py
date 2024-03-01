import pandas as pd
import psycopg2
from config import config

# all code obtained from ChatGPT (2024) and Copilot (2024)

def main():
    # connect to the PostgreSQL database
    params = config()
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()

    # Update tool_info with the correct values
    update_query = '''
    UPDATE tool_info 
    SET stars = COALESCE(NULLIF(stars, 'NaN'), 0),
        likes = COALESCE(NULLIF(likes, 'NaN'), 0),
        saves = COALESCE(NULLIF(saves, 'NaN'), 0);
    '''
    cur.execute(update_query)
    # Update review_info with the correct values
    update_query_fin = '''
    UPDATE financial_info 
    SET total_funding_amount = COALESCE(NULLIF(total_funding_amount, 'NaN'), 0);
    '''
    cur.execute(update_query_fin)

    # formula for user_ranking
    insert_user_rankings_query = '''
    INSERT INTO user_rankings (tool_id, value)
    SELECT tool_id, (likes + saves) AS value
    FROM tool_info
    ORDER BY value DESC;
    '''
    cur.execute(insert_user_rankings_query)

    # formula for traffic_ranking
    insert_traffic_ranking_query = '''
    INSERT INTO traffic_ranking (tool_id, value)
    SELECT tool_id, (average_visits) AS value
    FROM traffic_data
    ORDER BY value DESC;
    '''
    cur.execute(insert_traffic_ranking_query)


    # formula for financial_ranking
    update_financial_ranking_query = '''
    INSERT INTO financial_ranking (tool_id, value)
    SELECT tool_id,
        (LOG(total_funding_amount + 1) * 1.5) + (number_of_investors * 2) + (number_of_acquisitions * 3) AS value
    FROM financial_info
    ORDER BY value DESC;
    '''
    cur.execute(update_financial_ranking_query)

    # close the connection
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
