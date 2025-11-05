pipeline {
    agent any
    triggers {
        githubPush()
    }

    environment {
        // ... (Variabel environment tidak diubah)
        ARTIFACT_REGISTRY_REPO = 'asia-southeast2-docker.pkg.dev/stately-bulwark-464613-j5/jenkins-braisee'
        IMAGE_NAME             = 'braisee-app'
        CLOUD_RUN_SERVICE      = 'braisee-service-ml'
        CLOUD_RUN_REGION       = 'asia-southeast2'
        GCP_PROJECT_ID         = 'stately-bulwark-464613-j5'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    def DOCKER_IMAGE = "${ARTIFACT_REGISTRY_REPO}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    echo "1. Mendefinisikan Image: ${DOCKER_IMAGE}"
                    // Langkah 2: Build Image
                    sh "docker build -t ${DOCKER_IMAGE} ."
                    // Simpan variabel untuk stage berikutnya
                    env.DOCKER_IMAGE_TAGGED = DOCKER_IMAGE 
                }
            }
        }
        
        // --- STAGE: PUSH IMAGE DIUBAH MENJADI STEP LEBIH RINCI ---
        stage('Push Image to Artifact Registry') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCP_KEYFILE')]) {
                    // Mencegah blok 'script' besar agar Blue Ocean mencatat waktu setiap 'sh'
                    def REGISTRY_HOSTNAME = 'https://asia-southeast2-docker.pkg.dev'
                    
                    // Step 1: Login ke AR
                    echo "2.1. Memulai Otentikasi ke Artifact Registry"
                    sh "cat ${GCP_KEYFILE} | docker login -u _json_key --password-stdin ${REGISTRY_HOSTNAME}"
                    
                    // Step 2: Push Image
                    echo "2.2. Mendorong Image ke Registry"
                    sh "docker push ${env.DOCKER_IMAGE_TAGGED}"
                }
            }
        }

        // --- STAGE: DEPLOY DIUBAH MENJADI STEP LEBIH RINCI ---
        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCP_KEYFILE')]) {
                    
                    // Step 1: Aktivasi Akun Layanan GCP
                    echo "3.1. Mengaktifkan Service Account"
                    sh 'gcloud auth activate-service-account --key-file=${GCP_KEYFILE}'
                    
                    // Step 2: Set Project ID
                    echo "3.2. Mengatur Project ID"
                    sh "gcloud config set project ${GCP_PROJECT_ID}"
                    
                    // Step 3: Deployment Utama
                    echo "3.3. Melakukan Deployment Cloud Run"
                    sh """
                        gcloud run deploy ${CLOUD_RUN_SERVICE} \\
                            --image ${env.DOCKER_IMAGE_TAGGED} \\
                            --region ${CLOUD_RUN_REGION} \\
                            --platform managed \\
                            --allow-unauthenticated
                    """
                }
            }
        }
    }
}
