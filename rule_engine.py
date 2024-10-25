import ast
import sqlite3

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # "operator" or "operand"
        self.value = value  # For operand nodes
        self.left = left  # Left child for operators
        self.right = right  # Right child for operators

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, left={self.left}, right={self.right})"

def init_db():
    conn = sqlite3.connect('rulesdb.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_text TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            result BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

def save_rule(rule_text):
    conn = sqlite3.connect('rulesdb.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rules (rule_text) VALUES (?)', (rule_text,))
    conn.commit()
    conn.close()

def save_evaluation_result(data, result):
    conn = sqlite3.connect('rulesdb.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO evaluation_results (data, result) VALUES (?, ?)', (str(data), result))
    conn.commit()
    conn.close()

def create_rule(rule_string):
    tree = ast.parse(rule_string, mode='eval')
    return ast_to_node(tree.body)

def ast_to_node(tree):
    if isinstance(tree, ast.BoolOp):
        op = 'AND' if isinstance(tree.op, ast.And) else 'OR'
        left = ast_to_node(tree.values[0])
        right = ast_to_node(tree.values[1])
        return Node(node_type='operator', value=op, left=left, right=right)
    elif isinstance(tree, ast.Compare):
        left = ast_to_node(tree.left)
        right = ast_to_node(tree.comparators[0])
        op = tree.ops[0]
        op_str = {
            ast.Gt: '>',
            ast.Lt: '<',
            ast.Eq: '=',
            ast.GtE: '>=',
            ast.LtE: '<=',
            ast.NotEq: '!='
        }[type(op)]
        return Node(node_type='operator', value=op_str, left=left, right=right)
    elif isinstance(tree, ast.Name):
        return Node(node_type='operand', value=tree.id)
    elif isinstance(tree, ast.Constant):
        return Node(node_type='operand', value=tree.value)
    elif isinstance(tree, ast.Str):  # For older versions of ast (Python 3.7 and below)
        return Node(node_type='operand', value=tree.s)
    elif isinstance(tree, ast.Num):  # For older versions of ast (Python 3.7 and below)
        return Node(node_type='operand', value=tree.n)
    else:
        raise ValueError(f"Unsupported AST node type: {type(tree)}")

def combine_rules(rules):
    nodes = [create_rule(rule) for rule in rules]
    while len(nodes) > 1:
        left = nodes.pop(0)
        right = nodes.pop(0)
        combined = Node(node_type='operator', value='AND', left=left, right=right)
        nodes.append(combined)
    return nodes[0]

def evaluate_rule(node, data):
    if node.type == 'operand':
        return data.get(node.value, node.value)
    elif node.type == 'operator':
        left_val = evaluate_rule(node.left, data)
        right_val = evaluate_rule(node.right, data)
        if node.value == 'AND':
            return left_val and right_val
        elif node.value == 'OR':
            return left_val or right_val
        elif node.value == '>':
            return left_val > right_val
        elif node.value == '<':
            return left_val < right_val
        elif node.value == '=':
            return left_val == right_val
        elif node.value == '>=':
            return left_val >= right_val
        elif node.value == '<=':
            return left_val <= right_val
        elif node.value == '!=':
            return left_val != right_val