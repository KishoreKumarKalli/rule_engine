from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from rule_engine.ast_node import Node
from rule_engine.parser import create_rule
from rule_engine.evaluator import evaluate_rule

app = FastAPI()

class RuleRequest(BaseModel):
    rule_string: str

class EvaluationRequest(BaseModel):
    rule: Dict[str, Any]
    data: Dict[str, Any]

@app.post("/api/rules/create")
async def create_rule_endpoint(request: RuleRequest):
    try:
        ast = create_rule(request.rule_string)
        return ast.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/rules/evaluate")
async def evaluate_rule_endpoint(request: EvaluationRequest):
    try:
        result = evaluate_rule(request.rule, request.data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))