%global fullversion %{version}
%global release_repository http://nexus.scala-tools.org/content/repositories/releases
%global snapshot_repository http://nexus.scala-tools.org/content/repositories/snapshots
%if 0%{?fedora} > 19
%global jansi_jar %{_javadir}/jansi/jansi.jar
%else
%global jansi_jar %{_javadir}/jansi.jar
%endif
%if 0%{?fedora} > 20
%global jline2_jar %{_javadir}/jline/jline.jar
%else
%global jline2_jar %{_javadir}/jline2.jar
%endif
%global scaladir %{_datadir}/scala
%global bootstrap_build 1
%if 0%{?fedora} > 19
%global apidoc %{_docdir}/%{name}-apidoc
%else
%global apidoc %{_docdir}/%{name}-apidoc-%{version}
%endif

%global junit_pkg junit


Name:           scala
Version:        2.10.4
Release:        1%{?dist}
Summary:        A hybrid functional/object-oriented language for the JVM
BuildArch:      noarch
Group:          Development/Languages
# License was confirmed to be standard BSD by fedora-legal
# https://www.redhat.com/archives/fedora-legal-list/2007-December/msg00012.html
License:        BSD
URL:            http://www.scala-lang.org/

Source0:        https://github.com/scala/scala/archive/v%{version}.tar.gz
Source1:        scala-library-2.10.0-bnd.properties.in
# Bootstrap file generated by ./get-sources.sh
Source2:        scala-2.10.3-bootstrap.tgz
# git information generated by ./get-sources.sh
Source3:        scala.gitinfo

# we need this binary copy of the scala 2.10.4 compiler
# for bootstrapping under Java 8; this can be removed if
# necessary after Scala 2.10.5 is released if it uses 2.10.4
# for bootstrapping.

# unfortunately, this has the same name as the source archive,
# so we can't use a URL here.  Get this file by running 
#   curl http://www.scala-lang.org/files/archive/scala-2.10.4.tgz \
#       > scala-bin-2.10.4.tgz

Source4:        http://www.scala-lang.org/files/archive/scala-2.10.4.tgz

# Source0:        http://www.scala-lang.org/downloads/distrib/files/scala-sources-%{fullversion}.tgz
# Change the default classpath (SCALA_HOME)
Patch1:         scala-2.10.0-tooltemplate.patch
# Use system jline2 instead of bundled jline2
Patch2:         scala-2.10.3-use_system_jline.patch
# change org.scala-lang jline in org.sonatype.jline jline
Patch3:         scala-2.10.3-compiler-pom.patch
# Patch Swing module for JDK 1.7
Patch4:         scala-2.10.2-java7.patch
# fix incompatibilities with JLine 2.7
Patch6:         scala-2.10-jline.patch
# work around a known bug when running binary-compatibility tests against
# non-optimized builds (we can't do optimized builds due to another bug):
# http://grokbase.com/t/gg/scala-internals/1347g1jahq/2-10-x-bc-test-fails
# Patch7:         scala-2.10.1-bc.patch
Patch8:         scala-2.10.4-build_xml.patch

Source21:       scala.keys
Source22:       scala.mime
Source23:       scala-mime-info.xml
Source24:       scala.ant.d

Source31:       scala-bootstript.xml

BuildRequires:  java-devel >= 1:1.7.0
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  ant-contrib
%if 0%{?fedora} > 20
BuildRequires:  jline >= 2.10
%else
BuildRequires:  jline2
%endif
BuildRequires:  javapackages-tools
BuildRequires:  shtool
BuildRequires:  aqute-bnd
BuildRequires:  %{junit_pkg}
BuildRequires:  felix-framework
BuildRequires:  jpackage-utils

%if !(0%{?bootstrap_build})
BuildRequires:  scala
%endif

Requires:       jpackage-utils
Requires:       jansi

%if 0%{?fedora} > 20
Requires:       java-headless >= 1:1.7.0
Requires:       jline >= 2.10
%global want_jdk8 1
%else
Requires:       java >= 1:1.7.0
Requires:       jline2
%global want_jdk8 0
%endif

