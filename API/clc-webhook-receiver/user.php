<?php
// Webhook Receiver for CenturyLink Cloud
// Written by Tommy Hughes - 2/20/2015
//
// name this php file according to function & type.
// applicable types include - server, account, & user
// e.g.
// 		server.php
// 		account.php
// 		user.php
//
// call each type from webhook with applicable action specified...
// applicable actions include - created, deleted, & updated
// e.g.
// https://webhook.reciever.com/server.php?action=created
// https://webhook.reciever.com/server.php?action=updated
// https://webhook.reciever.com/server.php?action=deleted
// https://webhook.reciever.com/account.php?action=created
// https://webhook.reciever.com/account.php?action=updated
// https://webhook.reciever.com/account.php?action=deleted
// https://webhook.reciever.com/user.php?action=created
// https://webhook.reciever.com/user.php?action=updated
// https://webhook.reciever.com/user.php?action=deleted

$logsdir = "/var/log/webhooks/logs";
$enable_csv = "yes";         // anything other than "yes" disables csv output
date_default_timezone_set('America/Los_Angeles');

$type = basename(__FILE__, '.php');
$headers = apache_request_headers();
$request = "$_SERVER[REQUEST_URI]";
$datestamp = date("Y-m-d");
$timestamp = date("H:i:s");
$monthstamp = date("Y-m");
$date_timestamp = date("Y-m-d-His");

$errorfilename = $logsdir."/"."error_".$monthstamp.".log";

if($type != 'server' && $type != 'account' && $type != 'user')
{
  $error = "Wrong type specified";
  $errordetails = "-----------------------------------\n".$date_timestamp."\n".print_r($headers, true).$error."\n".$request."\n";
  file_put_contents($errorfilename, $errordetails, FILE_APPEND | LOCK_EX);
  exit("Wrong type specified");
}

$method = $_SERVER['REQUEST_METHOD'];
if($method != "POST")
{
  $error = "Not a POST request";
  $errordetails = "-----------------------------------\n".$date_timestamp."\n".print_r($headers, true).$error."\n".$request."\n";
  file_put_contents($errorfilename, $errordetails, FILE_APPEND | LOCK_EX);
  exit("Access denied");
}

$action = $_GET['action'];
if($action != 'created' && $action != 'deleted' && $action != 'updated')
{
  $error = "Wrong action specified";
  $errordetails = "-----------------------------------\n".$date_timestamp."\n".print_r($headers, true).$error."\n".$request."\n";
  file_put_contents($errorfilename, $errordetails, FILE_APPEND | LOCK_EX);
  exit("Access denied");
}

$uid = uniqid('', true);
$input = file_get_contents("php://input");

////// Signature Validation //////
$publickey = <<<'EOT'
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnmwsVLJ22Y8lmnk+1fI/
JKkm4bM1GvggI7DN10KIoPDgBbNcePZqcFayDdmVuq/jL9MFBrqFSfVszgdq8OWF
G9lEB5vP29K/N+0kRg5V2NDXddI5AOzx6jDjkNM/jjb45UXeDcPzMMdMOl/ds6uT
p6mbfG3U8dWqM/if7mzjEbbhYkBM3OuacEFk38Tkm49IJ4jHnC0p9qWO2iaxJqRc
08M2cJ+yKcFudCVKX8ANE6g6YKK+5aSabxfHX83Vjr4I0kpqo0cfP4aSW/CPDUZ7
yR4bFiy5Wv2de2V+FOGVBQF+/viSzrtrwQjUOJViuxEnifc06xuDF0QFta9anz4d
LQIDAQAB
-----END PUBLIC KEY-----
EOT;

$publickey = openssl_pkey_get_public($publickey);
$signature = $_SERVER['HTTP_TIER3_RSASHA1'];
$signature = base64_decode($signature);

$ok = openssl_verify($input, $signature, $publickey, sha1WithRSAEncryption);
if($ok != 1)
{
    $error = "Signature Invalid";
//    header('HTTP/1.1 403 Access Denied', true, 403);
    $errordetails = "-----------------------------------\n".$date_timestamp."\n".print_r($headers, true).$error."\n".$request."\n";
    file_put_contents($errorfilename, $errordetails, FILE_APPEND | LOCK_EX);
    exit("Signature Invalid");
}
//////////////////////////////////

$phpArray = json_decode($input, true);

$output1 = array_flatten($phpArray);
$output = remove_int_keys($output1);
// print_r($output, false);
extract($output, EXTR_PREFIX_ALL, "clc");

