<?php
ignore_user_abort(true);
set_time_limit(0);

$script       = '${UTILS_DIR}/updateContent.sh';
$dstLog       = '/var/log/updateContent.log';

shell_exec('sh '.$script.' >> '.$dstLog.' 2>&1');
