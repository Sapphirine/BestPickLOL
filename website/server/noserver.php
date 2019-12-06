<?php

function typeChangeFloat($str) {
    return (float)$str;
}

function typeChangeInt($str) {
    return (int)$str;
}

function recommend1() {
    global $pick0, $pick1, $skip, $Wco, $Wop, $Mco, $Mop;
    $S = [];
    $ids = range(1,555);
    for($i = 0; $i < 555; $i++)
        if(in_array($i + 1, $skip)) {
            $S[$i] = 0;
            continue;
        } else {
            $Sco = 0;
            $Sop = 0;
            foreach($pick0 as $id)
                $Sco += $Mco[$i][$id-1];
            foreach($pick1 as $id)
                $Sop += $Mop[$i][$id-1];
            $S[$i] = $Sco*$Wco + $Sop*$Wop;
        }
    array_multisort($S,SORT_DESC,$ids);
    $top10["s"] = array_slice($S, 0, 10);
    $top10["k"] = array_slice($ids, 0, 10);
    $top10["s"] = implode(',', $top10["s"]);
    $top10["k"] = implode(',', $top10["k"]);
    return $top10;
}

function recommend2() {
    global $pick0, $pick1, $skip, $Wco, $Wop, $Mco, $Mop;
    $S = [];
    $ids1 = [];
    $ids2 = [];
    $counter = 0;
    for($i = 0; $i < 555; $i++)
        if(in_array($i + 1, $skip))
            continue;
        else
            for($j = $i + 1; $j < 555; $j++)
                if(in_array($j + 1, $skip))
                    continue;
                else {
                    $ids1[$counter] = $i + 1;
                    $ids2[$counter] = $j + 1;
                    $S[$counter] = 0;
                    $Sco = 0;
                    $Sop = 0;
                    foreach($pick0 as $id)
                        $Sco += $Mco[$i][$id-1] + $Mco[$j][$id-1];
                    foreach($pick1 as $id)
                        $Sop += $Mop[$i][$id-1] + $Mop[$j][$id-1];
                    $S[$counter] = $Sco*$Wco + $Sop*$Wop;
                    $counter++;
                }
    array_multisort($S,SORT_DESC,$ids1,$ids2);
    $top10_1 = implode(',', array_slice($ids1, 0, 10));
    $top10_2 = implode(',', array_slice($ids2, 0, 10));
    $top10 = [$top10_1, $top10_2];
    return $top10;
}

// Gets, Posts, Argvs

$bans   = $_GET["bans"]  ?? $_POST["bans"]  ?? $argv[1];
$pick0  = $_GET["pick0"] ?? $_POST["pick0"] ?? $argv[2];
$pick1  = $_GET["pick1"] ?? $_POST["pick1"] ?? $argv[3];
$number = $_GET["need"]  ?? $_POST["need"]  ?? $argv[4];

// Process

$bans   = array_unique(explode(",", $bans));
$pick0  = array_unique(explode(",", $pick0));
$pick1  = array_unique(explode(",", $pick1));

$bans   = array_map("typeChangeInt", $bans);
$pick0  = array_map("typeChangeInt", $pick0);
$pick1  = array_map("typeChangeInt", $pick1);
$number = (int)$number;

$bans   = array_diff($bans,  [0]);
$pick0  = array_diff($pick0, [0]);
$pick1  = array_diff($pick1, [0]);

$notAllowed = [0, -1];
$skip   = array_merge($notAllowed, $bans, $pick0, $pick1);
$skip   = array_unique($skip);

// File read

$Fco = fopen("Mco.csv", 'r');
$Mco = [];
while (($line = fgets($Fco)) !== false) {
    $line = explode(",",$line);
    $line = array_map("typeChangeFloat", $line);
    $Mco[] = $line;
}
if (!feof($Fco)) {
    echo "Error: unexpected fgets() fail\n";
}
fclose($Fco);

$Fop = fopen("Mop.csv", 'r');
$Mop = [];
while (($line = fgets($Fop)) !== false) {
    $line = explode(",",$line);
    $line = array_map("typeChangeFloat", $line);
    $Mop[] = $line;
}
if (!feof($Fop)) {
    echo "Error: unexpected fgets() fail\n";
}
fclose($Fop);

// Parameters

$Wco = 7;
$Wop = 5;

// Calculate

if($number == 1) {
    $rcmd = recommend1();
    $json = array("recommend"=>$rcmd["k"], "score"=>$rcmd["s"]);
} else {
    $rcmds = recommend2();
    $json = array("recommend1"=>$rcmds[0], "recommend2"=>$rcmds[1]);
}
$json["bans"] = $bans;
$json["pick0"] = $pick0;
$json["pick1"] = $pick1;
$json["skip"] = $skip;
echo json_encode($json);

return 0;
