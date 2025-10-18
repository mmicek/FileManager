from rest_framework.routers import DefaultRouter


class BaseRouter(DefaultRouter):
    """
    Ensure both endpoint with/without '/' will work. By default, it is required.
    """

    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"
