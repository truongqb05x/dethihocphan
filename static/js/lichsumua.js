        let viewedExams = [];
        let complaints = [];

        function showError(message) {
            const tableBody = document.getElementById('examTableBody');
            tableBody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; padding: 2rem; color: var(--error);">
                        <i class="fas fa-exclamation-circle" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                        <p>${message}</p>
                    </td>
                </tr>
            `;
        }

        async function fetchViewedExams() {
            try {
                const response = await fetch('/api/viewed_documents');
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Không thể tải danh sách tài liệu đã xem');
                }
                viewedExams = await response.json();
                filterExams();
            } catch (error) {
                showError(error.message);
                if (error.message.includes('đăng nhập')) {
                    setTimeout(() => {
                        window.location.href = '/index.html';
                    }, 2000);
                }
            }
        }

        function renderExamTable(exams) {
            const tableBody = document.getElementById('examTableBody');
            tableBody.innerHTML = '';

            if (exams.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="6" style="text-align: center; padding: 2rem; color: var(--text-light);">
                            Không có tài liệu nào đã xem
                        </td>
                    </tr>
                `;
                return;
            }

            exams.forEach(exam => {
                let iconClass = '';
                let iconColor = '';
                switch (exam.type.toLowerCase()) {
                    case 'pdf':
                        iconClass = 'fa-file-pdf';
                        iconColor = '#e34c26';
                        break;
                    case 'word':
                        iconClass = 'fa-file-word';
                        iconColor = '#2b579a';
                        break;
                    case 'excel':
                        iconClass = 'fa-file-excel';
                        iconColor = '#217346';
                        break;
                    case 'zip':
                        iconClass = 'fa-file-archive';
                        iconColor = '#7c4dff';
                        break;
                    default:
                        iconClass = 'fa-file';
                        iconColor = 'var(--text-light)';
                }

                const complaint = complaints.find(c => c.examName === exam.name);
                const complaintStatus = complaint 
                    ? `<span class="status-${complaint.status}" data-exam="${exam.name}">
                        ${complaint.status === 'pending' ? 'Đang chờ' : 'Chấp thuận'}
                       </span>`
                    : `<button class="action-btn complaint-btn" data-name="${exam.name}" title="Gửi khiếu nại">
                        <i class="fas fa-exclamation-circle"></i>
                       </button>`;

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>
                        <i class="fas ${iconClass} file-icon" style="color: ${iconColor};"></i>
                        ${exam.name}
                    </td>
                    <td>${exam.type}</td>
                    <td>${exam.size}</td>
                    <td>${exam.purchaseDate}</td>
                    <td>${complaintStatus}</td>
                    <td>
                        <div class="file-actions">
                            <button class="action-btn view-btn" data-path="${exam.path}" title="Xem đề thi">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button class="action-btn download-btn" data-name="${exam.name}" title="Tải xuống">
                                <i class="fas fa-download"></i>
                            </button>
                        </div>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            document.querySelectorAll('.view-btn').forEach(btn => {
                btn.addEventListener('click', async () => {
                    const path = btn.getAttribute('data-path');
                    try {
                        const response = await fetch('/view_document', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ document_path: path })
                        });
                        const result = await response.json();

                        if (!response.ok) {
                            if (result.error.includes('hết lượt xem')) {
                                if (confirm('Bạn đã hết lượt xem. Bạn có muốn đổi lượt xem không?')) {
                                    window.location.href = '/view';
                                }
                            } else if (result.error.includes('đăng nhập')) {
                                window.location.href = '/index.html';
                            } else {
                                showError(result.error);
                            }
                            return;
                        }

                        window.open(result.document_path, '_blank');
                    } catch (error) {
                        showError('Không thể mở tài liệu: ' + error.message);
                    }
                });
            });

            document.querySelectorAll('.download-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const name = btn.getAttribute('data-name');               // ví dụ "de1.pdf"
    const path = btn.closest('tr').querySelector('.view-btn').dataset.path;

    try {
      // 1) Lấy link thật từ API xem
      const viewRes = await fetch('/view_document', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ document_path: path })
      });
      const viewData = await viewRes.json();

      if (!viewRes.ok) {
        // xử lý lỗi giống nút View
        if (viewData.error.includes('hết lượt xem') && confirm('Bạn đã hết lượt xem. Muốn đổi lượt xem không?')) {
          return window.location.href = '/view';
        }
        if (viewData.error.includes('đăng nhập')) {
          return window.location.href = '/index.html';
        }
        return showError(viewData.error || 'Không thể tải xuống tài liệu');
      }

      // 2) Fetch blob và download
      const fileRes = await fetch(viewData.document_path);
      const blob = await fileRes.blob();
      const url = URL.createObjectURL(blob);

      // --- xử lý thêm hậu tố vào filename ---
      const dotIndex = name.lastIndexOf('.');
      const base = dotIndex > -1 ? name.slice(0, dotIndex) : name;
      const ext  = dotIndex > -1 ? name.slice(dotIndex) : '';
      const newName = `${base}_dethihocphan.com${ext}`;  // ví dụ "de1_dethihocphan.com.pdf"

      const a = document.createElement('a');
      a.href = url;
      a.download = newName;
      document.body.appendChild(a);
      a.click();
      URL.revokeObjectURL(url);
      document.body.removeChild(a);
      // -----------------------------------------
    } catch (err) {
      showError('Không thể tải xuống: ' + err.message);
    }
  });
});


            document.querySelectorAll('.complaint-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const name = btn.getAttribute('data-name');
                    const modal = document.getElementById('complaintModal');
                    const examNameInput = document.getElementById('complaintExamName');
                    examNameInput.value = name;
                    modal.classList.add('active');
                });
            });

            document.querySelectorAll('.status-pending, .status-approved').forEach(status => {
                status.addEventListener('click', () => {
                    const examName = status.getAttribute('data-exam');
                    const complaint = complaints.find(c => c.examName === examName);
                    if (complaint) {
                        const modal = document.getElementById('complaintDetailModal');
                        const resolutionGroup = document.getElementById('resolutionGroup');
                        document.getElementById('detailExamName').textContent = complaint.examName;
                        document.getElementById('detailStatus').textContent = 
                            complaint.status === 'pending' ? 'Đang chờ' : 'Chấp thuận';
                        document.getElementById('detailReason').textContent = 
                            {
                                content_error: 'Nội dung sai sót',
                                file_corrupted: 'File bị lỗi',
                                wrong_file: 'File không đúng',
                                other: 'Khác'
                            }[complaint.reason] || complaint.reason;
                        document.getElementById('detailDetails').textContent = complaint.details;
                        
                        if (complaint.status === 'approved') {
                            resolutionGroup.style.display = 'block';
                            document.getElementById('detailResolution').textContent = complaint.resolution || 'Đã hoàn lại lượt xem';
                        } else {
                            resolutionGroup.style.display = 'block';
                            document.getElementById('detailResolution').textContent = 'Vui lòng đợi xử lý trong 24h';
                        }
                        
                        modal.classList.add('active');
                    }
                });
            });
        }

        function filterExams() {
            const searchQuery = document.getElementById('searchInput').value.toLowerCase();
            const fileType = document.getElementById('filterFileType').value;

            const filteredExams = viewedExams.filter(exam => {
                const matchesSearch = exam.name.toLowerCase().includes(searchQuery) ||
                    exam.type.toLowerCase().includes(searchQuery) ||
                    exam.subject_name.toLowerCase().includes(searchQuery) ||
                    exam.faculty_name.toLowerCase().includes(searchQuery) ||
                    exam.school_name.toLowerCase().includes(searchQuery);
                const matchesFileType = !fileType || exam.type.toLowerCase() === fileType;

                return matchesSearch && matchesFileType;
            });

            renderExamTable(filteredExams);
        }

