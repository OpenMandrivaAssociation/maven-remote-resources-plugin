Name:           maven-remote-resources-plugin
Version:        1.1
Release:        10
Summary:        Maven Remote Resources Plugin

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-remote-resources-plugin/
#svn export http://svn.apache.org/repos/asf/maven/plugins/tags/maven-remote-resources-plugin-1.1/
#tar jcf maven-remote-resources-plugin-1.1.tar.bz2 maven-remote-resources-plugin-1.1/
Source0:        %{name}-%{version}.tar.bz2
#Class org.apache.maven.shared.artifact.filter.collection.TransitivityFilter which ProcessRemoteResourcesMojo.java imports
#is renamed as org.apache.maven.shared.artifact.filter.collection.ProjectTransitivityFilter in
#the version 1.3 of maven-shared-common-artifact-filters package.
Patch0:        ProcessRemoteResourcesMojo.java.patch

# TODO: upstream
Patch1:        0001-Fix-velocity-dep.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: maven2
BuildRequires: maven-plugin-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-shared-filtering
BuildRequires: plexus-container-default
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

Requires:       maven2
Requires:       java
Requires:       jpackage-utils
Requires:       maven-wagon
Requires:       maven-shared-artifact-resolver

Requires(post):       jpackage-utils
Requires(postun):     jpackage-utils

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
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build
# fix 613582
# we now use plexus-velocity which has the correct descriptor with a hint.
rm -f src/main/resources/META-INF/plexus/components.xml

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -Dpm 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.apache.maven.plugins %{name} %{version} JPP %{name}

# poms
install -Dpm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

