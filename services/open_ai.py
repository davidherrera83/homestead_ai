import time

from openai import OpenAI
from fw import get_secret



class Openai:
    def __init__(self) -> None:
        api_key = get_secret().api_key
        self.client = OpenAI(api_key=api_key)

    def create_thread(self):
        try:
            thread = self.client.beta.threads.create()
            return thread.id
        except Exception as e:
            print(f"Error creating message thread: {e}")
            return None
    
    def create_message(self, user_query, thread_id):
        try:
            thread_message = self.client.beta.threads.messages.create(
                f"{thread_id}",
                role = "user",
                content = user_query
            )
            return thread_message.id
        except Exception as e:
            print(f"Error creating message: {e}")
            return None
        
    def create_run(self, thread_id: str):
        try:
            run = self.client.beta.threads.runs.create(
                thread_id= f"{thread_id}",
                assistant_id= f"{get_secret().assistant_id}"
            )
            return run.id
        except Exception as e:
            print(f"Error creating run: {e}")
            return None

    def retrieve_run(self, thread_id: str, run_id: str):
        try:
            run = self.client.beta.threads.runs.retrieve(
                thread_id = f"{thread_id}",
                run_id = f"{run_id}"
            )
            return run.status
        except Exception as e:
            print(f"Error retrieving run: {e}")
            return None
        
    def list_messages(self, thread_id: str):
        try:
            thread_messages = self.client.beta.threads.messages.list(
                f"{thread_id}"
            )
            return thread_messages.data
        except Exception as e:
            print(f"Error listing messages: {e}")
            return None

    def homestead(self, user_query: str, timeout: int = 5, max_wait_time: int = 60):
        start_time = time.time()
        thread_id = self.create_thread()
        self.create_message(user_query, thread_id)
        run_id = self.create_run(thread_id)

        while True:
            if time.time() - start_time > max_wait_time:
                raise TimeoutError("Exceeded maximum wait time for response")

            status = self.retrieve_run(thread_id, run_id)
            if status == "completed":
                break
            elif status == "failed":
                raise Exception("Run failed")
            else:
                time.sleep(timeout)

        messages_response = self.list_messages(thread_id)
        return messages_response

          