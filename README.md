Rule Engine with AST

This project implements a Rule Engine that uses Abstract Syntax Trees (AST) to evaluate complex rules and conditions based on user-defined attributes. This engine allows for dynamic rule creation, combination, modification, and evaluation for various use cases, such as determining user eligibility based on attributes like age, department, income, and experience.

Features

•	Dynamic Rule Creation: Define rules using strings with logical operators (AND, OR) and conditions.

•	Rule Combination: Combine multiple rules into a single AST structure.

•	Flexible Evaluation: Evaluate rules against input data to determine if conditions are met.

•	Error Handling: Manage invalid rule strings or data formats.

•	Rule Modification: Modify existing rules by changing operators, operand values, or adding/removing sub-expressions.


Example Rules

sample rules include conditions for determining eligibility based on age, department, salary, and experience:

rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"

rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

Data Structure

The rule engine uses a custom Node class to represent the AST, structured as follows:

•	type: Indicates the node type (operator or operand).

•	left: Reference to the left child node.

•	right: Reference to the right child node.

•	value: Holds the value for operand nodes (e.g., age > 30).

Node Structure Example

class Node:

    def __init__(self, node_type, left=None, right=None, value=None):
    
        self.type = node_type
        
        self.left = left
        
        self.right = right
        
        self.value = value
        
API Functions

1. create_rule(rule_string)
    
Parses a rule string into an AST structure.

rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"

ast_rule1 = create_rule(rule1)

3. combine_rules(rules)
   
Combines multiple rules into a single AST structure for efficient evaluation.

rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

combined_ast = combine_rules([rule1, rule2])

4. evaluate_rule(ast, data)

Evaluates the rule represented by the AST against a data dictionary of user attributes.

data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}

result = evaluate_rule(combined_ast, data)

print(result)  # Output: True or False

Installation

Clone the repository:

git clone https://github.com/your-username/rule-engine-ast.git

cd rule-engine-ast

Install dependencies:

pip install -r requirements.txt

Testing

Run tests to verify rule creation, combination, and evaluation functionalities.

pytest tests/

Error Handling

The system includes basic error handling for invalid rule strings, missing operators, or incompatible data types. Custom exceptions and validations ensure that rule conditions align with the attributes present in the user data.

Future Enhancements

Catalog Validation: Ensure attributes in rule conditions are valid according to a predefined catalog.
User-Defined Functions: Extend support for advanced conditions and calculations in rules.
Rule Modification API: Add an API to modify existing rules by adding or removing conditions.
