import pytest
from fastapi.testclient import TestClient
from app import app, create_rule, evaluate_node, Node

client = TestClient(app)


# Unit Tests
def test_create_simple_rule():
    rule_string = "age > 30"
    node = create_rule(rule_string)
    assert node.type == "operand"
    assert node.value["field"] == "age"
    assert node.value["operator"] == ">"
    assert node.value["value"] == "30"


def test_create_compound_rule():
    rule_string = "age > 30 AND department = 'Sales'"
    node = create_rule(rule_string)
    assert node.type == "operator"
    assert node.value == "AND"
    assert node.left.type == "operand"
    assert node.right.type == "operand"


def test_evaluate_simple_rule():
    node = Node(
        type_="operand",
        value={"field": "age", "operator": ">", "value": "30"}
    )
    data = {"age": 35}
    assert evaluate_node(node, data) == True
    data = {"age": 25}
    assert evaluate_node(node, data) == False


def test_evaluate_compound_rule():
    node = Node(
        type_="operator",
        value="AND",
        left=Node(
            type_="operand",
            value={"field": "age", "operator": ">", "value": "30"}
        ),
        right=Node(
            type_="operand",
            value={"field": "department", "operator": "=", "value": "Sales"}
        )
    )
    data = {"age": 35, "department": "Sales"}
    assert evaluate_node(node, data) == True
    data = {"age": 25, "department": "Sales"}
    assert evaluate_node(node, data) == False


# Integration Tests
def test_create_rule_endpoint():
    response = client.post(
        "/api/rules/create",
        json={"rule_string": "age > 30 AND department = 'Sales'"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "operator"
    assert data["value"] == "AND"


def test_evaluate_rule_endpoint():
    rule = {
        "type": "operator",
        "value": "AND",
        "left": {
            "type": "operand",
            "value": {"field": "age", "operator": ">", "value": "30"}
        },
        "right": {
            "type": "operand",
            "value": {"field": "department", "operator": "=", "value": "Sales"}
        }
    }
    data = {"age": 35, "department": "Sales"}

    response = client.post(
        "/api/rules/evaluate",
        json={"rule": rule, "data": data}
    )
    assert response.status_code == 200
    assert response.json()["result"] == True


# Error Cases
def test_invalid_rule_syntax():
    with pytest.raises(ValueError):
        create_rule("age > > 30")


def test_missing_field():
    node = Node(
        type_="operand",
        value={"field": "age", "operator": ">", "value": "30"}
    )
    with pytest.raises(ValueError):
        evaluate_node(node, {"department": "Sales"})


def test_invalid_operator():
    with pytest.raises(ValueError):
        create_rule("age INVALID 30")


# Performance Tests
def test_large_compound_rule():
    # Create a large rule with multiple conditions
    rule_parts = ["age > 30"] * 100
    rule_string = " AND ".join(rule_parts)
    node = create_rule(rule_string)
    assert node is not None


# Security Tests
def test_sql_injection_attempt():
    response = client.post(
        "/api/rules/create",
        json={"rule_string": "age > 30; DROP TABLE users;"}
    )
    assert response.status_code == 400


def test_xss_attempt():
    response = client.post(
        "/api/rules/create",
        json={"rule_string": "age > 30 AND department = '<script>alert(1)</script>'"}
    )
    assert response.status_code == 200
    assert "<script>" not in response.text