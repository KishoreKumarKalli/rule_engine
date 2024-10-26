def evaluate_rule(rule: Dict[str, Any], data: Dict[str, Any]) -> bool:
    node = dict_to_node(rule)
    return evaluate_node(node, data)


def dict_to_node(rule_dict: Dict[str, Any]) -> Node:
    if not rule_dict:
        return None

    node = Node(
        type_=rule_dict["type"],
        value=rule_dict["value"],
        left=dict_to_node(rule_dict["left"]) if rule_dict.get("left") else None,
        right=dict_to_node(rule_dict["right"]) if rule_dict.get("right") else None
    )
    return node


def evaluate_node(node: Node, data: Dict[str, Any]) -> bool:
    if not node:
        return True

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

        if operator == ">":
            return field_value > value
        elif operator == "<":
            return field_value < value
        elif operator == "=":
            return field_value == value
        elif operator == ">=":
            return field_value >= value
        elif operator == "<=":
            return field_value <= value
        elif operator == "!=":
            return field_value != value

    return False