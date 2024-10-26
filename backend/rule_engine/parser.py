def create_rule(rule_string: str) -> Node:
    # Simple parser for demonstration - you'd want more robust parsing in production
    tokens = tokenize(rule_string)
    return parse_tokens(tokens)


def tokenize(rule_string: str) -> List[str]:
    # Basic tokenization - split on spaces and keep operators
    rule_string = rule_string.replace('(', ' ( ').replace(')', ' ) ')
    return [token for token in rule_string.split() if token.strip()]


def parse_tokens(tokens: List[str]) -> Node:
    if not tokens:
        raise ValueError("Empty rule string")

    stack = []
    operators = {'AND', 'OR'}
    comparisons = {'>', '<', '=', '>=', '<=', '!='}

    for token in tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            # Process until matching parenthesis
            sub_expr = []
            while stack and stack[-1] != '(':
                sub_expr.append(stack.pop())
            if stack:
                stack.pop()  # Remove '('
            if sub_expr:
                # Create node from sub-expression
                node = create_node_from_expression(sub_expr[::-1])
                stack.append(node)
        else:
            stack.append(token)

    return create_node_from_expression(stack)


def create_node_from_expression(expr) -> Node:
    # Simplified node creation - you'd want more robust parsing in production
    if len(expr) == 3:  # Simple comparison
        return Node(
            type_="operand",
            value={
                "field": expr[0],
                "operator": expr[1],
                "value": expr[2].strip("'")
            }
        )
    elif len(expr) == 3:  # Binary operation
        return Node(
            type_="operator",
            value=expr[1],
            left=expr[0] if isinstance(expr[0], Node) else Node("operand", expr[0]),
            right=expr[2] if isinstance(expr[2], Node) else Node("operand", expr[2])
        )
    raise ValueError(f"Invalid expression: {expr}")