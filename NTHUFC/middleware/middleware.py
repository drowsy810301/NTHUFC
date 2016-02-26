from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
class RestrictStaffToAdminMiddleware(object):
    """
    A middleware that restricts staff members access to administration panels.
    """
    def process_request(self, request):
        if request.path.startswith(reverse('admin:index')):
            if request.user.is_authenticated():
                if not request.user.is_staff:
                    raise PermissionDenied

