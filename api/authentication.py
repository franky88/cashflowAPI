from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            # Inject it into the header so the parent method can process it
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        return super().authenticate(request)
