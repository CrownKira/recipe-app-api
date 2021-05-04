from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        # run before every test that we run
        # life cycle method
        # create test client
        # create a new user, regular user that is not auth, etc
        self.client = Client()
        # self.admin_user: to make it available to all other methods below
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@londonappdev.com", password="password123"
        )
        # force_login: client helper function
        # allows to log a user in
        # client represents a person, a person can login, etc
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@londonappdev.com",
            password="password123",
            name="Test user full name",
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # reverse helper function: used to create url
        # generate url for our list user page
        # url is:  /admin/core/user/
        url = reverse("admin:core_user_changelist")
        # use our test client to perform http get
        # ie. will have the auth token
        res = self.client.get(url)

        # checks the res contains the certain item
        # check http response is 200, etc
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        # make sure the change page renders correctly
        # not recommended to test the dependencies of ur project
        # just need to make sure the code that we write runs correctly
        """Test that user edit page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        # /admin/core/user/id
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
