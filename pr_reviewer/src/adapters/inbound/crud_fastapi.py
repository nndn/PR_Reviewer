
from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from src.ports.crud_application import ICrudApplication
from src.domain.exceptions import ResourceNotFound
from dataclasses import asdict
from src.adapters.inbound.http_api_schemas import \
HealthCheck, AnalyzePrRequest, AnalyzePrResponse, TaskResultResponse, TaskStatusResponse


class CrudFastapiAdapter:

    def __init__(self, application:ICrudApplication):
        self.application = application
        
    def get_router(self) -> FastAPI:
        return get_router(self.application)


def get_router(application:ICrudApplication) -> FastAPI: 
    app = FastAPI(title="pr_agent crud server")
    
    @app.get("/health")
    async def health_check() -> HealthCheck:
        return HealthCheck(status="OK")
    
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui():
        return get_swagger_ui_html(openapi_url="/openapi.json", title="API Documentation")
    
    @app.post("/analyze-pr")
    async def analyze_pr(req: AnalyzePrRequest) -> AnalyzePrResponse:
        task_id = application.add_review_task(req.repo_url, pr_number=req.pr_number, auth_token=req.github_token)
        return AnalyzePrResponse(accepted=True, repo_url=req.repo_url, task_id=task_id)
    
    @app.get("/status/{task_id}")
    async def get_task_status(task_id:int) -> TaskStatusResponse:
        try:
            status = application.get_review_status(task_id)
        except (ResourceNotFound):
            raise HTTPException(status_code=404, detail="task not found")
        return TaskStatusResponse(task_id=task_id, status=status)
    
    @app.get("/results/{task_id}")
    async def get_task_result(task_id:int) -> TaskResultResponse:
        try:
            status, review = application.get_review_result(task_id)
        except (ResourceNotFound):
            raise HTTPException(status_code=404, detail="task not found")
        response = TaskResultResponse(task_id=task_id, status=status)
        if review is not None:
            response.results = asdict(review)
        return response
    
    return app

