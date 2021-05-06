from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    # test command when db is already available
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # if operational error is not thrown, then db is available
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            # return_value: Set this to configure the value returned
            # by calling the mock
            gi.return_value = True
            # name of the management command that we are going to create
            call_command("wait_for_db")
            # call_count: An integer telling you how many times the
            # mock object has been called
            self.assertEqual(gi.call_count, 1)

    # replace the behavior of time.sleep with return_value=True
    # decorator is a wrapper function
    # check if gonna raise error, then wait for 1s
    # remove the delay, dont actually sleep in test
    @patch("time.sleep", return_value=True)
    def test_wait_for_db(self, ts):
        # ts is the returned value of mock_time_sleep
        """Test waiting for db"""
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            # side_effect: This can either be a function to be
            # called when the mock is called, an iterable or an
            # exception (class or instance) to be raised.
            # mock = Mock()
            # mock.side_effect = [3, 2, 1]
            # mock(), mock(), mock()
            # (3, 2, 1)
            # mock this gi behavior
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command("wait_for_db")
            # the __getitem__ mock will get called 6 times
            # when wait_for_db command is called
            self.assertEqual(gi.call_count, 6)
