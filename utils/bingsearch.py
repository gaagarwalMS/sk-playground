from semantic_kernel.functions import kernel_function
from dotenv import load_dotenv

class SearchInternet:
    @kernel_function(
        name="search_internet",
        description="Searches the internet if the user asks of any information that may require some latest information/facts being searched on the internet."
    ) 

    async def search_bing(self, query: str):
        # Add logic to send an email using the recipient_emails, subject, and body
        # For now, we'll just print out a success message to the console
        print("Email sent!")