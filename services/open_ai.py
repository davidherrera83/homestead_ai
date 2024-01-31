import time

from openai import OpenAI
from fw import Files, get_secret



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
        
    def upload_files(self):
        try:
            file = self.client.files.create(
                file=open(f"{Files.hh_context}", "rb"),
                purpose="assistants"
            )
            return file.id
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None
        
    def delete_file(self, file_id: str):
        try:
            file = self.client.files.delete(file_id)
            return file.deleted
        except Exception as e:
            print (f"Error deleting file: {e}")
            return False
          