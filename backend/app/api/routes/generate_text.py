from fastapi import APIRouter

router = APIRouter(prefix="/gentext")

@router.post("testmodel")
def testmodel(prompt: str):
    return {
        "prompt": prompt
    }