Requires:       %{jansi_jar}
Requires:       %{jline2_jar}

%{?filter_setup:
%filter_from_requires /ant/d;
%filter_setup
}

%description
Scala is a general purpose programming language designed to express common
programming patterns in a concise, elegant, and type-safe way. It smoothly
integrates features of object-oriented and functional languages. It is also
fully interoperable with Java.

%package apidoc
Summary:        Documentation for the Scala programming language
Group:          Documentation

%description apidoc
Scala is a general purpose programming language for the JVM that blends
object-oriented and functional programming. This package provides
reference and API documentation for the Scala programming language.

%package swing
Summary:        The swing library for the scala programming languages
Group:          Development/Libraries
Requires:       scala = %{version}-%{release}

%if 0%{?fedora} > 20
Requires:       java >= 1:1.7.0
%endif

%description swing
This package ontains the swing library for the scala programming lauguages. This library is
required to develope GUI-releate applications in scala. The release provided by this package
is not the original version from upstream because this version is not compatible with JDK-1.7.

%package -n ant-scala
Summary:        Development files for Scala
Group:          Development/Languages
Requires:       scala = %{version}-%{release}, ant

%description -n ant-scala
Scala is a general purpose programming language for the JVM that blends
object-oriented and functional programming. This package enables support for
the scala ant tasks.

%if 0
%package examples
Summary:        Examples for the Scala programming language
Group:          Development/Languages
# Otherwise it will pick up some perl module
Autoprov:       0
Requires:       scala = %{version}-%{release}
Requires:       ant

%description examples
Scala is a general purpose programming language for the JVM that blends
object-oriented and functional programming. This package contains examples for
the Scala programming language

%package swing-examples
Summary:        Examples for the Scala Swing library
Group:          Development/Libraries
Requires:       scala = %{version}-%{release}
Requires:       ant

%description swing-examples
This package contains examples for the Swing library of the Scala language which is required
to create GUI applications in the Scala programming language. 
%endif

%prep

%global _default_patch_fuzz 2

%setup -q 
%patch1 -p1 -b .tool
%patch2 -p1 -b .sysjline
%patch3 -p1 -b .compiler-pom
%patch4 -p1 -b .jdk7
%patch6 -p1 -b .rvk
# %patch7 -p1 -b .bc
%patch8 -p1 -b .bld

echo "starr.version=2.10.4\nstarr.use.released=0" > starr.number

pushd src
rm -rf jline
popd

sed -i '/is not supported by/d' build.xml
sed -i '/exec.*pull-binary-libs.sh/d' build.xml

%if 0%{?bootstrap_build}
%global do_bootstrap -DdoBootstrapBuild=yes
tar -xzvf %{SOURCE2}
%if %{want_jdk8}
tar -xzvf %{SOURCE4} --strip-components=1 scala-2.10.4/lib
%endif
%else
%global do_bootstrap %{nil}
%endif

pushd lib
#  fjbg.jar ch.epfl.lamp
#  forkjoin.jar scala.concurrent.forkjoin available @ https://bugzilla.redhat.com/show_bug.cgi?id=854234 as jsr166y
#  find -not \( -name 'scala-compiler.jar' -or -name 'scala-library.jar' -or -name 'midpapi10.jar' -or \
#       -name 'msil.jar' -or -name 'fjbg.jar' -or -name 'forkjoin.jar' \) -and -name '*.jar' -delete


#  midpapi10.jar https://bugzilla.redhat.com/show_bug.cgi?id=807242 ?
#  msil.jar ch.epfl.lamp.compiler
#  scala-compiler.jar
#  scala-library-src.jar
#  scala-library.jar
%if !(0%{?bootstrap_build})
    rm -rf scala-compiler.jar
    ln -s $(build-classpath scala/scala-compiler.jar) scala-compiler.jar
    rm -rf scala-library.jar
    ln -s $(build-classpath scala/scala-library.jar) scala-library.jar
    rm -rf scala-reflect.jar
    ln -s $(build-classpath scala/scala-reflect.jar) scala-reflect.jar
