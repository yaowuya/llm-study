from fastapi import Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from apps.study.entity.decode_form import DecodeForm
from apps.study.entity.encode_form import EncodeForm
from core.renderer.common_response_schema import CommonResponseSchema
from core.utils.crypto_utils import CryptoUtils

study_api = InferringRouter()


@cbv(study_api)
class StudyApi:
    @study_api.post("/v1/encode", response_model=CommonResponseSchema, name="对密码进行加密")
    async def encode(self, data: EncodeForm = Body(None, description="加密的对象")) -> CommonResponseSchema:
        encrypt_content = CryptoUtils.encrypt(data.content)
        return CommonResponseSchema(data=encrypt_content, message="操作成功", success=True)

    @study_api.post("/v1/decode", response_model=CommonResponseSchema, name="对密码进行解密")
    async def decode(self, data: DecodeForm = Body(None, description="解密的对象")) -> CommonResponseSchema:
        encrypt_content = CryptoUtils.decrypt(data.content)
        return CommonResponseSchema(data=encrypt_content, message="操作成功", success=True)
