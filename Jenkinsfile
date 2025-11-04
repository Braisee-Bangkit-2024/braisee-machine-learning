pipeline {
    agent any


        triggers {
        githubPush()
    }

    environment {
        // Alamat LENGKAP ke repositori Artifact Registry-mu
        ARTIFACT_REGISTRY_REPO = 'asia-southeast2-docker.pkg.dev/stately-bulwark-464613-j5/jenkins-braisee'
        
        // Nama image aplikasimu
        IMAGE_NAME             = 'braisee-app'
        
        // Konfigurasi Cloud Run
        CLOUD_RUN_SERVICE      = 'braisee-service-ml' // Pastikan nama ini sesuai
        CLOUD_RUN_REGION       = 'asia-southeast2'
        GCP_PROJECT_ID         = 'stately-bulwark-464613-j5' // Pastikan Project ID ini benar
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Definisikan nama image lengkap menggunakan variabel yang benar
                    def DOCKER_IMAGE = "${ARTIFACT_REGISTRY_REPO}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    echo "Building image: ${DOCKER_IMAGE}"
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }
        stage('Push Image to Artifact Registry') {
            steps {
                // withCredentials HARUS di dalam steps
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCP_KEYFILE')]) {
                    script {
                        def DOCKER_IMAGE = "${ARTIFACT_REGISTRY_REPO}/${IMAGE_NAME}:${BUILD_NUMBER}"
                        def REGISTRY_HOSTNAME = 'https://asia-southeast2-docker.pkg.dev'

                        echo "Authenticating to Artifact Registry and pushing image..."
                        // Gunakan hostname yang benar untuk login
                        sh "cat ${GCP_KEYFILE} | docker login -u _json_key --password-stdin ${REGISTRY_HOSTNAME}"
                        sh "docker push ${DOCKER_IMAGE}"
                    }
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                // withCredentials HARUS di dalam steps
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCP_KEYFILE')]) {
                    script {
                        def DOCKER_IMAGE = "${ARTIFACT_REGISTRY_REPO}/${IMAGE_NAME}:${BUILD_NUMBER}"
                        
                        echo "Deploying to Cloud Run service: ${CLOUD_RUN_SERVICE}"
                        sh 'gcloud auth activate-service-account --key-file=${GCP_KEYFILE}'
                        sh "gcloud config set project ${GCP_PROJECT_ID}"
                        sh """
                            gcloud run deploy ${CLOUD_RUN_SERVICE} \\
                                --image ${DOCKER_IMAGE} \\
                                --region ${CLOUD_RUN_REGION} \\
                                --platform managed \\
                                --allow-unauthenticated
                        """
                    }
                }
            }
        }
    }
}
