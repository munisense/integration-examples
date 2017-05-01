<?php
/**
 * Example script to query the a sensor value from a node using the Net2GRID ZGD API.
 * Change addr, cluster and attributes depending on which values you want to read.
 *
 * Read more: http://developer.net2grid.com/documentation/api/embedded/#!/zgd.json/ZclReadAttributes
 */
$curl = curl_init();

curl_setopt_array($curl, [
    CURLOPT_URL => "<IP>/zgd/zcl/read",
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_ENCODING => "",
    CURLOPT_MAXREDIRS => 10,
    CURLOPT_TIMEOUT => 30,
    CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
    CURLOPT_CUSTOMREQUEST => "POST",
    CURLOPT_POSTFIELDS => '{
    "addr": {"eui": ["0x00", "0x0d", "0x6f", "0x00", "0x12", "0x34", "0x56", "0xf78"]},
    "endpoint": "0x0a",
    "profile": "0xf100",
    "cluster": "0x9400",
    "attributes": ["0x0000"]}', // LAeq attribute id = 0x0000
    CURLOPT_HTTPHEADER => [
        "cache-control: no-cache",
        "content-type: application/json",
    ],
]);

$response = json_decode(curl_exec($curl), true);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
    echo "cURL Error #:" . $err;
} else {
    $output = $response["attributes"][0]["value"];
    $value = hexdec(dechex($output[1]) . dechex($output[0]));
    echo "Value: " . $value / 100 . " dBA" . PHP_EOL;
}
