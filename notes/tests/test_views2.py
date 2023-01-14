import pytest
from notes.models import Notes
from .factories import UserFactory, NotesFactory

@pytest.fixture
def logged_user(client):
    user = UserFactory()
    client.login(username = user.username, password = 'password')
    return user

@pytest.mark.django_db
def test_list_endpoint_return_user_notes(client, logged_user):
    note = NotesFactory(user = logged_user)
    note2 = NotesFactory(user = logged_user)
    response = client.get(path='/smart/notes')
    assert response.status_code == 200
    content = str(response.content)
    assert note.title in content
    assert note2.title in content
    assert 2 == content.count("<h3>")

@pytest.mark.django_db
def test_list_endpoint_go_to_login_page_from_authenticated_user(client):
    response = client.get(path='/smart/notes', follow=True)
    assert response.status_code == 200
    assert "home/login.html" in response.template_name

@pytest.mark.django_db
def test_list_endpoint_only_list_notes_from_authenticated_user(client, logged_user):
    user2 = UserFactory()
    note = NotesFactory(user = logged_user)
    note2 = NotesFactory(user = logged_user)
    note3 = NotesFactory(user = user2)
    note4 = NotesFactory(user = user2)
    response = client.get(path='/smart/notes')
    assert response.status_code == 200
    content = str(response.content)
    assert note.title in content
    assert note2.title in content
    assert note3.title not in content
    assert note4.title not in content
    assert 2 == content.count("<h3>")

@pytest.mark.django_db
def test_create_view_endpoint_receives_form_data(client, logged_user):
    form_data = {'title': 'some title', 'text': 'some text'}
    response = client.post(path='/smart/notes/new', data=form_data, follow=True)

    assert response.status_code == 200
    assert 'notes/notelist.html' in response.template_name
    assert 1 == logged_user.notes.count()
    assert form_data['title'] in str(response.content)
    assert form_data['text'] in str(response.content)