def test_homestead_io(openai):
    response = openai.homestead("What should Herrera Homestead focus on as an emerging new business?")
    assistant_response = openai.parse_response(response)
    openai.save_test_artifact(data=assistant_response)
    assert response is not None

def test_file_manipulation(openai, new_file):
    file_id = new_file.json()["id"]

    list_file_response = openai.list_files()
    assert list_file_response.status_code == 200
    files = list_file_response.json()
    file_ids = [file['id'] for file in files['data']]
    assert file_id in file_ids, "Uploaded file ID should be in the list of files"


    file_deletion = openai.delete_file(file_id)
    assert file_deletion.status_code == 200

