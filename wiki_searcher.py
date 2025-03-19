import os
from elasticsearch import Elasticsearch

class WikiSearcher:
    """
    A class to interact with an Elasticsearch index for performing search queries.
    """

    def __init__(self, index_name='wiki_en', url: str = "https://localhost:9200"):
        """
        Initializes the ElasticsearchSearcher with the given configuration.

        Args:
            index_name (str): Name of the Elasticsearch index.
            hostname (str, optional): Elasticsearch hostname. Defaults to 'localhost'.
            port (int, optional): Elasticsearch port. Defaults to 9200.
            size (int, optional): Number of search results to return. Defaults to 10.
        """

        self.index_name = index_name
        self.es = self.create_es_client(url)

        # Verify connection
        if not self.es.ping():
            raise ConnectionError(f"Cannot connect to Elasticsearch at {url}")

    def search(self, query, size=5):
        """
        Searches the Elasticsearch index for documents matching the query.

        Args:
            query (str): The search query string.

        Returns:
            list: A list of dictionaries containing search results.
        """
        # Define the search query using multi_match to search in 'title' and 'text' fields
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "text"] 
                }
            },
            "size": size
        }

        # Execute the search
        response = self.es.search(index=self.index_name, body=search_body)

        # Parse the search results
        results = [
            {
                'id': hit['_id'],
                'score': hit['_score'],
                'url': hit['_source'].get('url', ''),           # Add 'url' to the result if available in the document
                'title': hit['_source'].get('title', ''),       # Add 'title' to the result if available in the document
                'content': hit['_source'].get('text', '')       # Add 'text' to the result if available in the document
            }
            for hit in response['hits']['hits']
        ]
        return results

    def close(self):
        """
        Closes the Elasticsearch connection.
        """
        self.es.close()

    @staticmethod
    def create_es_client(url: str) -> Elasticsearch:
        """Initialize Elasticsearch client with environment configuration."""
        if not os.environ.get('ELASTIC_PASSWORD'):
            raise ValueError('ELASTIC_PASSWORD environment variable not set')

        return Elasticsearch(
            url,
            basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD")),
            verify_certs=False,
            ssl_show_warn=False,
        )

def main():
    """
    Main function to handle command-line arguments and perform searches.
    """
    # Parse command-line arguments
    query = "Paris 2024 Olympic Games"

    try:
        # Initialize the searcher
        searcher = WikiSearcher()

        # Perform the search
        results = searcher.search(query)

        # Display the results
        if not results:
            print("No relevant documents found.")
        else:
            for idx, doc in enumerate(results, start=1):
                print(f"Result {idx}:")
                print(f"ID: {doc['id']}")
                print(f"Score: {doc['score']}")
                print(f"Title: {doc['title']}")
                print(f"Content: {doc['content']}\n")

    except ConnectionError as ce:
        print(f"Connection Error: {ce}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure the Elasticsearch connection is closed
        if 'searcher' in locals():
            searcher.close()

if __name__ == '__main__':
    main()
