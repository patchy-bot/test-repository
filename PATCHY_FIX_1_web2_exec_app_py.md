# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
Removed the use of direct exec() with arbitrary user input which allows remote code execution. Instead, this fix parses the user-submitted code using Python's 'ast' module to analyze its abstract syntax tree (AST). It implements a whitelist to allow only certain safe node types, rejecting potentially dangerous constructs. Also, execution is done in a restricted environment where only limited builtins are available, significantly reducing attack surface.

## Security Notes
Always validate or restrict user-submitted code. Using AST parsing is a safer way to analyze code before execution. Consider sandboxing with dedicated tools or environments for executing user code in more complex scenarios. Avoid exec or eval with user input whenever possible.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/run_code', methods=['POST'])
def run_code():
    user_code = request.form.get('code', '')
    try:
        # Parse the user code into an AST to validate syntax and limit harmful constructs
        parsed_code = ast.parse(user_code, mode='exec')
        # Define a whitelist of allowed AST node types
        allowed_nodes = (ast.Module, ast.Expr, ast.BinOp, ast.UnaryOp, ast.Num, ast.Str, ast.NameConstant, ast.Name, ast.Load, ast.Call, ast.Attribute, ast.List, ast.Tuple, ast.Dict, ast.Compare, ast.BoolOp)

        for node in ast.walk(parsed_code):
            if not isinstance(node, allowed_nodes):
                return jsonify({'error': 'Unsafe code detected.'}), 400

        # Use a restricted globals and locals dict to limit execution environment
        safe_globals = {'__builtins__': {'print': print, 'range': range, 'len': len}}
        safe_locals = {}

        exec(compile(parsed_code, filename='<user_code>', mode='exec'), safe_globals, safe_locals)
        return jsonify({'result': 'Code executed successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Error executing code: {str(e)}'}), 400

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- import ast

## Testing Recommendations
- Test that only safe code executes successfully.
- Test that unsafe code returns error and does not execute.
- Test edge cases for allowed AST node types.

## Alternative Solutions

### Use a secure sandbox environment like Docker or an external service to execute user code safely.
**Pros:** Strong isolation, prevents access to host environment.
**Cons:** More complex to implement, requires infrastructure changes.

### Use a domain-specific language or a restricted subset of expressions that can be safely evaluated using libraries like 'asteval'.
**Pros:** Easier to sandbox, less risk of malicious code.
**Cons:** Limits functionality, may not support all desired features.

