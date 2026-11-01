
import streamlit as st
import requests

import json
import os

st.set_page_config(
    page_title="News Aggregator",
    page_icon="📰"
)

# Permanent Bookmark Storage
SAVE_FILE = "saved_news.json"

def load_saved_news():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    return []

def save_saved_news(news):
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(news, file, ensure_ascii=False, indent=4)

st.title("📰 News Aggregator Platform")
st.write("Find the latest news")

API_KEY = st.secrets["NEWS_API_KEY"]

# Search
search = st.text_input(
    "🔍 Search News",
    placeholder="Enter topic like AI, Cricket, Technology"
)

# Category
categories = {
    "All": "",
    "Technology": "technology",
    "Sports": "sports",
    "Business": "business",
    "Entertainment": "entertainment",
    "Science": "science",
    "Health": "health"
}

category = st.selectbox(
    "🏷️ Select Category",
    list(categories.keys())
)
news_count = st.selectbox(
    "📰 Number of News Articles",
    [5, 10, 20]
)

# News API
url = "https://newsapi.org/v2/top-headlines"
params = {
    "country": "us",
    "apiKey": API_KEY,
    "pageSize": news_count
}

# Category apply
if categories[category]:
    params["category"] = categories[category]

# Search apply
if search:
    url = "https://newsapi.org/v2/everything"

    params = {
     "q": search,
     "language": "en",
     "sortBy": "publishedAt",
     "apiKey": API_KEY,
     "pageSize": news_count
}
 
# Refresh News Button
st.button("🔄 Refresh News")

# Bookmark Feature
if "saved_news" not in st.session_state:
    st.session_state.saved_news = load_saved_news()

# News API Response
response = requests.get(url, params=params)

if response.status_code == 200:

    data = response.json()

    st.success(
        f"{len(data['articles'])} news articles found!"
    )

    for article in data["articles"]:

        with st.container(border=True):

            # News Image
            if article.get("urlToImage"):
                st.image(
                    article["urlToImage"],
                    use_container_width=True
                )

            # News Title
            st.subheader(article["title"])

            # Description
            if article.get("description"):
                st.write(article["description"])

            # Source
            source = article.get("source", {}).get("name", "Unknown")
            st.caption("📰 Source: " + source)

            # Published Date
            date = article.get("publishedAt", "Date unavailable")
            st.caption("📅 Published: " + date[:10])

                       # Read More
            if article.get("url"):
                st.link_button(
                    "Read Full News →",
                    article["url"]
                )

            # Save News Button
            if st.button("⭐ Save News", key=article["url"]):
                if article not in st.session_state.saved_news:
                    st.session_state.saved_news.append(article)
                    save_saved_news(st.session_state.saved_news)
                    st.success("News saved permanently!")
                else:
                    st.info("News already saved!")         
else:
    st.error(
        f"News load nahi ho paayi: {response.status_code}"
    )

 
# My Saved News
st.divider()
st.header("⭐ My Saved News")

if st.session_state.saved_news:
    for i, news in enumerate(st.session_state.saved_news):

        st.write("📰 " + news["title"])

        st.link_button(
            "Read Saved News",
            news["url"]
        )

        if st.button("❌ Remove Bookmark", key=f"remove_{i}"):
            st.session_state.saved_news.pop(i)
            save_saved_news(st.session_state.saved_news)
            st.rerun()

else:
    st.info("No saved news yet!")

