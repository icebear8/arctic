<?php
ignore_user_abort(true);
set_time_limit(0);

$updateScript     = '/var/www/utils/updateContent.sh';
$clearCacheScript = '/var/www/utils/clearGravCache.sh';
$logDestination   = '/var/log/updateContent.log';

shell_exec('sh '.$updateScript.' >> '.$logDestination.' 2>&1');
shell_exec('sh '.$clearCacheScript.' >> '.$logDestination.' 2>&1');

header ("Location: http://intranet.arctic:8080");

?>