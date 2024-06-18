# routes/__init__.py
from fastapi import APIRouter
from controllers import reports   # Import your routers
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Create a central router
router = APIRouter()

# Include the routers from controllers
router.include_router(reports.router, prefix="/reports")
# Add more include_router statements for other controllers

# Additional common routes or middleware can be added directly to this router if needed
# For example: router.add_api_route("/", some_function)

app = FastAPI()
class NoDataError:
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

@app.exception_handler(NoDataError)
async def exception_handle(request: Request, exe: NoDataError):
    return JSONResponse(
        status_code=exe.error_code,
        content={"Error Message": exe.message}
        )

# Export the central router
__all__ = ["router"]
