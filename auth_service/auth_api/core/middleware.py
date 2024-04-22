from starlette.responses import JSONResponse

from core.exceptions import exception_mappings


async def handle_exceptions(request, call_next):
    try:
        return await call_next(request)
    except tuple(exception_mappings) as error:
        status_code = exception_mappings[type(error)]
        return JSONResponse(status_code=status_code, content={"message": str(error)})
