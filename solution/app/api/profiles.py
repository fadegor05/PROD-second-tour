from app.api.api_router import api_router


@api_router.get('/profiles/{login}', response_model_exclude_none=True)
def get_profiles_by_login_handler():
    ...
    #TODO