%endif
  pushd ant
    rm -rf ant.jar
    rm -rf ant-contrib.jar
    ln -s $(build-classpath ant.jar) ant.jar
    ln -s $(build-classpath ant/ant-contrib) ant-contrib.jar
#    rm -rf ant-dotnet-1.0.jar
#    rm -rf maven-ant-tasks-2.1.1.jar
#    rm -rf vizant.jar
  popd
popd

cp -rf %{SOURCE31} .


sed -i -e 's!@JLINE@!%{jline2_jar}!g' build.xml

echo echo $(head -n 1 %{SOURCE3}) > tools/get-scala-commit-sha
echo echo $(tail -n 1 %{SOURCE3}) > tools/get-scala-commit-date
chmod 755 tools/get-scala-*

%build

export ANT_OPTS="-Xms2048m -Xmx2048m %{do_bootstrap}"

# NB:  the "build" task is (unfortunately) necessary
#  build-opt will fail due to a scala optimizer bug
#  and its interaction with the system jline
# ant -f scala-bootstript.xml build
ant build docs || exit 1
pushd build/pack/lib
sed -e 's/@VERSION@/%{version}/g' %{SOURCE1} >bnd.properties
java -jar $(build-classpath aqute-bnd) wrap -properties \
    bnd.properties scala-library.jar
mv scala-library.jar scala-library.jar.no
mv scala-library.bar scala-library.jar
popd

%check

# these tests fail, but their failures appear spurious
rm -f test/files/run/parserJavaIdent.scala
rm -rf test/files/presentation/implicit-member
rm -rf test/files/presentation/t5708
rm -rf test/files/presentation/ide-bug-1000349
rm -rf test/files/presentation/ide-bug-1000475
rm -rf test/files/presentation/callcc-interpreter
rm -rf test/files/presentation/ide-bug-1000531
rm -rf test/files/presentation/visibility
rm -rf test/files/presentation/ping-pong

rm -f test/osgi/src/ReflectionToolboxTest.scala

# fails under mock but not under rpmbuild
rm -f test/files/run/t6223.scala

## Most test dependencies still aren't available in Fedora
# ant test

%install

install -d $RPM_BUILD_ROOT%{_bindir}
for prog in scaladoc fsc scala scalac scalap; do
        install -p -m 755 build/pack/bin/$prog $RPM_BUILD_ROOT%{_bindir}
done

install -p -m 755 -d $RPM_BUILD_ROOT%{_javadir}/scala
install -p -m 755 -d $RPM_BUILD_ROOT%{scaladir}/lib
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

# XXX: add scala-partest when it works again
for libname in scala-compiler \
    scala-library \
    scala-reflect \
    scalap \
    scala-swing ; do
        install -m 644 build/pack/lib/$libname.jar $RPM_BUILD_ROOT%{_javadir}/scala/
        shtool mkln -s $RPM_BUILD_ROOT%{_javadir}/scala/$libname.jar $RPM_BUILD_ROOT%{scaladir}/lib
        sed -i "s|@VERSION@|%{fullversion}|" src/build/maven/$libname-pom.xml
        sed -i "s|@RELEASE_REPOSITORY@|%{release_repository}|" src/build/maven/$libname-pom.xml
        sed -i "s|@SNAPSHOT_REPOSITORY@|%{snapshot_repository}|" src/build/maven/$libname-pom.xml
        install -pm 644 src/build/maven/$libname-pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-$libname.pom
%add_maven_depmap JPP.%{name}-$libname.pom %{name}/$libname.jar
done
shtool mkln -s $RPM_BUILD_ROOT%{jline2_jar} $RPM_BUILD_ROOT%{scaladir}/lib
shtool mkln -s $RPM_BUILD_ROOT%{jansi_jar} $RPM_BUILD_ROOT%{scaladir}/lib

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
install -p -m 644 %{SOURCE24} $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/scala

%if 0
cp -pr docs/examples $RPM_BUILD_ROOT%{_datadir}/scala/
%endif 

