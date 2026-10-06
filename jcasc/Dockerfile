FROM jenkins/jenkins:2.492.1-lts-jdk21
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false" CASC_JENKINS_CONFIG=/var/jenkins_home/casc
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt
COPY jenkins.yaml /var/jenkins_home/casc/jenkins.yaml
