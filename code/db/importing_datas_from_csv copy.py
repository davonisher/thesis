
import psycopg2
import pandas as pd
from config import config

def importing_datas_from_csv():
    conn=None
    cur=None
    

    try:
        # Connecting Database
        params = config()
        conn = psycopg2.connect(**params)

        #Creating Cursor
        cur=conn.cursor()

    # IMPORTING DATA IN CSV FILE TO THE TABLE 
        #Reading csv files
        
        category_data = pd.read_csv ("/Users/macbook/thesis/new/code/data/processed_data/category_db.csv",sep=",")
        final_data = pd.read_csv ("/Users/macbook/thesis/new/code/data/processed_data/op.csv",sep=",")
        topic_data = pd.read_csv ("/Users/macbook/thesis/new/code/data/processed_data/topics_sentiment.csv",sep=",")   

        # Defining DataFrames 
        ratingdf= pd.DataFrame(category_data)
        finaldf= pd.DataFrame(final_data)
        topicdf = pd.DataFrame(topic_data)
      
        #Inserting data to the rating table
        for row in finaldf.itertuples():
            cur.execute('''
                INSERT INTO tool_info(tool_id, saves, likes, stars, name_format, url_format, url_or)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''',
        (row.tool_id,
            row.saves,
         row.likes,
         row.stars,
         row.name_format,  # Verondersteld dat 'name' overeenkomt met 'name_format'
         row.url_format,
         row.url)  # Verondersteld dat 'url_or' overeenkomt met 'url'
                )
        print("tool info Data is successfully imported")

        #Inserting data to the rating table
        for row in ratingdf.itertuples():
            cur.execute('''
                INSERT INTO tool_category(tool_id,category_id,category_name,description)
                VALUES (%s,%s, %s,%s)
                ''',
                (row.tool_id,
                row.category_id,
                row.category_name,
                row.description,)
                
                )
        print("Rating Data is successfully imported")
        for row in finaldf.itertuples(index=False):
            # Controleer of tool_id bestaat in tool_info
            cur.execute('SELECT EXISTS(SELECT 1 FROM tool_info WHERE tool_id = %s)', (row.tool_id,))
            exists = cur.fetchone()[0]

            if exists:
                try:
                    cur.execute('''
                        INSERT INTO tool_descriptions(tool_id, description_text)
                        VALUES (%s, %s)
                        ''', (row.tool_id, row.full_description)
                    )
                    print(f"Beschrijving toegevoegd voor tool_id {row.tool_id} in tool_descriptions.")
                except Exception as e:
                    print(f"Fout bij invoegen in tool_descriptions voor tool_id {row.tool_id}: {e}")
            else:
                print(f"tool_id {row.tool_id} bestaat niet in tool_info, rij wordt overgeslagen.")


        for row in finaldf.itertuples(index=False):
            # Controleer of tool_id bestaat in tool_info
            cur.execute('SELECT EXISTS(SELECT 1 FROM tool_info WHERE tool_id = %s)', (row.tool_id,))
            exists = cur.fetchone()[0]

            if exists:
                try:
                    cur.execute('''
                        INSERT INTO tool_descriptions(tool_id, description_text)
                        VALUES (%s, %s)
                        ON CONFLICT (tool_id) DO NOTHING
                        ''',
                        (row.tool_id, row.full_description)
                    )
                    print(f"Beschrijving toegevoegd of bestond al voor tool_id {row.tool_id} in tool_descriptions.")
                except Exception as e:
                    print(f"Fout bij invoegen in tool_descriptions voor tool_id {row.tool_id}: {e}")
            else:
                print(f"tool_id {row.tool_id} bestaat niet in tool_info, rij wordt overgeslagen.")












        #Saving the Tables
        conn.commit()
        print("Description Data is successfully imported")


    except Exception as error:
        print(error)

    # Closing connection and cursor    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
if __name__ == "__main__":
    importing_datas_from_csv()           









