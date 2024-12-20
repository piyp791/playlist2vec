import json
import os

from fastapi.exceptions import RequestValidationError

from src.helpers.autocomplete_helper import AutocompleteHelper
from src.helpers.db_helper import DBHelper
from src.logfactory import LogFactory
from src.middlewares.error_middleware import ErrorHandlingMiddleware
from src.middlewares.log_middleware import LoggingMiddleware
from src.middlewares.request_validation_middleware import RequestValidationMiddleware
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

config = json.load(open("src/config.json", "r"))

# logging related initializations
logFactory = LogFactory(config)
logger = logFactory.get_logger(__name__)
# end of logging related initializations

is_mini = os.getenv("IS_MINI", "false").lower() == "true"
logger.info(f"Is mini environment variable:: {str(is_mini)}")

db_client = DBHelper(config, logFactory, is_mini)
search_helper = AutocompleteHelper(config, db_client, logFactory)

app = FastAPI()
app.add_middleware(RequestValidationMiddleware)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware, logFactory=logFactory)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
	return JSONResponse({
		"error": { "code": "HTTP_ERROR", "message": exc.detail,},
		"status": "FAILURE",
	}, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
	return JSONResponse({
		"error": { "code": "INVALID_INPUT", "message": str(exc),},
		"status": "FAILURE",
	}, status_code=422) 

@app.get('/populate')
def complete(term: str = Query(min_length=1, max_length=50)):
	"""
	Provides autocomplete suggestions based on the given search term.

	Args:
		term (str): The search term for which suggestions are generated. Must be between 1 and 50 characters.

	Raises:
		HTTPException: Raised with a 400 status code if required headers (e.g., requestid or endpoint) are missing.
		HTTPException: Raised with a 422 Unprocessable Entity status code if the input term is invalid 
					(e.g., not within the allowed length of 1 to 50 characters).
		HTTPException: Raised with a 500 status code for any other exceptions.

	Returns:
		JSONResponse: A JSON object containing:
					- Suggestions: The list of autocomplete suggestions.
					- Count: The number of suggestions returned.
					- Status: The status of the request.
	"""
	suggestions = search_helper.auto_complete(term)
	response = {
		"results": suggestions,
		"count": len(suggestions),
		"status": "SUCCESS",
		}
	return JSONResponse(response)


