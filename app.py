from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import os
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


class RuleRequest(BaseModel):
    rule_string: str


class EvaluationRequest(BaseModel):
    rule: Dict[str, Any]
    data: Dict[str, Any]


class Node:
    def __init__(self, type_: str, value=None, left=None, right=None):
        self.type = type_
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }


def parse_rule(rule_string: str) -> Node:
    # Split the rule into tokens
    tokens = rule_string.replace('(', ' ( ').replace(')', ' ) ').split()
    tokens = [t.strip("'") for t in tokens if t.strip()]

    def parse_expression(tokens, pos=0):
        if pos >= len(tokens):
            raise ValueError("Unexpected end of expression")

        if tokens[pos] == '(':
            node, next_pos = parse_expression(tokens, pos + 1)
            if next_pos >= len(tokens) or tokens[next_pos] != ')':
                raise ValueError("Missing closing parenthesis")
            pos = next_pos + 1
        else:
            # Parse simple condition
            if pos + 2 >= len(tokens):
                raise ValueError("Invalid condition format")
            field = tokens[pos]
            operator = tokens[pos + 1]
            value = tokens[pos + 2]
            node = Node(
                type_="operand",
                value={"field": field, "operator": operator, "value": value}
            )
            pos = pos + 3

        # Check for AND/OR
        if pos < len(tokens) and tokens[pos] in ['AND', 'OR']:
            operator = tokens[pos]
            right_node, next_pos = parse_expression(tokens, pos + 1)
            return Node(type_="operator", value=operator, left=node, right=right_node), next_pos

        return node, pos

    try:
        node, _ = parse_expression(tokens)
        return node
    except Exception as e:
        raise ValueError(f"Invalid rule syntax: {str(e)}")


def evaluate_node(node: Node, data: Dict[str, Any]) -> bool:
    if node.type == "operator":
        left_result = evaluate_node(node.left, data)
        right_result = evaluate_node(node.right, data)

        if node.value == "AND":
            return left_result and right_result
        elif node.value == "OR":
            return left_result or right_result

    elif node.type == "operand":
        field = node.value["field"]
        operator = node.value["operator"]
        value = node.value["value"]

        if field not in data:
            raise ValueError(f"Field {field} not found in data")

        field_value = data[field]
        compare_value = value

        # Convert string numbers to appropriate type
        if isinstance(field_value, (int, float)):
            try:
                compare_value = float(value)
            except ValueError:
                pass

        if operator == ">":
            return field_value > compare_value
        elif operator == "<":
            return field_value < compare_value
        elif operator == "=":
            return field_value == compare_value
        elif operator == ">=":
            return field_value >= compare_value
        elif operator == "<=":
            return field_value <= compare_value
        elif operator == "!=":
            return field_value != compare_value

    return False


@app.post("/api/rules/create")
async def create_rule_endpoint(request: RuleRequest):
    try:
        ast = parse_rule(request.rule_string)
        return ast.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/rules/evaluate")
async def evaluate_rule_endpoint(request: EvaluationRequest):
    try:
        # Convert rule dict back to Node
        def dict_to_node(d):
            if d is None:
                return None
            return Node(
                type_=d["type"],
                value=d["value"],
                left=dict_to_node(d["left"]) if d.get("left") else None,
                right=dict_to_node(d["right"]) if d.get("right") else None
            )

        rule_node = dict_to_node(request.rule)
        result = evaluate_node(rule_node, request.data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
async def root():
    return FileResponse('static/index.html')