<?php
$url = "http://aires.astoria-tula.ru/sharedapi/org_events/list";


$data = json_decode(file_get_contents('php://input'), true);
$apikey = "21d1c8300ca07c06bf8f3aac3c16c275";  // Первый параметр
$deal_id = 1125;    // Второй параметр
$time = "1732745214";    // Второй параметр
$params = array(
          	'filters' => array(
          		'employee' => $deal_id,
//           		'dtstart' => $time,
//           		'dtend' => $time,
//           		'summary' => "Позвонить: +79952605482 Никита : сделка ID: 106143",
          	),
          );

$post = array(
    'apikey' => "$apikey",
    'params' => $params
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($post));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$response = curl_exec($ch);
curl_close($ch);
$result = json_decode($response, true);
echo json_encode($result, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
?>