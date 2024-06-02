import requests
from collections import defaultdict
import json
import time

# Define the search function with retry logic and exponential backoff
def search_crossref(keyword, start_year, end_year, retries=5, delay=1, email="alexander.luzhkov@gmail.com"):
    url = "https://api.crossref.org/works"
    headers = {
        'User-Agent': 'YourAppName/1.0 (mailto:{})'.format(email)
    }
    yearly_counts = defaultdict(int)
    
    for year in range(start_year, end_year + 1):
        params = {
            'query.bibliographic': keyword,
            'filter': f'from-pub-date:{year}-01-01,until-pub-date:{year}-12-31',
            'rows': 0
        }
        attempt = 0
        while attempt < retries:
            try:
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    data = response.json()
                    yearly_counts[year] = data['message']['total-results']
                    break
                else:
                    attempt += 1
                    wait_time = delay * (2 ** attempt)  # Exponential backoff with adjustable delay
                    print(f"Failed to retrieve data for {keyword} in {year}, attempt {attempt}/{retries}. Retrying in {wait_time} seconds.")
                    time.sleep(wait_time)
            except requests.exceptions.RequestException as e:
                attempt += 1
                wait_time = delay * (2 ** attempt)  # Exponential backoff with adjustable delay
                print(f"Exception occurred: {e}, attempt {attempt}/{retries}. Retrying in {wait_time} seconds.")
                time.sleep(wait_time)
    
    return yearly_counts

# Define the function to get counts for multiple keywords
def get_counts_for_keywords(keywords, start_year, end_year, delay=1, email="alexander.luzhkov@gmail.com"):
    results = defaultdict(lambda: defaultdict(int))
    for topic, topic_keywords in keywords.items():
        yearly_article_ids = defaultdict(set)
        for keyword in topic_keywords:
            print(f"Searching for keyword: {keyword}")
            yearly_counts = search_crossref(keyword, start_year, end_year, delay=delay, email=email)
            for year, count in yearly_counts.items():
                # Simulate unique article IDs by using counts, since we don't have actual IDs
                yearly_article_ids[year].update(range(count))
            print(f"Completed search for keyword: {keyword}")
        
        for year, article_ids in yearly_article_ids.items():
            results[topic][year] = len(article_ids)
    return results

# Define the keywords for each topic
keywords = {
    "Generative AI": [
        "Generative AI",
        "Generative Adversarial Networks",        
        "Image Synthesis"
    ],
    "Natural Language Processing (NLP)": [
        "Natural Language Processing",
        "Language Models",
        "Text Generation"        
    ],
    "Reinforcement Learning": [
        "Policy Gradient",
        "Q-Learning",
        "Reinforcement Learning"
    ],
    "Computer Vision": [
        "Object Detection",
        "Image Segmentation",
        "Visual Recognition"
    ],
    "AI Ethics and Explainability": [
        "Fairness in AI",
        "Algorithmic Bias",
        "Explainable AI (XAI)"
    ]
}

# Define the search period
start_year = 2012
end_year = 2023

# Get counts for the defined keywords with an adjustable delay between requests
results = get_counts_for_keywords(keywords, start_year, end_year, delay=1, email="alexander.luzhkov@gmail.com")

# Save the results to a JSON file
with open("ai_articles_counts.json", "w") as f:
    json.dump(results, f, indent=4)

# Display the results
for topic, yearly_counts in results.items():
    print(f"Topic: {topic}")
    for year, count in sorted(yearly_counts.items()):
        print(f"  Year: {year}, Number of articles: {count}")
