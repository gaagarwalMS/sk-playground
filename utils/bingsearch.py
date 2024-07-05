from semantic_kernel.functions import kernel_function
import requests
from dotenv import load_dotenv
import os

load_dotenv('C:\Projects\sk-projects\sk101\.env')

subscription_key = os.getenv("SUBSCRIPTION_KEY")
search_endpoint = os.getenv("SEARCH_ENDPOINT")

class SearchInternet:
    @kernel_function(
        name="search_internet",
        description="Searches the internet if the user asks of any information that may require some latest information/facts being searched on the internet and prints the search results."
    ) 

    async def search_bing(self, query: str):
        print("searching bing:")
        print(search_endpoint)
        print(subscription_key)  
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}  
        params = {"q": query, "textDecorations": True, "textFormat": "HTML"}  
        response = requests.get(search_endpoint, headers=headers, params=params)  
        response.raise_for_status()  
        search_results = response.json()

        results_prompt = ""
        # add logic to summarize the search results
        for snippet in search_results["webPages"]["value"]:
            results_prompt += snippet["snippet"] + "|||"

        # final_prompt = f"Here are the search results for {query}: {results_prompt} separated by |||. Can you please summarize the results to get the answer for"
        print(results_prompt)