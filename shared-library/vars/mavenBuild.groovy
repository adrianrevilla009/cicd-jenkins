// Global step: mavenBuild(goals: 'verify', javaImage: 'maven:3.9.9-eclipse-temurin-21')
def call(Map cfg = [:]) {
  String goals = cfg.get('goals', 'verify')
  String buildImage = cfg.get('javaImage', 'maven:3.9.9-eclipse-temurin-21')
  pipeline {
    agent { docker { image buildImage } }
    options { timeout(time: 15, unit: 'MINUTES') }
    stages {
      stage('Maven') {
        steps { sh "mvn -B ${goals}" }
      }
    }
    post { always { junit allowEmptyResults: true, testResults: 'target/surefire-reports/*.xml' } }
  }
}
