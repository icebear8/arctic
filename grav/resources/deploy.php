<?php
ignore_user_abort(true);
set_time_limit(0);

$updateScript     = 'cd /opt/repo &&/opt/utils/git/repoUpdate.sh';
$clearCacheScript = '/opt/utils/grav/clearGravCache.sh';
$logDestination   = '/var/log/updateContent.log';

shell_exec('sh '.$updateScript.' >> '.$logDestination.' 2>&1');
shell_exec('sh '.$clearCacheScript.' >> '.$logDestination.' 2>&1');

header("Location: {$_SERVER['HTTP_REFERER']}");

?>