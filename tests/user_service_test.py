import unittest
from unittest.mock import MagicMock, patch
from fastapi import Response, status

from src.models.user_model import User
from src.services.password_service import hash_and_spice_password
from src.services.user_service import check_password



class TestUserService(unittest.TestCase):
    class TestUserService(unittest.TestCase):
        def test_check_password_correct(self):
            # GIVEN
            # create a User
            id = 12345
            password = "password"
            salt = "salty"
            user = User(password, salt)
            user.id = id
            user.password = hash_and_spice_password(password)

            # mocking the query method of Session
            with patch('src.database.database_setup.Session') as mock_session:
                mock_query = MagicMock(return_value=user)
                mock_session.return_value.query = mock_query

                # WHEN
                result = check_password(id, password)

                # THEN
                self.assertEqual(result, Response(content="Password is correct", status_code=status.HTTP_202_ACCEPTED))
                mock_query.assert_called_once_with(
                    User)  # Ensure that the query method was called with the expected model
