from .authentication import urlpatterns as auth_urls
from .data_retriever import urlpatterns as data_retriever_urls
from .registration import urlpatterns as registration_urls

urlpatterns = [
    *auth_urls,
    *data_retriever_urls,
    *registration_urls,
]
