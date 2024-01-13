import requests
import time
import os

from fw import Endpoint


class Openai:

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

    def parse_response(self, messages: dict):
        for message in messages.get('data', []):
            if message.get("role") == "assistant":
                content_list = message.get("content", [])
                if content_list and isinstance(content_list, list):
                    for content in content_list:
                        if "text" in content and "value" in content["text"]:
                            return content["text"]["value"]

        return None
    
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

    def create_message(self, text: str):
        thread_id = self.create_thread()
        url = Endpoint.threads + f"/{thread_id}/messages"
        headers = Endpoint.headers
        payload = {
            "role": "user",
            "content": f"{text}",
            "file_ids": [f"{Endpoint.file_id}"]
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

    def list_files(self):
        url = Endpoint.files
        headers = Endpoint.headers
        response = requests.get(url=url, headers=headers)
        if response.ok:
            return response.json()
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
        