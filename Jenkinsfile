node() {
	def os = System.properties['os.name'].toLowerCase()
	env.WORKSPACE_LOCAL = sh(returnStdout: true, script: 'pwd').trim()
	env.BUILD_TIME = "${BUILD_TIMESTAMP}"
	def HUDSON_URL = "${env.HUDSON_URL}"
	def SERVER_JENKINS = ""
	if (HUDSON_URL.contains("10.88.48.21")) {
		SERVER_JENKINS = "WOPR-SB"
	} else {
		SERVER_JENKINS = "WOPR-PROD-JENKINS"
	}
	def passthruString = sh(script: "printenv", returnStdout: true)
	passthruString = passthruString.replaceAll('\n',' ')
	stage("Prepare Workspace") {
		echo "\n\n\n*** Prepare Workspace on ${SERVER_JENKINS} ***"
		cleanWs()
		echo "Workspace set to: " + env.WORKSPACE_LOCAL
		echo "Build time: " + env.BUILD_TIME
		sh "ls -l"
		def url = "${scm.userRemoteConfigs}"
		def repoURL = url.split(" ")[2]
		def branches = scm.branches[0].name
		def branch2 = branches.split("/")[1]
		git branch: branch2, url: repoURL
                echo " ** REPO SHARED LIBRARIES FOR ALL GIT-ARC PROJECTS ** "
                git branch: "main", url: GIT_SHARED_LIB
		sh "ls -l"
	}
	stage("AWX Runner") {
            def awx_output = sh(script: "python3 ${orchPy} ${passthruString}", returnStdout: true)
            echo "${awx_output}"
        }
	stage("BDD-Behave") {
		echo "\n\n\n*** BDD-Behave-Python3 on ${SERVER_JENKINS} ***"
                sh "/var/lib/jenkins/.pyenv/shims/behave -v"
                echo "\n\n\n"
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
	stage('Import results to Xray') {
		echo "\n\n*** Import Results to XRAY ***"
		def description = "[STC_BUILD_URL|${env.BUILD_URL}]"
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
                "summary": "Testing Jenkins - Automated Regression Execution @ ''' + env.BUILD_TIME + ' ' + environment + ''' " ,
                "issuetype": {
                    "id": "''' + testExecutionFieldId + '''"
                }
            }
        }'''
		echo info
		step([$class: 'XrayImportBuilder', endpointName: '/cucumber/multipart', importFilePath: 'reports/cucumber.json', importInfo: info, inputInfoSwitcher: 'fileContent', serverInstance: xrayConnectorId])
    
	}
}
