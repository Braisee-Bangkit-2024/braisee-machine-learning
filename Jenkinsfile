pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                echo 'Kode berhasil diambil dari GitHub.'
            }
        }
        
stage('Build Docker Image') {
    steps {
        echo 'Memulai proses build Docker image...'
        // PERUBAHAN DI SINI: Kita aktifkan BuildKit dan set network ke 'host'
        sh 'DOCKER_BUILDKIT=1 docker build --network=host -t nendaseputra/braisee-app:latest .'
        echo 'Build Docker image selesai.'
    }
}

        stage('Run Tests') {
            steps {
                // Nanti kita isi dengan test yang sesungguhnya
                echo 'Tahap testing... (lewatkan untuk saat ini)'
            }
        }

        // =======================================================
        // TAHAP BARU DIMULAI DARI SINI
        // =======================================================
// ... stage sebelumnya ...

        stage('Deploy Application') {
            steps {
                script {
                    def containerName = 'braisee-app-live'
                    
                    echo "Mencoba menghentikan dan menghapus kontainer lama: ${containerName}"
                    sh "docker stop ${containerName} || true"
                    sh "docker rm ${containerName} || true"
                    
                    echo "Menjalankan kontainer baru dari image nendaseputra/braisee-app:latest"
                    // PERUBAHAN DI SINI: Kita map ke port 8081 di host, tapi tetap menargetkan port 8080 di dalam container
                    sh "docker run -d --name ${containerName} -p 8081:8080 nendaseputra/braisee-app:latest"
                }
            }
        }
    }
}
