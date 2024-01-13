def test_homestead_io(openai):
    response = openai.homestead("What should Herrera Homestead focus on as an emerging new business?qw  ")
    assistant_response = openai.parse_response(response)
    openai.save_test_artifact(data=assistant_response)
    assert response is not None