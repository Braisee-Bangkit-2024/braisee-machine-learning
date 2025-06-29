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
                // Kita gunakan nama image yang sama dengan nama proyek untuk konsistensi
                sh 'docker build . -t nendaseputra/braisee-app:latest'
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
        stage('Deploy Application') {
            steps {
                // 'script' block diperlukan untuk menjalankan logika shell yang lebih kompleks
                script {
                    // Beri nama yang konsisten pada kontainer aplikasimu
                    def containerName = 'braisee-app-live'
                    
                    echo "Mencoba menghentikan dan menghapus kontainer lama: ${containerName}"
                    // Perintah '|| true' adalah trik agar pipeline tidak gagal jika container tidak ditemukan
                    sh "docker stop ${containerName} || true"
                    sh "docker rm ${containerName} || true"
                    
                    echo "Menjalankan kontainer baru dari image nendaseputra/braisee-app:latest"
                    // Jalankan kontainer baru dengan nama yang sudah kita definisikan
                    sh "docker run -d --name ${containerName} -p 8080:8080 nendaseputra/braisee-app:latest"
                }
            }
        }
    }
}
