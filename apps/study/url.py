from fastapi_utils.inferring_router import InferringRouter

from apps.study.api.study_api import study_api

core_api = InferringRouter()
core_api.include_router(study_api, prefix="/study", tags=["Study"])
