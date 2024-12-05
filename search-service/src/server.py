import json

from fastapi.exceptions import RequestValidationError

from src.dto.request_details import RequestDetails
from src.helpers.db_helper import DBHelper
from src.helpers.search_helper import SearchHelper
from src.logfactory import LogFactory
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.middlewares.error_middleware import ErrorHandlingMiddleware
from src.middlewares.request_validation_middleware import RequestValidationMiddleware
from src.middlewares.log_middleware import LoggingMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

config = json.load(open("src/config.json", "r"))

# logging related initializations
logFactory = LogFactory(config)
logger = logFactory.get_logger(__name__)
# end of logging related initializations

db_client = DBHelper(config, logFactory)
search_helper = SearchHelper(config, db_client, logFactory)

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
		"error": { "code": "INVALID_SEARCH", "message": str(exc),},
		"status": "FAILURE",
	}, status_code=422)

@app.get('/search')
def do_search(request: Request, id: int | None = None, 
              is_random: bool = True):
	"""
	Handles search requests by retrieving results based on a provided ID or generating a random one.

	Args:
		request (Request): The incoming HTTP request object.
		id (int | None, optional): The ID to search for. Defaults to None.
		is_random (bool, optional): Flag to determine whether to generate a random ID. Defaults to True.

	Raises:
		HTTPException: Raised with a 400 status code if required headers are missing.
		HTTPException: Raised with a 422 Unprocessable Entity status code if the input is invalid 
					(e.g., ID is not an integer or is_random is not a boolean).
		HTTPException: Raised with a 500 status code if the ID is not found or for any other exceptions.

	Returns:
		JSONResponse: A JSON object containing the search results.
	"""
	request_details: RequestDetails = RequestDetails(create_extra_log_context(request))
	query_idx: int = None
	if is_random: query_idx = search_helper.get_random_playlist_index()
	elif not is_random and id is not None: query_idx = id
		
	logger.info(f"Final query idx:: {query_idx}", extra=request_details.asdict())
	if query_idx is None or query_idx < 0: raise Exception("INVALID_QUERY_IDX")

	search_results = search_helper.get_search_results_from_query(int(query_idx), 
													request=request_details.asdict())
	return JSONResponse({"results": search_results, "count": len(search_results), "status": "SUCCESS"})

def create_extra_log_context(request, **kwargs):
    context = {
        "requestid": request.headers["requestid"],
        "endpoint": request.headers["endpoint"]
    }
    return {**context, **kwargs.get("context")} if "context" in kwargs else context