$thepath = $logsdir."/".$type."/";
$testdir = is_dir($thepath); 
if ($testdir == false) {
    mkdir($thepath, 0754, true);
}

$summaryfilename = $thepath."".$type."_summary_".$monthstamp.".log";
if($type == 'server')
{
  $account_alias = substr($clc_name, 3, 4);
  $summary = '"event_type='.$action.'"'.',"datetime_stamp='.$date_timestamp.'"'.',"accountAlias='.$account_alias.'"'.',"server='.$clc_name.'"'.',"data_center='.$clc_locationId.'"'.',"osType='.$clc_osType.'"'.',"internal_ip='.$clc_internal.'"'.',"public_ip='.$clc_public.'"'.',"createdBy='.$clc_createdBy.'"'.',"modifiedBy='.$clc_modifiedBy.'"'.',"unique_id='.$uid.'"'."\n";
  $csv = 'event_type,accountAlias,server,data_center,osType,internal_ip,public_ip,createdBy,modifiedBy,eventDate,eventTime,uniqueEvent_id'."\n";
  $csvdata = $action.','.$account_alias.','.$clc_name.','.$clc_locationId.','.$clc_osType.','.$clc_internal.','.$clc_public.','.$clc_createdBy.','.$clc_modifiedBy.','.$datestamp.','.$timestamp.','.$uid."\n";
}
if($type == 'account')
{
  $summary = '"event_type='.$action.'"'.',"datetime_stamp='.$date_timestamp.'"'.',"accountAlias='.$clc_accountAlias.'"'.',"businessName='.$clc_businessName.'"'.',"parentAlias='.$clc_parentAlias.'"'.',"primaryDataCenter='.$clc_primaryDataCenter.'"'.',"unique_id='.$uid.'"'."\n";
  $csv = 'event_type,accountAlias,businessName,parentAlias,primaryDataCenter,eventDate,eventTime,uniqueEvent_id'."\n";
  $csvdata = $action.','.$clc_accountAlias.','.$clc_businessName.','.$clc_parentAlias.','.$clc_primaryDataCenter.','.$datestamp.','.$timestamp.','.$uid."\n";
}
if($type == 'user')
{
  $summary = '"event_type='.$action.'"'.',"datetime_stamp='.$date_timestamp.'"'.',"accountAlias='.$clc_accountAlias.'"'.',"userName='.$clc_userName.'"'.',"firstName='.$clc_firstName.'"'.',"lastName='.$clc_lastName.'"'.',"emailAddress='.$clc_emailAddress.'"'.',"status='.$clc_status.'"'.',"unique_id='.$uid.'"'."\n";
  $csv = 'event_type,accountAlias,userName,firstName,lastName,emailAddress,status,eventDate,eventTime,uniqueEvent_id'."\n";
  $csvdata = $action.','.$clc_accountAlias.','.$clc_userName.','.$clc_firstName.','.$clc_lastName.','.$clc_emailAddress.','.$clc_status.','.$datestamp.','.$timestamp.','.$uid."\n";
}
file_put_contents($summaryfilename, $summary, FILE_APPEND | LOCK_EX);

$detailsfilename = $thepath."".$type."_".$action."_".$monthstamp.".log";
$details = "-----------------------------------\n".$date_timestamp."\n".$uid."\n".print_r($headers, true).$input."\n";
file_put_contents($detailsfilename, $details, FILE_APPEND | LOCK_EX);

if($enable_csv == 'yes')
{
  $csvfilename = $thepath."".$type."_events_".$monthstamp.".csv";
  $testfile = file_exists($csvfilename); 
  if ($testfile == false) {
    file_put_contents($csvfilename, $csv);
  }
  file_put_contents($csvfilename, $csvdata, FILE_APPEND | LOCK_EX);
}

function array_flatten($phpArray, $preserve_keys = 1, &$newArray = Array()) {
  foreach ($phpArray as $key => $child) {
    if (is_array($child)) {
      $newArray =& array_flatten($child, $preserve_keys, $newArray);
    } elseif ($preserve_keys + is_string($key) > 1) {
      $newArray[$key] = $child;
    } else {
      $newArray[] = $child;
    }
  }
  return $newArray;
}

function remove_int_keys($arr) {
	foreach($arr as $key => $value){
    if(is_numeric($key)) unset($arr[$key]);
	}
	return $arr;
}

?>