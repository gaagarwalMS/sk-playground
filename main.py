import os  
import asyncio
import logging 

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
from utils.sendemail import EmailPlugin;
from utils.bingsearch import SearchInternet;
  
async def main():  
    try:  
        # Get configuration settings  
        load_dotenv()  
        azure_oai_key = os.getenv("AZURE_OAI_KEY")  
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")  
        azure_oai_baseuri = os.getenv("AZURE_OAI_ENDPOINT")
        search_endpoint = os.getenv("SEARCH_ENDPOINT")
        subscription_key = os.getenv("SUBSCRIPTION_KEY")  
  
        if not all([azure_oai_key, azure_oai_deployment, azure_oai_baseuri]):  
            raise ValueError("Azure OpenAI configuration is not set correctly in .env file")  
  
        kernel = Kernel()  
        kernel.add_service(AzureChatCompletion(  
            deployment_name=azure_oai_deployment,  
            api_key=azure_oai_key,  
            base_url=azure_oai_baseuri  
        ))

        # Set the logging level for  semantic_kernel.kernel to DEBUG.
        logging.basicConfig(
            format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.getLogger("kernel").setLevel(logging.DEBUG)

        kernel.add_plugin(
            EmailPlugin(),
            plugin_name="Email"
        )
        kernel.add_plugin(
            SearchInternet(),
            plugin_name="SearchInternet"
        )  
  
        chat_completion: AzureChatCompletion = kernel.get_service(type=ChatCompletionClientBase)  
  
        # Enable planning  
        execution_settings = AzureChatPromptExecutionSettings(tool_choice="auto")
        execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(auto_invoke=True, filters={})  
  
        chatHistory = ChatHistory(system_message="""
                You are a friendly assistant who likes to follow the rules. You will complete required steps
                and request approval before taking any consequential actions. If the user doesn't provide
                enough information for you to complete a task, you will keep asking questions until you have
                enough information to complete the task.
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