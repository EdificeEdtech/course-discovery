"""Custom API throttles."""
from rest_framework.throttling import UserRateThrottle

from course_discovery.apps.core.models import UserThrottleRate


class OverridableUserRateThrottle(UserRateThrottle):
    """Rate throttling of requests, overridable on a per-user basis."""

    def allow_request(self, request, view):
        user = request.user

        if user and user.is_authenticated():
            if user.is_superuser or user.is_staff:
                return True
            try:
                # Override this throttle's rate if applicable
                user_throttle = UserThrottleRate.objects.get(user=user)
                self.rate = user_throttle.rate
                self.num_requests, self.duration = self.parse_rate(self.rate)
            except UserThrottleRate.DoesNotExist:
                pass

        return super(OverridableUserRateThrottle, self).allow_request(request, view)
