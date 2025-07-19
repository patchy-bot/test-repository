# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed exec() entirely and replaced it with AST-based parsing. We only allow specific node types (numbers and arithmetic operators) and evaluate in a restricted builtins-less environment. Any other node causes a rejection.

## Security Notes
Using ast.parse with a whitelist of safe nodes prevents arbitrary code execution. eval() is called with an empty __builtins__ to block access to dangerous functions.

## Fixed Code
```py
from flask import Flask, request, jsonify, abort
import ast

app = Flask(__name__)

@app.route('/evaluate', methods=['POST'])
def evaluate_expression():
    user_input = request.json.get('expression')
    if not isinstance(user_input, str):
        abort(400, 'Invalid input type')
    # Allow only arithmetic expressions by parsing AST
    try:
        expr_ast = ast.parse(user_input, mode='eval')
        # Walk the AST and ensure only safe nodes
        for node in ast.walk(expr_ast):
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                     ast.Num, ast.Add, ast.Sub, ast.Mult,
                                     ast.Div, ast.Pow, ast.Mod, ast.UAdd, ast.USub,
                                     ast.Load, ast.Constant)):
                abort(400, 'Disallowed expression')
        result = eval(compile(expr_ast, '<string>', 'eval'), {'__builtins__': {}})
    except Exception as e:
        abort(400, f'Error evaluating expression: {e}')
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False)
```

## Additional Dependencies
- import ast

## Testing Recommendations
- Submit valid arithmetic expressions
- Submit disallowed code snippets and confirm 400 responses
- Fuzz random inputs to ensure no code injection
- Test boundary cases (large numbers, decimals)

## Alternative Solutions

### Use a dedicated math expression library like 'asteval' or 'numexpr'
**Pros:** Well-tested, Handles complex math
**Cons:** Additional dependency

