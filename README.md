
Copy code
# AI Tools Dataset Development and Analysis Project

## Overview
This project aims to create a robust dataset concerning various AI tools, with an emphasis on meticulous data collection, cleansing, and storage, culminating in insightful analysis. The dataset focuses on capturing the nuances of AI tools through various attributes gathered from multiple sources.

## Project Structure

📁 code
📁 data
📁 processed_data # Cleaned and preprocessed data ready for analysis
📁 raw_data # Original datasets from primary sources
📁 datacleaning
📘 explaining_data_cleaning.ipynb # Guide on the data cleaning process
📁 datascraping
📄 categories.py # Script to scrape categories of AI tools
📄 links_ph.py # Script to scrape links from Product Hunt
📄 rescape_blocked.py # Script to rescrape blocked resources
📄 reviews_scraper_ph.py # Script to scrape reviews from Product Hunt
📄 toolinfoscraper_ta.py # Script to scrape product page data from There's an AI for that
📄 toolscraper_ta.py # Script to scrape homepage tool info from There's an AI for that
📁 db
📄 config.py # Configuration settings for the project
📄 creating_database.py # Script for initializing the database
📄 importing_data.py # Script to import data into the database
📁 local_llm
📄 .env # Environment variables for local settings
📄 ollama_classifier.py # Python script for the Ollama classifier
📄 ollama_product_description.py # Python script for generating product descriptions
📁 nlp
📘 nlp.ipynb # Notebook for NLP operations
📘 testing_nlp.ipynb # Notebook for testing NLP models
📁 topic_modelling
📘 lda.ipynb # Notebook for LDA topic modelling
📘 analysis.ipynb # Notebook for conducting data analysis
📄 main.py # Main script for running various data operation tasks

## Installation and Configuration

Before diving into the project, ensure you have Python 3.x installed along with Jupyter Notebooks. This project relies on libraries like pandas, numpy, matplotlib, seaborn, scikit-learn, and others that are essential for data science tasks.

To install these libraries, run:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn spacy

python -m spacy download en_core_web_sm

Make sure to set up the .env file with necessary environment variables and update the config.py with the appropriate settings for database connections and other configurations.

Data Scraping
To gather the most recent data, navigate to the datascraping/ directory and execute the scraping scripts:


python datascraping/links_ph.py
# ...
Data Cleaning
The datacleaning/ directory contains notebooks that detail the cleaning process. Execute these notebooks to clean and preprocess your data.

Data Analysis and Topic Modelling
For data analysis and topic modelling, utilize the notebooks within the topic_modelling/ directory:

lda.ipynb: For Latent Dirichlet Allocation topic modelling.
analysis.ipynb: For comprehensive data analysis.

Database Management
Run db/creating_database.py to initialize your database structure. After cleaning your data, use db/importing_data.py to import it into your database.

Local Large Language Models (LLM)
Scripts such as ollama_classifier.py and ollama_product_description.py within the local_llm/ directory are used for classification and generating product descriptions.

Natural Language Processing (NLP)
The nlp/ directory contains notebooks for building and testing NLP models. They are essential for analyzing text data and extracting insights.

Contributions
We welcome contributions to enhance the project's capabilities. Please adhere to the established coding standards, commit guidelines, and follow the pull request process detailed in the contributing section.

Contact
For queries or further assistance, feel free to reach out at [insert your email here].

![Alt text](../processflow.png)