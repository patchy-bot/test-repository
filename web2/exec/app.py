from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

# Define a safe subset of operations via AST parsing
SAFE_NODES = {
    'Expression', 'BinOp', 'Add', 'Sub', 'Mult', 'Div', 'Pow',
    'Num', 'Load', 'UnaryOp', 'UAdd', 'USub', 'Name'
}

class SafeEvaluator(ast.NodeVisitor):
    def generic_visit(self, node):
        node_type = type(node).__name__
        if node_type not in SAFE_NODES:
            raise ValueError(f"Unsafe expression: {node_type}")
        super().generic_visit(node)

    def visit_Name(self, node):
        if node.id not in ('x', 'y', 'z'):
            raise ValueError(f"Unknown variable: {node.id}")
        super().generic_visit(node)

@app.route('/eval', methods=['POST'])
def evaluate():
    data = request.get_json() or {}
    expr = data.get('expr', '')
    try:
        # Parse expression into AST
        parsed = ast.parse(expr, mode='eval')
        # Validate AST nodes
        SafeEvaluator().visit(parsed)
        # Compile and evaluate in restricted namespace
        code = compile(parsed, '<string>', 'eval')
        result = eval(code, {'__builtins__': {}}, {'x':1,'y':2,'z':3})
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()