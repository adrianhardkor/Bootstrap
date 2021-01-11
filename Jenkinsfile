node() {
    def STC_INSTALL = "/opt/STC_CLIENT/Spirent_TestCenter_5.16/Spirent_TestCenter_Application_Linux64Client/"
    def os = System.properties['os.name'].toLowerCase()
    try {
        notifyBuild('STARTED')
        def passthruString = sh(script: "printenv", returnStdout: true)
        passthruString = passthruString.replaceAll('\n',' ')
        def paramsString1 = params.toString().replaceAll("[\\[\\](){}]","")
        paramsString = paramsString1.replaceAll(', ',' ')
        def paramsStringXray = paramsString1.replaceAll(', ','\\n - ')
        def HUDSON_URL = "${env.HUDSON_URL}"
        def SERVER_JENKINS = ""
        if (HUDSON_URL.contains("10.88.48.21")) {
            SERVER_JENKINS = "WOPR-SB"
        } else {
            SERVER_JENKINS = "WOPR-PROD-JENKINS"
        }       
        stage("Prepare Workspace") {
            echo "*** Prepare Workspace ***"
            cleanWs()
            sh "ls -l"
            env.WORKSPACE_LOCAL = sh(returnStdout: true, script: 'pwd').trim()
            env.BUILD_TIME = "${BUILD_TIMESTAMP}"
            echo "Workspace set to:" + env.WORKSPACE_LOCAL
            echo "Build time:" + env.BUILD_TIME
        }
        stage('Checkout Self') {
            echo "\n\n\n GIT CLONE STAGE"
            def url = "${scm.userRemoteConfigs}"
            def repoURL = url.split(" ")[2]
            def branches = scm.branches[0].name
            def branch2 = branches.split("/")[1]
            git branch: branch2, url: repoURL
            echo " ** REPO SHARED LIBRARIES FOR ALL GIT-ARC PROJECTS ** "
            sh """
                mkdir lib
                cd lib/
                git clone ${GIT_SHARED_LIB}
                cd ..
                ls -l
            """
            echo "\n\n\n"
        }
        stage("Get Gsheet Credentials") {
           def User_Pass_Json = sh(script: "python3 ./src/gsheet_get_Architecture_Login_pwd.py", returnStdout: true).trim()
           // User_Pass_Json = User_Pass_Json.replaceAll("\'", '"')
           env.User_Pass_Json = User_Pass_Json
           // echo "\n\n\n env.User_Pass_Json = ${env.User_Pass_Json}\n\n\n"
        }
        stage("AWX Runner") {
            def awx_output = sh(script: "python3 ${orchPy} ${paramsString}", returnStdout: true)
            def awx_output_xray = awx_output.replaceAll("\n",'\\n')
            echo "${awx_output}"
        }
        stage("BDD-Behave") {
            echo "\n\n\n*** BDD-Behave-Python3 on ${SERVER_JENKINS} ***"
            // sh "/var/lib/jenkins/.pyenv/shims/behave -v"
            // echo "\n\n\n"
            try {
                sh """
                    export SERVER_JENKINS=${SERVER_JENKINS}
                    export STC_PRIVATE_INSTALL_DIR=${STC_INSTALL}
                    /var/lib/jenkins/.pyenv/shims/behave -f cucumber -o reports/cucumber.json --junit
                """
            } catch (error) {
                echo "\n\n\n FAILURE FOUND -- CONTINUING TO XRAY-IMPORT \n\n\n"
            } finally {
                echo "*** JUNIT ***"
                junit skipPublishingChecks: true, allowEmptyResults: true, keepLongStdio: true, testResults: 'reports/*.xml'
            } 
        }
        stage ('Cucumber Reports') {
            cucumber buildStatus: "UNSTABLE",
            fileIncludePattern: "**/cucumber.json",
            jsonReportDirectory: 'reports'
        }
        stage('Import results to Xray') {
            echo "*** Import Results to XRAY ***"
            def description = "[${env.JOB_NAME} Test Report|${env.BUILD_URL}/cucumber-html-reports/overview-features.html] \\n \\n INPUTS:\\n ${paramsStringXray}" 
            def labels = '["regression","automated_regression"]'
            def environment = "DEV"
            def testExecutionFieldId = 10552
            def testEnvironmentFieldName = "customfield_10372"
            def projectKey = "XT"
            def projectId = 10606
            def xrayConnectorId = "${xrayConnectorId}"
            def info = '''{
                "fields": {
                    "project": {
                        "id": "''' + projectId + '''"
                    },
                    "labels":''' + labels + ''',
                    "description":"''' + description + '''",
                    "summary": "''' + env.JOB_NAME + ''' Automated Test Execution @ ''' + env.BUILD_TIME + ' ' + environment + ''' " ,
                    "issuetype": {
                        "id": "''' + testExecutionFieldId + '''"
                    }
                }
            }'''
            echo info
            step([$class: 'XrayImportBuilder', 
            endpointName: '/cucumber/multipart', 
            importFilePath: 'reports/cucumber.json', 
            importInfo: info, 
            inputInfoSwitcher: 'fileContent', 
            serverInstance: xrayConnectorId])
        }
    }
    catch(e) {                           
        // If there was an exception thrown, the build failed
        currentBuild.result = "FAILED"
        throw e
    } finally {
        // Success or failure, always send notifications
        echo "I AM HERE"
        notifyBuild(currentBuild.result)
    }
}
def notifyBuild(String buildStatus = 'STARTED') {
    // build status of null means successful
    buildStatus =  buildStatus ?: 'SUCCESSFUL'
    // Default values
    def colorName = 'RED'
    def colorCode = '#FF0000'
    def subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
    def summary = "${subject} (${env.BUILD_URL})"
    def details = """<p>STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
      <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>"""
      // Override default values based on build status
      if (buildStatus == 'STARTED') {
        color = 'BLUE'
        colorCode = '#0000FF'
        msg = "Build: ${env.JOB_NAME} has started: ${BUILD_TIMESTAMP}"
      } else if (buildStatus == 'UNSTABLE') {
        color = 'YELLOW'
        colorCode = '#FFFF00'
        msg = "Build: ${env.JOB_NAME} was listed as unstable. Look at ${env.BUILD_URL} and Report: ${env.BUILD_URL}/cucumber-html-reports/overview-features.html"
      } else if (buildStatus == 'SUCCESSFUL') {
        color = 'GREEN'
        colorCode = '#00FF00'
        msg = "Build: ${env.JOB_NAME} Completed Successfully ${env.BUILD_URL} Report: ${env.BUILD_URL}/cucumber-html-reports/overview-features.html"
      } else {
        color = 'RED'
        colorCode = '#FF0000'
        msg = "Build: ${env.JOB_NAME} had an issue ${env.BUILD_URL}/console"
      }
    // Send notifications
    slackSend baseUrl: 'https://hooks.slack.com/services/', 
    channel: 'wopr-jenkins-test', 
    color: colorCode, 
    message: msg,
    teamDomain: 'https://wow-technology.slack.com', 
    tokenCredentialId: 'Slack-Token', 
    username: 'JenkinsAutomation'
}
