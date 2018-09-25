from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyCurrentUserAccessMixin(UserPassesTestMixin):
    """ Only current user has access to view """
    def test_func(self):
        return self.request.user.get_username() == self.kwargs['username']