document.addEventListener('DOMContentLoaded', () => {
    fetchViewedExams();

    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme); // Fixed line

    const activeThemeBtn = document.querySelector(`.theme-btn[data-theme="${savedTheme}"]`);
    if (activeThemeBtn) {
        // Ensure themeBtns is defined, e.g.:
        const themeBtns = document.querySelectorAll('.theme-btn');
        themeBtns.forEach(b => b.classList.remove('active'));
        activeThemeBtn.classList.add('active');
        
        const themeIcon = document.querySelector('.theme-icon i');
        themeIcon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
            const filterModal = document.getElementById('filterModal');
            const filterBtn = document.getElementById('filterBtn');
            const filterModalClose = document.getElementById('filterModalClose');
            const filterApplyBtn = document.getElementById('filterApplyBtn');
            const filterResetBtn = document.getElementById('filterResetBtn');

            filterBtn.addEventListener('click', () => {
                filterModal.classList.add('active');
            });

            filterModalClose.addEventListener('click', () => {
                filterModal.classList.remove('active');
            });

            filterApplyBtn.addEventListener('click', () => {
                filterModal.classList.remove('active');
                filterExams();
            });

            filterResetBtn.addEventListener('click', () => {
                document.getElementById('filterFileType').value = '';
                filterExams();
            });

            const complaintModal = document.getElementById('complaintModal');
            const complaintModalClose = document.getElementById('complaintModalClose');
            const complaintCancelBtn = document.getElementById('complaintCancelBtn');
            const complaintSubmitBtn = document.getElementById('complaintSubmitBtn');

            complaintModalClose.addEventListener('click', () => {
                complaintModal.classList.remove('active');
                resetComplaintForm();
            });

            complaintCancelBtn.addEventListener('click', () => {
                complaintModal.classList.remove('active');
                resetComplaintForm();
            });

            complaintSubmitBtn.addEventListener('click', () => {
                const examName = document.getElementById('complaintExamName').value;
                const reason = document.getElementById('complaintReason').value;
                const details = document.getElementById('complaintDetails').value;

                if (!reason) {
                    alert('Vui lòng chọn lý do khiếu nại');
                    return;
                }

                complaints.push({
                    examName,
                    status: 'pending',
                    reason,
                    details
                });

                complaintModal.classList.remove('active');
                resetComplaintForm();
                filterExams();
                alert('Khiếu nại đã được gửi!');
            });

            function resetComplaintForm() {
                document.getElementById('complaintExamName').value = '';
                document.getElementById('complaintReason').value = '';
                document.getElementById('complaintDetails').value = '';
            }

            const complaintDetailModal = document.getElementById('complaintDetailModal');
            const complaintDetailModalClose = document.getElementById('complaintDetailModalClose');
            const complaintDetailCloseBtn = document.getElementById('complaintDetailCloseBtn');

            complaintDetailModalClose.addEventListener('click', () => {
                complaintDetailModal.classList.remove('active');
            });

            complaintDetailCloseBtn.addEventListener('click', () => {
                complaintDetailModal.classList.remove('active');
            });

            document.getElementById('searchInput').addEventListener('input', filterExams);

            window.addEventListener('click', (e) => {
                if (e.target === filterModal) {
                    filterModal.classList.remove('active');
                }
                if (e.target === complaintModal) {
                    complaintModal.classList.remove('active');
                    resetComplaintForm();
                }
                if (e.target === complaintDetailModal) {
                    complaintDetailModal.classList.remove('active');
                }
            });
        });