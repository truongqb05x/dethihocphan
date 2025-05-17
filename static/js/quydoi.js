document.addEventListener('DOMContentLoaded', async function() {
    let userId = null;

    // Lấy user_id từ API check-session
    try {
        const response = await fetch('/check-session', {
            method: 'GET',
            credentials: 'same-origin' // Đảm bảo gửi cookie/session
        });
        const data = await response.json();

        if (data.loggedIn) {
            userId = data.user_id; // Giả sử API trả về user_id
            console.log('User ID:', userId);
        } else {
            console.error('User not logged in');
            alert('Vui lòng đăng nhập để tiếp tục.');
            return; // Thoát nếu không đăng nhập
        }
    } catch (error) {
        console.error('Error fetching session:', error);
        alert('Lỗi khi kiểm tra phiên đăng nhập.');
        return;
    }

    // Modal functionality
    const uploadBtn = document.getElementById('uploadBtn');
    const viewContributionsBtn = document.getElementById('viewContributionsBtn');
    const buyViewsBtn = document.getElementById('buyViewsBtn');
    const uploadModal = document.getElementById('uploadModal');
    const contributionsModal = document.getElementById('contributionsModal');
    const buyViewsModal = document.getElementById('buyViewsModal');
    const loadingModal = document.getElementById('loadingModal');
    const successModal = document.getElementById('successModal');
    const closeButtons = document.querySelectorAll('.modal-close');
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const successCloseBtn = document.getElementById('successCloseBtn');
    const fileError = document.getElementById('fileError');

    // Open modals
    uploadBtn.addEventListener('click', () => {
        uploadModal.classList.add('active');
        fileError.style.display = 'none';
    });

    viewContributionsBtn.addEventListener('click', () => {
        contributionsModal.classList.add('active');
        fetchContributions();
    });

    buyViewsBtn.addEventListener('click', () => {
        buyViewsModal.classList.add('active');
    });

    // Close modals
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.closest('.modal').classList.remove('active');
            fileError.style.display = 'none';
        });
    });

    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.classList.remove('active');
            fileError.style.display = 'none';
        }
    });

    successCloseBtn.addEventListener('click', () => {
        successModal.classList.remove('active');
    });

    // File upload drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.style.borderColor = 'var(--primary)';
        dropArea.style.backgroundColor = 'rgba(255, 109, 40, 0.1)';
    }

    function unhighlight() {
        dropArea.style.borderColor = 'var(--border)';
        dropArea.style.backgroundColor = '';
    }

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        handleFiles(files);
        fileError.style.display = 'none';
    }

    dropArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        if (this.files.length) {
            handleFiles(this.files);
            fileError.style.display = 'none';
        }
    });

    // Hàm xử lý file được chọn hoặc kéo thả
    function handleFiles(files) {
        const file = files[0];
        if (file) {
            // Kiểm tra kích thước file (tối đa 20MB)
            if (file.size <= 20 * 1024 * 1024) {
                // Cắt ngắn tên file nếu quá dài
                const fileName = file.name.length > 30
                    ? file.name.substring(0, 15) + '...' + file.name.substring(file.name.length - 10)
                    : file.name;

                // Cập nhật giao diện khu vực kéo thả với thông tin file
                dropArea.innerHTML = `
                    <i class="fas fa-file-alt" style="color: var(--success);"></i>
                    <h4 class="file-upload-text">${fileName}</h4>
                    <p class="file-upload-hint">${(file.size / 1024 / 1024).toFixed(2)} MB</p>
                `;
            } else {
                // Thông báo lỗi nếu file quá lớn
                alert('File quá lớn. Vui lòng chọn file nhỏ hơn 20MB.');
                fileInput.value = '';
            }
        }
    }

    // Handle form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        if (!fileInput.files || fileInput.files.length === 0) {
            fileError.style.display = 'block';
            fileError.textContent = 'Vui lòng chọn một file.';
            return;
        }

        if (!userId) {
            alert('Không thể xác định người dùng. Vui lòng đăng nhập lại.');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('user_id', userId);

        loadingModal.classList.add('active');

        try {
            const response = await fetch('/api/upload_document', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                uploadModal.classList.remove('active');
                loadingModal.classList.remove('active');
                successModal.classList.add('active');
                uploadForm.reset();
                dropArea.innerHTML = `
                    <i class="fas fa-file-upload"></i>
                    <h4 class="file-upload-text">Kéo thả tài liệu vào đây hoặc nhấn để chọn</h4>
                    <p class="file-upload-hint">Hỗ trợ file PDF, DOCX, PPTX (tối đa 20MB)</p>
                `;
            } else {
                throw new Error(result.error || 'Upload failed');
            }
        } catch (error) {
            loadingModal.classList.remove('active');
            fileError.style.display = 'block';
            fileError.textContent = 'Lỗi: ' + error.message;
        }
    });

    // Fetch contributions
    async function fetchContributions() {
        if (!userId) {
            console.error('No user ID available');
            return;
        }

        try {
            const response = await fetch(`/api/contributions/${userId}`);
            const contributions = await response.json();
            const tableBody = document.getElementById('contributionsTableBody');
            tableBody.innerHTML = '';

            contributions.forEach(contribution => {
                // Set views_earned to 3 if status is approved
                const viewsEarned = contribution.status === 'approved' ? 3 : contribution.views_earned;
                
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${contribution.file_name}</td>
                    <td>${new Date(contribution.created_at).toLocaleDateString('vi-VN')}</td>
                    <td><span class="status status-${contribution.status}">${getStatusText(contribution.status)}</span></td>
                    <td>${viewsEarned}</td>
                `;
                tableBody.appendChild(row);
            });
        } catch (error) {
            console.error('Error fetching contributions:', error);
            alert('Lỗi khi tải danh sách đóng góp: ' + error.message);
        }
    }

    function getStatusText(status) {
        switch (status) {
            case 'approved': return 'Đã duyệt';
            case 'pending': return 'Chờ duyệt';
            case 'rejected': return 'Từ chối';
            default: return status;
        }
    }

    // Handle payment
    const packageButtons = document.querySelectorAll('.select-package');
    const paymentSection = document.getElementById('paymentSection');

    packageButtons.forEach(button => {
        button.addEventListener('click', function() {
            packageButtons.forEach(btn => {
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-outline');
            });
            this.classList.remove('btn-outline');
            this.classList.add('btn-primary');
            paymentSection.style.display = 'block';
            const amount = this.getAttribute('data-amount');
            const views = this.getAttribute('data-views');
            document.getElementById('selectedPackageText').textContent = `${views} lượt xem`;
            document.getElementById('totalAmountText').textContent = `${parseInt(amount).toLocaleString()}₫`;
            paymentSection.scrollIntoView({ behavior: 'smooth' });
        });
    });

    const walletOption = document.getElementById('walletOption');
    const bankOption = document.getElementById('bankOption');
    const walletDetails = document.getElementById('walletDetails');
    const bankDetails = document.getElementById('bankDetails');
    const confirmPayment = document.getElementById('confirmPayment');
    const confirmPaymentBtn = document.getElementById('confirmPaymentBtn');

    walletOption.addEventListener('click', function() {
        this.classList.toggle('active');
        walletDetails.classList.toggle('active');
        bankOption.classList.remove('active');
        bankDetails.classList.remove('active');
        const icon = this.querySelector('.fa-chevron-down');
        icon.className = walletDetails.classList.contains('active')
            ? 'fas fa-chevron-up'
            : 'fas fa-chevron-down';
    });

    bankOption.addEventListener('click', function() {
        this.classList.toggle('active');
        bankDetails.classList.toggle('active');
        walletOption.classList.remove('active');
        walletDetails.classList.remove('active');
        const icon = this.querySelector('.fa-chevron-down');
        icon.className = bankDetails.classList.contains('active')
            ? 'fas fa-chevron-up'
            : 'fas fa-chevron-down';
    });

    const walletItems = document.querySelectorAll('.wallet-item');
    walletItems.forEach(item => {
        item.addEventListener('click', function() {
            walletItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            const walletName = this.querySelector('span').textContent;
            document.getElementById('selectedMethodText').textContent = walletName;
            confirmPayment.classList.add('active');
        });
    });

    const bankItems = document.querySelectorAll('.bank-item');
    bankItems.forEach(item => {
        item.addEventListener('click', function() {
            bankItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            const bankName = this.querySelector('.bank-name').textContent;
            document.getElementById('selectedMethodText').textContent = `Thẻ ${bankName}`;
            confirmPayment.classList.add('active');
        });
    });

    confirmPaymentBtn.addEventListener('click', () => {
        buyViewsModal.classList.remove('active');
        loadingModal.classList.add('active');
        setTimeout(() => {
            loadingModal.classList.remove('active');
            successModal.classList.add('active');
            document.getElementById('successMessage').textContent = 'Lượt xem đã được thêm vào tài khoản của bạn.';
        }, 2000);
    });
});