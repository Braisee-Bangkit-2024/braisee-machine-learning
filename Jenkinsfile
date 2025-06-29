// Ini adalah cetak biru pipeline-mu.
pipeline {
    // 'agent any' artinya pekerjaan ini bisa dijalankan di server Jenkins mana saja yang tersedia.
    agent any

    // 'stages' adalah kumpulan semua tahapan kerja.
    stages {
        // 'stage' adalah satu tahapan spesifik. Beri nama yang jelas.
        stage('Checkout Code') {
            steps {
                // 'checkout scm' adalah perintah standar untuk mengambil source code dari Git.
                checkout scm
                echo 'Kode berhasil diambil dari GitHub.'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Memulai proses build Docker image...'
                // 'sh' adalah cara Jenkins menjalankan perintah terminal.
                // Ganti dengan perintah build docker-mu yang sebenarnya.
                sh 'docker build . -t braisee-app:jenkins-build'
                echo 'Build Docker image selesai.'
            }
        }

        stage('Run Tests') {
            steps {
                // Kosongkan dulu untuk sekarang. Nanti kita isi.
                echo 'Tahap testing... (lewatkan untuk saat ini)'
            }
        }
    }
}