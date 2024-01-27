import requests
import time
import uuid
import os

from fw import Endpoint, Files


class Openai:

    def homestead(self, user_query: str, timeout: int = 5):
        thread_id = self.create_thread()
        self.create_message(user_query=user_query)
        run_id = self.create_run(thread_id=thread_id)

        while True:
            status = self.retrieve_run(thread_id, run_id)
            if status == "completed":
                break
            elif status == "failed":
                raise Exception("Run failed")
            else:
                time.sleep(timeout)

        messages_response = self.list_messages(thread_id)

        return messages_response.json()

    def list_messages(self, thread_id: str):

        url = f"https://api.openai.com/v1/threads/{thread_id}/messages"
        headers = Endpoint.headers

        response = requests.get(url=url, headers=headers)
        if response.ok:
            return response
        else:
            raise ConnectionError(
                "Response was not OK: " + str(response.content))
    
    def save_test_artifact(self, data: str, directory: str = "tests/test_artifacts", file_name: str = "test_artifact.txt"):
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, file_name)
        with open(file_path, "w") as file:
            file.write(data)


    def create_thread(self):
        url = Endpoint.threads
        headers = Endpoint.headers
        response = requests.post(url=url, headers=headers)
        if response.ok:
            return response.json()['id']
        else:
            raise ConnectionError(
                "Response was not OK: " + str(response.content))

    def create_message(self, user_query: str):
        thread_id = self.create_thread()
        url = Endpoint.threads + f"/{thread_id}/messages"
        headers = Endpoint.headers
        payload = {
            "role": "user",
            "content": f"{user_query}",
        }
        response = requests.post(url=url, headers=headers, json=payload)
        if response.ok:
            return response.json()['id']
        else:
            raise ConnectionError(
                "Response was not OK: " + str(response.content))

    def create_run(self, thread_id: str):
        url = Endpoint.threads + f"/{thread_id}/runs"
        headers = Endpoint.headers
        payload = {
            "assistant_id": f"{Endpoint.assistant_id}"
        }
        response = requests.post(url=url, headers=headers, json=payload)
        if response.ok:
            return response.json()['id']
        else:
            raise ConnectionError(
                "Response was not OK: " + str(response.content))

    def retrieve_run(self, thread_id: str, run_id: str):
        url = Endpoint.threads + f"/{thread_id}/runs/{run_id}"
        headers = Endpoint.headers
        response = requests.get(url=url, headers=headers)
        if response.ok:
            return response.json()['status']
        else:
            raise ConnectionError(
                "Response was not OK: " + str(response.content))

    def upload_file(self, path: str = f'{Files.hh_context}'):
        url = Endpoint.files
        headers = Endpoint.file_headers
        files = {'file': open(path, 'rb')}
        data = {
            "purpose": "assistants"
        }
        response = requests.post(url, headers=headers, data=data, files=files)
        if response.ok:
            return response.json()['id']
        else:
            raise ConnectionError("Response was not OK: " + str(response.content))
        
    def list_files(self):
        url = Endpoint.files
        headers = Endpoint.headers
        response = requests.get(url=url, headers=headers)
        if response.ok:
            return response
        else:
            raise ConnectionError(
                "Response was not OK: " + str(response.content))
        
    def delete_file(self, file_id: str):
        url = Endpoint.files + f"/{file_id}"
        headers = Endpoint.headers
        response = requests.delete(url=url, headers=headers)
        if response.ok:
            return response
        else:
            raise ConnectionError(
                "Response was not OK: " + str(response.content))
        