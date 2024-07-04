import os  
import asyncio
from dotenv import load_dotenv  
from semantic_kernel import Kernel  
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion  
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase  
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior  
from semantic_kernel.functions.kernel_arguments import KernelArguments  
from semantic_kernel.contents import ChatHistory  
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (  
    AzureChatPromptExecutionSettings,  
)  
  
async def main():  
    try:  
        # Get configuration settings  
        load_dotenv()  
        azure_oai_key = os.getenv("AZURE_OAI_KEY")  
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")  
        azure_oai_baseuri = os.getenv("AZURE_OAI_ENDPOINT")  
  
        if not all([azure_oai_key, azure_oai_deployment, azure_oai_baseuri]):  
            raise ValueError("Azure OpenAI configuration is not set correctly in .env file")  
  
        kernel = Kernel()  
        kernel.add_service(AzureChatCompletion(  
            deployment_name=azure_oai_deployment,  
            api_key=azure_oai_key,  
            base_url=azure_oai_baseuri  
        ))  
  
        chat_completion: AzureChatCompletion = kernel.get_service(type=ChatCompletionClientBase)  
  
        # Enable planning  
        execution_settings = AzureChatPromptExecutionSettings()  
  
        chatHistory = ChatHistory(system_message="""
            You are a friendly assitant who is built to help me with my software development tasks.
            """)
  
        # Initiate a back-and-forth chat  
        while True:  
            try:  
                # Collect user input  
                userInput = input("User > ")  
  
                # Terminate the loop if the user says "quit"  
                if userInput.lower() == "quit":  
                    break  
  
                if len(userInput) == 0:  
                    print("Please enter a prompt.")  
                    continue  
  
                # Add user input to the chat history  
                chatHistory.add_user_message(userInput)
  
                # Get the response from the AI  
                result = (await chat_completion.get_chat_message_contents(  
                    chat_history=chatHistory,  
                    settings=execution_settings,  
                    kernel=kernel,  
                    arguments=KernelArguments(),  
                ))[0]  
  
                # Print the results  
                print("Assistant > " + str(result))
                print("_" * 40)  
  
                # Add the message from the agent to the chat history  
                chatHistory.add_assistant_message(str(result))
  
            except Exception as inner_ex:  
                print(f"An error occurred during the chat loop: {inner_ex}")  
  
    except Exception as ex:  
        print(f"An error occurred in the main function: {ex}")
  
if __name__ == '__main__':  
    asyncio.run(main())