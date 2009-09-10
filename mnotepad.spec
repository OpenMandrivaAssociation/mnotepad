Name:		mnotepad
Version:	0.5
Release:	%mkrel 6
%define netbeansdir             %{_prefix}/lib/netbeans
%define nbjfuguesupportdir      %{_prefix}/lib/mnotepad

Summary:        Music Notepad based on JFugue
License:        CDDL
Url:            https://nbjfuguesupport.dev.java.net/
Group:		Sound
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
#
Source0:        nbjfuguesupport-%{version}.zip
Source1:        mnotepad.sh
Epoch:		0
BuildArch:	noarch
BuildRequires:	java-rpmbuild >= 1.6
BuildRequires:	libnb-platform7 >= 6.0
BuildRequires:	libnb-platform7-devel >= 6.0
Requires:	libnb-platform7 >= 6.0
Requires:	jfugue >= 3.2
BuildRequires:	jfugue >= 3.2
BuildRequires:	java >= 1.5
Requires:	java >= 1.5
BuildRequires:  ant ant-nodeps

%description
All that Music NotePad does is to enable the user to generate JFugue music 
strings, without needing to understand what they are, how they work, 
or what they're for. For example, when a quarter note is dragged to 
the "E" line in the clef register of the music sheet, a string consisting 
of "E5q" is generated in the Editor (right side of the screen, below 
the Palette). The JFugue API knows what to do with this string and, when 
File > Play is selected, the JFugue API plays the note. When File > Save 
is selected, the complete content of the Editor, which contains all the JFugue 
music strings in the order in which they were added, is played and then saved 
as a MIDI file. When a new instrument is selected, a related string is added to
the editor, and all subsequent notes are played by the last selected
instrument.


%prep
%{__rm} -fr %{buildroot}
%setup -q -c -n %{name}-%{version}
%remove_java_binaries || :

%{__mkdir_p} nbjfuguesupport-0.5/jfugue/release/modules/ext/
%{__ln_s} %{_javadir}/jfugue.jar nbjfuguesupport-%{version}/jfugue/release/modules/ext/jfugue.jar

%build
%{ant} -f nbjfuguesupport-%{version}/build.xml build-zip \
  -Dnbplatform.default.harness.dir=/usr/lib/netbeans/harness/ \
  -Dnbplatform.default.netbeans.dest.dir=/usr/lib/netbeans/

%install
# jar
%{__install} -d -m 755 %{buildroot}%{nbjfuguesupportdir}
cp -r nbjfuguesupport-%{version}/build/cluster/* %{buildroot}%{nbjfuguesupportdir}
%{__rm} %{buildroot}%{nbjfuguesupportdir}/modules/ext/jfugue.jar
%{__ln_s} %{_javadir}/jfugue.jar %{buildroot}%{nbjfuguesupportdir}/modules/ext/jfugue.jar
%{__mkdir_p} %{buildroot}/usr/bin/
%{__install} -m 755 %{SOURCE1} %{buildroot}/usr/bin/mnotepad
%{__mkdir_p} %{buildroot}/etc/
%{__install} -m 644 nbjfuguesupport-%{version}/build/launcher/etc/mnotepad.conf %{buildroot}/etc


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{nbjfuguesupportdir}/*
/etc/mnotepad.conf
/usr/bin/mnotepad


