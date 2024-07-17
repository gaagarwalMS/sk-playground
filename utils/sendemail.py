from semantic_kernel.functions import kernel_function

class EmailPlugin:
    @kernel_function(
        name="send_email",
        description="Generates an email to the recipient email according to the purpose specified. Please print the email content to the console.",
    )
    async def send_email(self, recipient_email: str):
        print("Email sent!")