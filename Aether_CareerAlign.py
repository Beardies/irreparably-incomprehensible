@app.entrypoint
def invoke(payload, context):
    global current_session

    # --- 1. Validate memory ---
    if not MEMORY_ID:
        return {"error": "Memory not configured"}

    # --- 2. Resolve actor id ---
    actor_id = (
        getattr(context, "headers", {}).get(
            "X-Amzn-Bedrock-AgentCore-Runtime-Custom-Actor-Id", "user"
        )
        if hasattr(context, "headers")
        else "user"
    )

    # --- 3. Resolve session id (sandbox sometimes passes differently) ---
    session_id = getattr(context, "session_id", None) or payload.get("sessionId", "default")
    current_session = session_id

    # --- 4. Resolve user prompt (sandbox vs direct runtime) ---
    user_prompt = payload.get("prompt") or payload.get("inputText") or ""

    if not user_prompt:
        return {"error": "No prompt provided"}

    # --- 5. Configure memory ---
    memory_config = AgentCoreMemoryConfig(
        memory_id=MEMORY_ID,
        session_id=session_id,
        actor_id=actor_id,
        retrieval_config={
            f"/users/{actor_id}/facts": RetrievalConfig(top_k=3, relevance_score=0.5),
            f"/users/{actor_id}/preferences": RetrievalConfig(top_k=3, relevance_score=0.5),
        },
    )

    # --- 6. Build the agent ---
    agent = Agent(
        model=MODEL_ID,
        session_manager=AgentCoreMemorySessionManager(memory_config, REGION),
        system_prompt="You are Career Align, a kind, energetic, and insightful AI coordinator."
"Your purpose is to connect career goals with the right learning pathways by collaborating with other career search agents."
"You take the user’s stated career objectives and analyze job requirements across industries."
"You then compare these requirements with available coursework at the University of Texas at Dallas to identify the most " 
"relevant classes, certifications, or learning paths."
"You generate personalized course recommendations with clear explanations of how each course helps the user build the skills needed for their target roles."
"You always respond with enthusiasm, empathy, and precision—helping users align their academic choices with their long-term professional goals.",
        tools=[calculate],
    )

    # --- 7. Get response ---
    try:
        result = agent(user_prompt)
        text = result.message.get("content", [{}])[0].get("text", str(result))
        return {"response": text}
    except Exception as e:
        return {"error": str(e)}







# from gnews import GNews
# import pandas as pd
# import datetime

# # Initialize GNews
# google_news = GNews(language='en', country='US', max_results=100)

# start = datetime.date(2025, 8, 1)
# end = datetime.date(2025, 8,14)

# google_news.start_date = start
# google_news.end_date = end


# # Search for a topic
# results = google_news.get_news('(brand OR company) AND (activism OR controversial OR polemic OR dispute OR contentious OR scandalous OR censor OR conflict OR "love and hate" )')


# # Convert results to DataFrame
# df = pd.DataFrame(results)

# # Save to CSV
# df.to_csv("results/gnews_results_08_1.csv", index=False)

# print("News results saved to gnews_results_January.csv")    









# # to download all the article from news.csv 

# import csv
# from newspaper import Article
# import pandas as pd
# from pathlib import Path  
# from newspaper import Config
# import nltk
# import requests
# from selenium import webdriver

# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import random





# from bs4 import BeautifulSoup
# import re
# from urllib.parse import unquote
# #config will allow us to access the specified url for which we are #not authorized. Sometimes we may get 403 client error while parsing #the link to download the article.
# nltk.download('punkt_tab')
# nltk.download('punkt')

# def read_csv(file_path):

#     data = []
#     try:
#         with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 data.append(row)
#     except FileNotFoundError:
#         print(f"Error: The file {file_path} does not exist.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
    
#     return data

# def parse_article(index,news_link, news_date, news_media, html_source, path_name):
#     user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
#     config = Config()
#     config.browser_user_agent = user_agent
#     list=[]

#     article = Article(news_link, config=config)

#     # print("downloading article from:" + news_link)
#     dict={}
#     try:
#         article.download(input_html=html_source)
#         article.parse()
#         article.nlp()

#         news_title=article.title
#         news_summary = article.summary
#         news_article=article.text
#         # print(dict['Summary'])
#     except:
#         print("cannot download" + news_link)

#     dict['News_Index']=index
#     dict['Date']=news_date
#     dict['Media']=news_media
#     dict['Title']=news_title
#     dict['Link']=news_link
#     dict['Summary']=clean_data(str(news_summary))
    

#     list.append(dict)   

#     news_df=pd.DataFrame(list)
#     filepath = Path(path_name)  
#     filepath.parent.mkdir(parents=True, exist_ok=True)  
#     news_df.to_csv(filepath, mode='a', index=False, header=False)      

#     # Open a file in write mode ('w') and create it if it doesn't exist
#     article_filename = "results/dataset/" + str(index) + ".txt"
#     with open(article_filename, "w") as file:
#         file.write(clean_data(str(news_article)))


#     print("parse news succesfully")


# def clean_data(text):
#     text = text.lower()
#     # text = text.replace('-', ' ')
#     text = text.replace('\n', ' ')
#     text = text.replace('  ', ' ')
#     # text = text.replace('–', ' ')
#     # text = text.replace('—', ' ')
#     # text = text.replace('“', ' ')
#     # text = text.replace('”', ' ')
#     # text = text.replace('‘', ' ')
#     # text = text.replace(',', ' ')
#     # text = text.replace('\'', ' ')
#     # text = text.replace('\"', ' ')
#     return text

# def convert_links(df):
#     # for ind in df.index:
    
    
#     options = webdriver.FirefoxOptions()
#     options.add_argument('ignore-certificate-errors')
#     driver = webdriver.Firefox(options=options)
#     driver.get(df['link'][1])
#     print(driver.current_url)
#     # path_name = 'results/sex_robot_news_all.csv'
#     # filepath = Path(path_name)  
#     # filepath.parent.mkdir(parents=True, exist_ok=True)  
#     # df.to_csv(filepath) 

# def download_website(link):
#     html_result = ""


#     try:
#         # Go to the initial URL
#         driver.get(link)
        
#         pause = random.randint(5,7)
#         time.sleep(pause)  
        
#         # Get the current URL and page source after redirection
#         final_url = driver.current_url
#         page_source = driver.page_source
        
#         # print("Final URL:", link)
#         html_result = page_source
#     finally:
#         print('successfully downloaded')

    
#     return html_result

# if __name__ == "__main__":
#     # service = Service(executable_path='/Users/uraiwanjansong/Research/THESIS_brand_activism/.venv/bin/geckodriver')
#     # driver = webdriver.Firefox(service=service)
#     driver = webdriver.Chrome()

#     index = 342

#     month = "06"

#     # for month in range(1,9):
#     file_path = f'results/gnews_results_{month}.csv'  
#     csv_data = read_csv(file_path)
    
#     df_news = pd.DataFrame(csv_data)
#     # convert_links(df_news)

#     for ind in range(0,60):
#     # for ind in range(0,1):
#         print('year '+ month +' round: ', ind)
#         html_source = download_website(df_news['url'][ind])
#         # print(html_source)
#         parse_article( index,
#                     df_news['url'][ind], 
#                     df_news['published date'][ind], 
#                     df_news['publisher'][ind], 
#                     html_source, 
#                     'results/dataset/brand_activism_dataset.csv')
#         # break
#         index+=1
#     driver.quit()
        