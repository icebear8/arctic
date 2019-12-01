#!/bin/sh


HOMEDIR="$(dirname ${0})"
cd ${HOMEDIR}

if [ "x$JAVA_HOME" != "x" ]; then
    JAVA="$JAVA_HOME/bin/java"
else
    JAVA="java"
fi


# to make sure ffmpeg is found and used if present in start directory 
export PATH=.:${PATH}

# -Xss256k: thread stack size. 256K reduces per-thread memory usage and may prevent "java.lang.OutOfMemoryError: unable to create new native thread" on some systems
# -Djava.awt.headless=true: required for image transcoding to work on headless systems (eg no X-Window libraries)

exec "${JAVA}" -Xss256k -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Dfile.encoding="UTF-8" -jar BubbleUPnPServerLauncher.jar $*