#!/bin/sh
set -x

VER=$(fedpkg verrel | sed -e 's/^scala\-\(.*\)\-.*$/\1/')

FNS=scala-$VER

rm -rf $FNS/
git clone git://github.com/scala/scala.git $FNS
cd $FNS
git checkout v$VER
git show v$VER >../gitdate.txt
cd ..
tar -zcf $FNS.tgz --exclude $FNS/.git $FNS/
cd $FNS
./pull-binary-libs.sh
rm -rf lib/jline.jar
tar -zcf ../$FNS-bootstrap.tgz --exclude .git lib/*.jar
cd ..
rm -rf $FNS/
fedpkg new-sources $FNS.tgz $FNS-bootstrap.tgz
