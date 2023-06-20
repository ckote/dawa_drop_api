# whitelist_middleware.py
from django.http import HttpResponseForbidden


class IPWhitelistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # List of allowed IP addresses
        self.allowed_ips = ['192.168.1.1', '127.0.0.1']  # Add your desired IP addresses here

    def __call__(self, request):
        # Get the client's IP address from the request
        client_ip = request.META.get('REMOTE_ADDR')

        # Check if the client's IP is in the whitelist
        if client_ip not in self.allowed_ips:
            return HttpResponseForbidden("You are not allowed to access this resource.")

        return self.get_response(request)
