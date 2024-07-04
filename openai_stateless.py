import os

from openai import AzureOpenAI
from dotenv import load_dotenv
from typing import Annotated

def main():
    try:
        # Get configuration settings  
        load_dotenv()  
        azure_oai_key = os.getenv("AZURE_OAI_KEY")  
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")  
        azure_oai_baseuri = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_apiversion = os.getenv("AZURE_OAI_APIVERSION")

        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
                    azure_endpoint = azure_oai_baseuri, 
                    api_key=azure_oai_key,  
                    api_version=azure_oai_apiversion
                )
    
        # Create a system message
        system_message = """I am a software developer assistant who helps his users learn about software development.
            """
           
        while True:
            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            print("\nSending request for summary to Azure OpenAI endpoint...\n\n")
            
            # Send request to Azure OpenAI model
            response = client.chat.completions.create(
                model=azure_oai_deployment,
                temperature=0.7,
                max_tokens=400,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": input_text}
                ]
            )
            generated_text = response.choices[0].message.content

            # Print the response
            print("Response: " + generated_text + "\n")

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()