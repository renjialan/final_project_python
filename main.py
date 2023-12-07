from db_manager import (
    create_connection, 
    insert_post, 
    create_sources_table, 
    create_posts_table, 
    get_or_insert_source
)
from news_api_client import fetch_news

def count_words(content, words):
    return sum(content.lower().count(word.lower()) for word in words)

def main():
    database_path = 'database.db'
    conn = create_connection(database_path)

    if conn is not None:
        create_sources_table(conn)
        create_posts_table(conn)

    
    search_queries = ['technology innovations', 'job market trends', 'economic recession', 'company hiring trends']
    neutral_words = ['technology', 'innovation']
    negative_words = ['recession', 'unemployment']
    positive_words = ['hiring', 'growth']

    for query in search_queries:
        articles = fetch_news(query)
        for article in articles:
            source_id = get_or_insert_source(conn, article['source']['name'])
            
            neutral_count = count_words(article['content'], neutral_words)
            negative_count = count_words(article['content'], negative_words)
            positive_count = count_words(article['content'], positive_words)
            insert_post(conn, source_id, article['content'], article['publishedAt'], neutral_count, negative_count, positive_count)

    conn.close()

if __name__ == '__main__':
    main()
