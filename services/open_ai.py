
import requests
import time

from models.token import TokenModel
from fw import Endpoint, OpenAI, get_token


class Openai:
    def __init__(self, token: TokenModel):
        self.token = token


    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token.api_key}",
            "OpenAI-Beta": "assistants=v1"
        }

    def homestead(self, text: str, timeout: int = 5):
        thread_id = self.create_thread()
        self.create_message(text=text)
        run_id = self.create_run(thread_id=thread_id)

        while True:
            status = self.retrieve_run(thread_id, run_id)
            if status == "completed":
                break
            elif status == "failed":
                raise Exception("Run failed")
            else:
                time.sleep(timeout)

        return self.list_message(thread_id)
    
    def list_message(self, thread_id: str):


        url = f"https://api.openai.com/v1/threads/{thread_id}/messages"
        headers = OpenAI.headers

        response = requests.get(url=url, headers=headers)
        if response.ok:
            return response
        else:
            raise ConnectionError(
                "Response was not OK: " + str(response.content))

    def create_thread(self):
        url = Endpoint.threads
        headers = OpenAI.headers
        response = requests.post(url=url, headers=headers)
        if response.ok:
            return response.json()['id']
        else:
            raise ConnectionError(
                "Response was not OK: " + str(response.content))

    def create_message(self, text: str):
        thread_id = self.create_thread()
        url = Endpoint.threads + f"/{thread_id}/messages"
        headers = OpenAI.headers
        payload = {
            "role": "user",
            "content": f"{text}",
            "file_ids": ["file-1IWyqznJRKnfvRBwV4esVbuz"]
        }
        response = requests.post(url=url, headers=headers, json=payload)
        if response.ok:
            return response.json()['id']
        else:
            raise ConnectionError(
                "Response was not OK: " + str(response.content))

    def create_run(self, thread_id: str):
        url = Endpoint.threads + f"/{thread_id}/runs"
        headers = OpenAI.headers
        payload = {
            "assistant_id": f"{OpenAI.assistant_id}"
        }
        response = requests.post(url=url, headers=headers, json=payload)
        if response.ok:
            return response.json()['id']
        else:
            raise ConnectionError(
                "Response was not OK: " + str(response.content))

    def retrieve_run(self, thread_id: str, run_id: str):
        url = Endpoint.threads + f"/{thread_id}/runs/{run_id}"
        headers = OpenAI.headers
        response = requests.get(url=url, headers=headers)
        if response.ok:
            return response.json()['status']
        else:
            raise ConnectionError(
                "Response was not OK: " + str(response.content))
