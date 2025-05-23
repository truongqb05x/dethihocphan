document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const sidebar = document.querySelector('.sidebar');
    
    mobileMenuBtn.addEventListener('click', function() {
        sidebar.classList.toggle('active');
        mobileMenuBtn.innerHTML = sidebar.classList.contains('active') 
            ? '<i class="fas fa-times"></i>' 
            : '<i class="fas fa-bars"></i>';
    });

    // Theme toggle function
    const toggleTheme = (theme) => {
        const themeBtns = document.querySelectorAll('.theme-btn');
        const body = document.body;
        
        themeBtns.forEach(b => b.classList.remove('active'));
        const activeThemeBtn = document.querySelector(`.theme-btn[data-theme="${theme}"]`);
        if (activeThemeBtn) {
            activeThemeBtn.classList.add('active');
        }
        
        body.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        const themeIcon = document.querySelector('.theme-icon i');
        themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    };

    // Theme toggle for sidebar buttons
    const themeBtns = document.querySelectorAll('.theme-btn');
    themeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const theme = this.getAttribute('data-theme');
            toggleTheme(theme);
        });
    });

    // Theme toggle for header icon
    const themeIcon = document.querySelector('.theme-icon');
    themeIcon.addEventListener('click', function() {
        const currentTheme = document.body.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        toggleTheme(newTheme);
    });

    // Initialize theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    toggleTheme(savedTheme);

    // Tab switching functionality
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs and contents
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });

    // File upload functionality
    const fileUploadArea = document.getElementById('file-upload-area');
    const fileInput = document.getElementById('file-input');
    const fileList = document.getElementById('file-list');

    fileUploadArea.addEventListener('click', () => fileInput.click());
    
    fileUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadArea.style.borderColor = 'var(--primary)';
        fileUploadArea.style.backgroundColor = 'rgba(255, 109, 40, 0.05)';
    });
    
    fileUploadArea.addEventListener('dragleave', () => {
        fileUploadArea.style.borderColor = 'var(--border)';
        fileUploadArea.style.backgroundColor = '';
    });
    
    fileUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadArea.style.borderColor = 'var(--border)';
        fileUploadArea.style.backgroundColor = '';
        
        if (e.dataTransfer.files.length) {
            handleFiles(e.dataTransfer.files);
        }
    });
    
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length) {
            handleFiles(fileInput.files);
        }
    });
    
    function handleFiles(files) {
        fileList.innerHTML = '';
        
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            
            const fileIcon = document.createElement('div');
            fileIcon.className = 'file-icon';
            
            // Determine icon based on file type
            if (file.type.includes('pdf')) {
                fileIcon.innerHTML = '<i class="fas fa-file-pdf"></i>';
            } else if (file.type.includes('word') || file.type.includes('document')) {
                fileIcon.innerHTML = '<i class="fas fa-file-word"></i>';
            } else if (file.type.includes('powerpoint') || file.type.includes('presentation')) {
                fileIcon.innerHTML = '<i class="fas fa-file-powerpoint"></i>';
            } else {
                fileIcon.innerHTML = '<i class="fas fa-file"></i>';
            }
            
            const fileName = document.createElement('div');
            fileName.className = 'file-name';
            fileName.textContent = file.name;
            
            const fileSize = document.createElement('div');
            fileSize.className = 'file-size';
            fileSize.textContent = formatFileSize(file.size);
            
            const fileRemove = document.createElement('div');
            fileRemove.className = 'file-remove';
            fileRemove.innerHTML = '<i class="fas fa-times"></i>';
            fileRemove.addEventListener('click', () => {
                fileItem.remove();
            });
            
            fileItem.appendChild(fileIcon);
            fileItem.appendChild(fileName);
            fileItem.appendChild(fileSize);
            fileItem.appendChild(fileRemove);
            
            fileList.appendChild(fileItem);
        }
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i]);
    }

    // Faculty select based on university
    const universitySelect = document.getElementById('university');
    const facultySelect = document.getElementById('faculty');
    
    universitySelect.addEventListener('change', function() {
        // In a real app, you would fetch faculties based on selected university
        facultySelect.innerHTML = '<option value="">-- Chọn khoa --</option>';
        
        if (this.value === '1') {
            // Bách Khoa faculties
            addOption(facultySelect, '1', 'Công nghệ Thông tin');
            addOption(facultySelect, '2', 'Điện - Điện tử');
            addOption(facultySelect, '3', 'Cơ khí');
        } else if (this.value === '2') {
            // Khoa học Tự nhiên faculties
            addOption(facultySelect, '4', 'Toán - Cơ - Tin học');
            addOption(facultySelect, '5', 'Vật lý');
            addOption(facultySelect, '6', 'Hóa học');
        } else if (this.value === '3') {
            // Kinh tế Quốc dân faculties
            addOption(facultySelect, '7', 'Quản trị Kinh doanh');
            addOption(facultySelect, '8', 'Kế toán');
            addOption(facultySelect, '9', 'Tài chính - Ngân hàng');
        }
    });

    // Subject select based on faculty
    facultySelect.addEventListener('change', function() {
        const subjectSelect = document.getElementById('subject');
        subjectSelect.innerHTML = '<option value="">-- Chọn môn học --</option>';
        
        if (this.value === '1') {
            // CNTT subjects
            addOption(subjectSelect, '1', 'Lập trình hướng đối tượng');
            addOption(subjectSelect, '2', 'Cấu trúc dữ liệu và giải thuật');
            addOption(subjectSelect, '3', 'Cơ sở dữ liệu');
        } else if (this.value === '2') {
            // Điện - Điện tử subjects
            addOption(subjectSelect, '4', 'Kỹ thuật điện');
            addOption(subjectSelect, '5', 'Kỹ thuật điện tử');
            addOption(subjectSelect, '6', 'Vi xử lý');
        }
        // Add more cases as needed
    });

    // Faculty select for subject tab
    const subjectUniversitySelect = document.getElementById('subject-university');
    const subjectFacultySelect = document.getElementById('subject-faculty');
    
    subjectUniversitySelect.addEventListener('change', function() {
        // Similar to universitySelect change handler
        subjectFacultySelect.innerHTML = '<option value="">-- Chọn khoa --</option>';
        
        if (this.value === '1') {
            addOption(subjectFacultySelect, '1', 'Công nghệ Thông tin');
            addOption(subjectFacultySelect, '2', 'Điện - Điện tử');
            addOption(subjectFacultySelect, '3', 'Cơ khí');
        } else if (this.value === '2') {
            addOption(subjectFacultySelect, '4', 'Toán - Cơ - Tin học');
            addOption(subjectFacultySelect, '5', 'Vật lý');
            addOption(subjectFacultySelect, '6', 'Hóa học');
        }
    });

    // Helper function to add options to select
    function addOption(selectElement, value, text) {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = text;
        selectElement.appendChild(option);
    }
});
