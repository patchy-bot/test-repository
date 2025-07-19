<?php
session_start();
// Ensure user is authenticated
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

// Fetch and validate POST inputs
function validate_account($acct) {
    return preg_match('/^[0-9]{6,12}$/', $acct);
}
function validate_amount($amt) {
    return is_numeric($amt) && $amt > 0;
}

$from = $_POST['from_account'] ?? '';
$to   = $_POST['to_account']   ?? '';
$amt  = $_POST['amount']       ?? '';

if (!validate_account($from) || !validate_account($to) || !validate_amount($amt)) {
    http_response_code(400);
    echo json_encode(['error'=>'Invalid input']);
    exit;
}

// Perform safe update using prepared statements
try {
    $db = new PDO('mysql:host=localhost;dbname=bank', 'user', 'pass');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $stmt = $db->prepare(
        'UPDATE accounts
         SET balance = CASE WHEN account_id = :from THEN balance - :amt
                            WHEN account_id = :to THEN balance + :amt END
         WHERE account_id IN (:from, :to)'
    );
    $stmt->execute([':from'=>$from, ':to'=>$to, ':amt'=>$amt]);
    echo json_encode(['status'=>'success']);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error'=>$e->getMessage()]);
}
?>