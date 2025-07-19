# Security Fix for web3/param/gateway.php

**Vulnerability Type:** AUTHENTICATION_BYPASS  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Added session-based authentication and switched to PDO with prepared statements. Inputs are validated against allowlists.

## Security Notes
Using PDO parameter binding prevents SQL injection. Always authenticate before modifying balances. Validate all inputs.

## Fixed Code
```php
<?php
session_start();
// Use PDO for parameterized queries
$dsn = 'mysql:host=localhost;dbname=bank';
$user = 'dbuser';
$pass = 'dbpass';
$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
];
$pdo = new PDO($dsn, $user, $pass, $options);

// Check authentication
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Authentication required']);
    exit;
}

// Parse and validate input
$input = json_decode(file_get_contents('php://input'), true);
$account = $input['account'] ?? null;
$amount = $input['amount'] ?? null;
if (!preg_match('/^[A-Za-z0-9]+$/', $account) || !is_numeric($amount) || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid input']);
    exit;
}

// Perform update with parameter binding
$stmt = $pdo->prepare('UPDATE accounts SET balance = balance + :amt WHERE account_id = :acc');
$stmt->execute([':amt' => $amount, ':acc' => $account]);

echo json_encode(['status' => 'success']);
?>
```

## Additional Dependencies
None

## Testing Recommendations
- POST without session (401)
- Invalid account IDs and amounts (400)
- Verify balances update correctly
- Attempt SQL injection in input

## Alternative Solutions
None provided
