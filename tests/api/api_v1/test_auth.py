import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.selectors.user import get_user_by_username
from app.utils.password import get_password_hash


# @pytest.mark.xfail
@pytest.mark.asyncio
async def test_signup_success(ac: AsyncClient):
    data = {
        "username": "testuser",
        "password": "password",
        "email": "user@test.com",
    }
    response = await ac.post("auth/signup", json=data)

    assert response.status_code == 400

    token = response.json()
    assert "detail" in token


@pytest.mark.asyncio
async def test_signup_missing_fields(ac: AsyncClient):
    """
    Test for missing fields like email
    """
    data = {"username": "", "password": ""}
    response = await ac.post("auth/signup", json=data)

    assert response.status_code == 422

    error = response.json()

    assert "field required" in error["detail"][0]["msg"]


@pytest.mark.asyncio
async def test_signup_username_already_in_use(ac: AsyncClient):
    # Create a user with the same username
    data = {
        "username": "testuser",
        "password": "password",
        "email": "user@test.com",
    }
    await ac.post("auth/signup", json=data)

    # Try to create another user with the same username
    data = {
        "username": "testuser",
        "password": "password",
        "email": "user@test.com",
    }
    response = await ac.post("auth/signup", json=data)

    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_signup_creates_user(ac: AsyncClient, session: AsyncSession):
    data = {
        "username": "testuser",
        "password": "password",
        "email": "user@test.com",
    }

    await ac.post("auth/signup", json=data)

    # Verify that the user was created in the database
    user = await get_user_by_username("testuser", session)
    session.commit()

    assert user.username == data["username"]
    assert user.email == data["email"]
    assert user.password == get_password_hash(data["password"])


@pytest.mark.asyncio
async def test_signin_success(ac: AsyncClient, test_user):
    # Test a successful signin
    data = {"username": "test", "password": "password"}
    response = await ac.post("auth/signin", json=data)

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_signin_error_incorrect_password(ac: AsyncClient, test_user):
    # Test an error if the password is incorrect
    data = {"username": "test", "password": "incorrectpassword"}
    response = await ac.post("auth/signin", json=data)

    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect username or password'}


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_signin_error_username_not_found(ac: AsyncClient):
    # Test an error if the username is not registered
    data = {"username": "unregistered_user", "password": "password123"}
    response = await ac.post("auth/signin", json=data)

    assert response.status_code == 400
    assert response.json() == {"detail": "User does not exists"}



@pytest.mark.asyncio
async def test_signin_error_username_required(ac: AsyncClient):
    # Test an error if the username is not provided
    data = {"password": "password123"}
    response = await ac.post("auth/signin", json=data)

    assert response.status_code == 422
    assert "field required" in response.json()["detail"][0]["msg"]


@pytest.mark.asyncio
async def test_signin_error_password_required(ac: AsyncClient):
    # Test an error if the password is not provided
    data = {"username": "test"}
    response = await ac.post("auth/signin", json=data)

    assert response.status_code == 422
    assert "password" in response.json()["detail"][0]["loc"]
    assert "field required" in response.json()["detail"][0]["msg"]

