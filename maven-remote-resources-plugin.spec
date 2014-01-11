%{?_javapackages_macros:%_javapackages_macros}
Name:           maven-remote-resources-plugin
Version:        1.4
Release:        5.1%{?dist}
Summary:        Maven Remote Resources Plugin


License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-remote-resources-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildArch: noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: maven-local
BuildRequires: maven-plugin-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-shared-filtering
BuildRequires: plexus-containers-container-default
BuildRequires: velocity
BuildRequires: maven-shared-artifact-resolver
BuildRequires: maven-shared-common-artifact-filters
BuildRequires: maven-shared-downloader
BuildRequires: plexus-interpolation
BuildRequires: plexus-utils
BuildRequires: plexus-velocity
BuildRequires: plexus-resources
BuildRequires: junit
BuildRequires: maven-plugin-testing-harness
BuildRequires: maven-wagon
BuildRequires: maven-shared-verifier
BuildRequires: maven-surefire-provider-junit
BuildRequires: modello

Requires:       java
Requires:       maven
Requires:       maven-artifact-resolver
Requires:       maven-common-artifact-filters
Requires:       maven-filtering
Requires:       maven-monitor
Requires:       maven-plugin-annotations
Requires:       maven-project
Requires:       plexus-containers-container-default
Requires:       plexus-interpolation
Requires:       plexus-resources
Requires:       plexus-utils
Requires:       plexus-velocity
Requires:       velocity

Obsoletes:      maven2-plugin-remote-resources <= 0:2.0.8
Provides:       maven2-plugin-remote-resources = 1:%{version}-%{release}

%description
Process resources packaged in JARs that have been deployed to
a remote repository. The primary use case being satisfied is
the consistent inclusion of common resources in a large set of
projects. Maven projects at Apache use this plug-in to satisfy
licensing requirements at Apache where each project much include
license and notice files for each release.

%package javadoc

Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q

#Class org.apache.maven.shared.artifact.filter.collection.TransitivityFilter which ProcessRemoteResourcesMojo.java imports
#is renamed as org.apache.maven.shared.artifact.filter.collection.ProjectTransitivityFilter in
#the version 1.3 of maven-shared-common-artifact-filters package.
sed -i "s/TransitivityFilter/Project&/" `find -name ProcessRemoteResourcesMojo.java`

%build
# fix 613582
# we now use plexus-velocity which has the correct descriptor with a hint.
rm -f src/main/resources/META-INF/plexus/components.xml

mvn-rpmbuild install javadoc:aggregate -Dmaven.test.skip=true

%install
# jars
install -Dpm 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}.jar
# poms
install -Dpm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar


# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}/

%files
%doc DEPENDENCIES LICENSE NOTICE
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%doc DEPENDENCIES LICENSE NOTICE
%{_javadocdir}/%{name}

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-4
- BuildRequire newer version of Plexus container

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-1
- Update to upstream version 1.4

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Tomas Radej <tradej@redhat.com> - 1.3-1
- Updated to latest upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov  7 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.1-3
- Add plexus-resources to Requires

* Wed Sep 07 2011 Tomas Radej <tradej@redhat.com> - 1.2.1-2
- Added license files

* Tue Sep 6 2011 Alexander Kurtakov <akurtako@redhat.com> 1.2.1-1
- Update to latest upstream release.

* Tue Jul 5 2011 Alexander Kurtakov <akurtako@redhat.com> 1.2-3
- BR modello.

* Tue Jul 5 2011 Alexander Kurtakov <akurtako@redhat.com> 1.2-2
- Add missing requires on maven-shared-downloader.

* Thu Mar 17 2011 Alexander Kurtakov <akurtako@redhat.com> 1.2-1
- Update to upstream 1.2 release.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov  3 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-7
- Fix velocity dependency in pom.xml

* Thu Jul 15 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-6
- Fix bug #613582

* Tue Jul 13 2010 Hui Wang <huwang@redhat.com> - 1.1-5
- Add missing requires maven2

* Tue Jul 13 2010 Alexander Kurtakov <akurtako@redhat.com> 1.1-4
- Add missing maven-shared-artifact-resolver requires.

* Tue Jul 13 2010 Hui Wang <huwang@redhat.com> - 1.1-3
- Set '-Dmaven.test.skip=true' to fix Bug 613567

* Thu Jun 03 2010 Hui Wang <huwang@redhat.com> - 1.1-2
- Fixed descirption line length
- Added comment on patch0
- Used macro in add_to_maven_depmap

* Fri May 21 2010 Hui Wang <huwang@redhat.com> - 1.1-1
- Initial version of the package
