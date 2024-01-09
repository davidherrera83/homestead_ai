
def test_homestead_io(openai):
    response = openai.homestead("What are the states with no income tax?")
    assert response.status_code == 200
