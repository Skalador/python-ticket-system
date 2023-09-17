from main import app
import pytest


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200


def test_submit(client):
    new_ticket = {
        "subject": "Pass Test",
        "severity": "SEV1",
        "description": "This Test has to be passed!"
    }
    response = client.post('/submit', data=new_ticket, follow_redirects=True)

    # Assert that the response status code is 200 (successful submit)
    assert response.status_code == 200

    # Check that the new ticket is present based on the ticket's ID
    assert "<p>ID:0</p>" in str(response.data)


def test_delete(client):
    new_ticket = {
        "subject": "Test Ticket",
        "severity": "SEV2",
        "description": "Sample description"
    }
    response = client.post('/submit', data=new_ticket, follow_redirects=True)

    # Get the ID of the newly created ticket
    ticket_id = response.data.decode(
        "utf-8").split("<p>ID:")[1].split("</p>")[0]

    # Send a POST request to the /delete route with the ticket ID
    delete_response = client.post(
        '/delete', data={"id": ticket_id}, follow_redirects=True)

    # Assert that the response status code is 200 (successful delete)
    assert delete_response.status_code == 200

    # Check that the deleted ticket's ID is not present in the response data
    assert f"ID:{ticket_id}" not in str(delete_response.data)
