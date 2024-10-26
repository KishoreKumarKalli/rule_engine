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