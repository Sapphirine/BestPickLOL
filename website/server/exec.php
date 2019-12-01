<?php
$b = $_GET["bans"] ?? $argv[1];
$p0 = $_GET["pick0"] ?? $argv[2];
$p1 = $_GET["pick1"] ?? $argv[3];
$n = $_GET["need"] ?? $argv[4];

$cmd = "python C:/inetpub/wwwroot/lab/bestbp/server/local.py $b $p0 $p1 $n";
$line = exec($cmd, $output, $return_val);
if ($n == 1) {
    $json = array("recommend"=>$output, "return"=>$return_val, "cmd"=>$cmd);
} else {
    $json = array("recommend1"=>$output, "recommend2"=>$array, "return"=>$return_val, "cmd"=>$cmd);
}
echo json_encode($json);