install -d $RPM_BUILD_ROOT%{_datadir}/mime-info
install -p -m 644 %{SOURCE21} %{SOURCE22} $RPM_BUILD_ROOT%{_datadir}/mime-info/

install -d $RPM_BUILD_ROOT%{_datadir}/mime/packages/
install -p -m 644 %{SOURCE23} $RPM_BUILD_ROOT%{_datadir}/mime/packages/

sed -i -e 's,@JAVADIR@,%{_javadir},g' -e 's,@DATADIR@,%{_datadir},g' $RPM_BUILD_ROOT%{_bindir}/*

install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m 644 build/scaladoc/manual/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1

%post
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
update-mime-database %{_datadir}/mime &> /dev/null || :

%files -f .mfiles
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/%{name}-compiler.jar
%{_javadir}/%{name}/%{name}-library.jar
%{_javadir}/%{name}/%{name}-reflect.jar
%{_javadir}/%{name}/scalap.jar
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/lib/j*.jar
%{_datadir}/%{name}/lib/%{name}-compiler.jar
%{_datadir}/%{name}/lib/%{name}-library.jar
%{_datadir}/%{name}/lib/%{name}-reflect.jar
%{_datadir}/%{name}/lib/scalap.jar
%{_datadir}/mime-info/*
%{_datadir}/mime/packages/*
%{_mandir}/man1/*
%doc docs/LICENSE

%files swing
%defattr(-,root,root,-)
%{_datadir}/%{name}/lib/%{name}-swing.jar
%{_javadir}/%{name}/%{name}-swing.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-swing.pom
%doc docs/LICENSE

%files -n ant-scala
%defattr(-,root,root,-)
# Following is plain config because the ant task classpath could change from
# release to release
%config %{_sysconfdir}/ant.d/*
%doc docs/LICENSE

%files apidoc
%defattr(-,root,root,-)
%doc build/scaladoc/library/*
%doc docs/LICENSE

%if 0
%files examples
%defattr(-,root,root,-)
%{_datadir}/scala/examples
%exclude %{_datadir}/scala/examples/swing 
%doc docs/LICENSE

%files swing-examples
%defattr(-,root,root,-)
%{_datadir}/scala/examples/swing 
%doc docs/LICENSE
%endif

%changelog
* Mon Sep 15 2014 William Benton <willb@redhat.com> - 2.10.4-1
- updated to upstream version 2.10.4
- fixes for Java 8 compatibility:  use scala 2.10.4 for bootstrapping

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 21 2014 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.3-11
- Implenting usage of headless java (#1068518)
- Fix rpmdeps version sanity check issue

* Mon Dec  9 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.3-10
- Activate compiler-pom patch again

* Sun Dec  8 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.3-9
- Put the swing library into a seperate subpackage

* Wed Nov 27 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.3-8
- Filter osgi(org.apache.ant) Req. (#975598)

* Thu Oct 31 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.3-7
- Fix wrong condition for jline Req.

* Wed Oct 30 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.3-6
- Jline2 is now jline in Rawhide
- Fix an issue with jansi.jar in F-20 (#1025062)

* Tue Oct 22 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.3-5
- Fix typo

* Mon Oct 21 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.3-4
- Fix jline2.jar path for Rawhide (#1021465)
- Add jpackage-utils as a BR

* Tue Oct 15 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.3-3
- Fix change classpath of jansi.jar
- Dynamicly setting of version in bnd.properties
- automatic generation of gitdate and gitsha

* Sun Oct 13 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.3-2
- Fix REPL crash issue when entering an exclaimation mark (#890069)

* Thu Oct 10 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.3-1
- New upstream release

* Thu Sep 26 2013 William Benton <willb@redhat.com> - 2.10.2-1
- upstream version 2.10.2

* Thu Sep 12 2013 William Benton <willb@redhat.com> - 2.10.1-4
- updated upstream source location (thanks to Antoine Gourlay for the observation)

* Wed Sep 11 2013 William Benton <willb@redhat.com> - 2.10.1-3
- Fixes to build and install on F19

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 16 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.1-1
- New upstream releae

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan  7 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.0-1
- New upstream release
- Add patch to use system aQuate-bnd.jar file

* Thu Dec 13 2012 Jochen Schmitt <s4504kr@omega.in.herr-schmitt.de> - 2.10.0-0.5
- New upstream release

* Fri Dec  7 2012 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.0-0.3
- New upstream release

* Thu Sep 13 2012 gil cattaneo <puntogil@libero.it> 2.9.2-1
- update to 2.9.2
- added maven poms
- adapted to current guideline
- built with java 7 support
- removed ant-nodeps from buildrequires
- disabled swing module

* Sat Jul 21 2012 Fedora Release Engineering <JOchen herr-schmitt de> - 2.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 27 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.9.1-2
- Build explicit agains java-1.6.0

* Thu Nov  3 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.9.1-1
- New upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  9 2010 Jochen Schmitt <Jochen herr-schmitt de> - 2.8.1-1
- New upstream release (#661853)

* Sun Aug 15 2010 Geoff Reedy <geoff@programmer-monk.net> - 2.8.0-1
- Update to upstream 2.8.0 release

* Thu Oct 29 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.7-1
- Update to upstream 2.7.7 release

* Sat Sep 19 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.5-1
- Update to upstream 2.7.5 release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.4-5
- fix problem in tooltemplate patch

* Mon May 18 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.4-4
- make jline implicitly available to match upstream behavior

* Mon May 18 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.4-3
- fix problem with substitutions to scripts in %%install

* Mon May 18 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.4-2
- fix launcher scripts by modifying template, not overriding them

* Tue May 12 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.4-1
- update to 2.7.4 final

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.3-1
- update to 2.7.3 final

* Sun Nov 09 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-1
- update to 2.7.2 final

* Mon Nov 03 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-0.3.RC6
- bump release to fix upgrade path

* Sat Nov 01 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-0.1.RC6
- update to 2.7.2-RC6

* Thu Oct 30 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-0.1.RC5
- update to 2.7.2-RC5

* Sat Sep 06 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-0.2.RC1
- All code is now under BSD license
- Remove dll so and exe binaries in prep
- Add BuildRequires required by Java packaging guidelines
- Add missing defattr for examples and ant-scala

* Wed Aug 20 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-0.1.RC1
- update to 2.7.2-RC1

* Wed Aug 13 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.1-3
- regenerate classpath in manifest patch to apply cleanly to 2.7.1

* Wed Aug 13 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.1-2
- no changes, accidental release bump

* Mon May 05 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.1-1
- Update to 2.7.1

* Fri May 02 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.0-2
- Use java-sdk-openjdk for non-fc8 builds

* Mon Mar 10 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.0-1
- Update to 2.7.0
- License now correctly indicated as BSD and LGPLv2+
- Include LICENSE file in apidoc subpackage

* Mon Feb 11 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-8
- Adhere more strongly to the emacs package guidelines
- Include some comments regarding the boot-strapping process

* Wed Jan 16 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-7
- Add dist tag to release
- Fix directory ownership issues in %%_datadir/scala
- Remove source code from -devel package
- Rename -devel package to ant-scala
- Fix packaging of gtksourceview2 language spec
- Preserve timestamps when installing and cping
- Add patch to remove Class-Path entries from jar manifests
- Fix line endings in enscript/README
 
* Sun Jan 13 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-6
- Include further information about inclusion of binary distribution
- Unpack only those files needed from the binary distribution
- Include note about license approval

* Thu Dec 27 2007 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-5
- Add emacs(bin) BR
- Patch out call to subversion in build.xml
- Add pkgconfig to BuildRequires

* Thu Dec 27 2007 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-4
- Reformat emacs-scala description
- Expand tabs to spaces
- Fix -devel symlinks
- Better base package summary

* Wed Dec 26 2007 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-3
- Add ant config to devel package
- Require icedtea for build
- Move examples to %%{_datadir}/scala/examples
- Clean up package descriptions
- Add base package requirement for scala-examples and scala-devel

* Wed Dec 26 2007 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-2
- Fix post scripts
- Use spaces instead of tabs

* Wed Dec 26 2007 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-1
- Initial build.
