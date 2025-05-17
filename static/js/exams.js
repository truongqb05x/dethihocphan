let currentPath = '/';
let currentSortColumn = 'name';
let sortDirection = 'asc';
let navigationHistory = [];
let currentSubjectId;
let pathNames = {}; // Lưu trữ ánh xạ ID-tên để hiển thị trong pathNavigation

// Hiển thị spinner tải
function showLoading() {
    const spinner = document.getElementById('loadingSpinner');
    const fileTableBody = document.getElementById('fileTableBody');
    if (spinner && fileTableBody) {
        spinner.style.display = 'block';
        fileTableBody.style.opacity = '0.3';
    }
}

// Ẩn spinner tải
function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    const fileTableBody = document.getElementById('fileTableBody');
    if (spinner && fileTableBody) {
        spinner.style.display = 'none';
        fileTableBody.style.opacity = '1';
    }
}

// Hiển thị thông báo lỗi
function showError(message) {
    const fileTableBody = document.getElementById('fileTableBody');
    fileTableBody.innerHTML = `
        <tr>
            <td colspan="4" style="text-align: center; padding: 2rem; color: var(--error);">
                <i class="fas fa-exclamation-circle" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                <p>${message}</p>
            </td>
        </tr>
    `;
}

// Tải danh sách trường với bộ lọc
function fetchSchools(filters = {}) {
    showLoading();
    fetch('/api/schools')
        .then(response => response.json())
        .then(schools => {
            let filteredSchools = schools;
            if (filters.schoolId) {
                filteredSchools = schools.filter(school => school.id.toString() === filters.schoolId);
            }
            renderItems(filteredSchools, 'school');
            updateFilterOptions('school', schools); // Cập nhật tùy chọn lọc
            schools.forEach(school => {
                pathNames[school.id] = school.name;
            });
            hideLoading();
        })
        .catch(error => {
            showError(`Không thể tải danh sách trường: ${error.message}`);
            hideLoading();
        });
}

// Tải danh sách khoa với bộ lọc
function fetchFaculties(schoolId, filters = {}) {
    if (!schoolId || isNaN(schoolId)) {
        showError(`ID trường không hợp lệ: ${schoolId}`);
        hideLoading();
        return;
    }
    showLoading();
    fetch(`/api/faculties?school_id=${schoolId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: Không thể tải danh sách khoa`);
            }
            return response.json();
        })
        .then(faculties => {
            let filteredFaculties = faculties;
            if (filters.facultyId) {
                filteredFaculties = faculties.filter(faculty => faculty.id.toString() === filters.facultyId);
            }
            renderItems(filteredFaculties, 'faculty');
            updateFilterOptions('faculty', faculties);
            faculties.forEach(faculty => {
                pathNames[faculty.id] = faculty.name;
            });
            hideLoading();
        })
        .catch(error => {
            showError(`Không thể tải danh sách khoa: ${error.message}`);
            hideLoading();
        });
}

// Tải danh sách môn học với bộ lọc
function fetchSubjects(facultyId, filters = {}) {
    if (!facultyId || isNaN(facultyId)) {
        showError(`ID khoa không hợp lệ: ${facultyId}`);
        hideLoading();
        return;
    }
    showLoading();
    fetch(`/api/subjects?faculty_id=${facultyId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: Không thể tải danh sách môn học`);
            }
            return response.json();
        })
        .then(subjects => {
            let filteredSubjects = subjects;
            if (filters.subjectId) {
                filteredSubjects = subjects.filter(subject => subject.id.toString() === filters.subjectId);
            }
            renderItems(filteredSubjects, 'subject');
            updateFilterOptions('subject', subjects);
            subjects.forEach(subject => {
                pathNames[subject.id] = subject.name;
            });
            hideLoading();
        })
        .catch(error => {
            showError(`Không thể tải danh sách môn học: ${error.message}`);
            hideLoading();
        });
}

// Tải danh sách năm với bộ lọc
function fetchYears(subjectId, filters = {}) {
    if (!subjectId || isNaN(subjectId)) {
        showError(`ID môn học không hợp lệ: ${subjectId}`);
        hideLoading();
        return;
    }
    showLoading();
    currentSubjectId = subjectId;
    fetch(`/api/years?subject_id=${subjectId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: Không thể tải danh sách năm`);
            }
            return response.json();
        })
        .then(years => {
            let filteredYears = years;
            if (filters.years && filters.years.length > 0) {
                filteredYears = years.filter(year => filters.years.includes(year.year));
            }
            renderItems(filteredYears, 'year');
            updateFilterOptions('year', years);
            hideLoading();
        })
        .catch(error => {
            showError(`Không thể tải danh sách năm: ${error.message}`);
            hideLoading();
        });
}

// Tải danh sách tài liệu với bộ lọc
function fetchDocuments(subjectId, year, filters = {}) {
    if (!subjectId || isNaN(subjectId) || !year) {
        showError(`Thiếu thông tin môn học hoặc năm: subjectId=${subjectId}, year=${year}`);
        hideLoading();
        return;
    }
    showLoading();
    fetch(`/api/documents?subject_id=${subjectId}&year=${year}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: Không thể tải danh sách tài liệu`);
            }
            return response.json();
        })
        .then(documents => {
            let filteredDocuments = documents;
            if (filters.years && filters.years.length > 0) {
                filteredDocuments = documents.filter(doc => filters.years.includes(doc.year));
            }
            renderItems(filteredDocuments, 'document');
            hideLoading();
        })
        .catch(error => {
            showError(`Không thể tải danh sách tài liệu: ${error.message}`);
            hideLoading();
        });
}

// Cập nhật đường dẫn điều hướng
function renderPathNavigation(path) {
    const pathNavigation = document.getElementById('pathNavigation');
    pathNavigation.innerHTML = '';

    const rootItem = document.createElement('div');
    rootItem.className = 'path-item';
    rootItem.innerHTML = `<a href="#" data-path="/" data-type="school"><i class="fas fa-home"></i> Thư viện</a>`;
    pathNavigation.appendChild(rootItem);

    const parts = path.split('/').filter(part => part);
    let currentPath = '';
    let type = 'school';

    for (let i = 0; i < parts.length; i++) {
        const separator = document.createElement('div');
        separator.className = 'path-separator';
        separator.textContent = '/';
        pathNavigation.appendChild(separator);

        currentPath += `/${parts[i]}`;
        const partItem = document.createElement('div');
        partItem.className = 'path-item';

        if (i === 0) type = 'faculty';
        else if (i === 1) type = 'subject';
        else if (i === 2) type = 'year';
        else if (i === 3) type = 'document';

        const displayName = type === 'year' || type === 'document' ? decodeURIComponent(parts[i]) : (pathNames[parts[i]] || decodeURIComponent(parts[i]));

        if (i === parts.length - 1) {
            partItem.innerHTML = `<span data-path="${currentPath}" data-type="${type}">${displayName}</span>`;
        } else {
            partItem.innerHTML = `<a href="#" data-path="${currentPath}" data-type="${type}">${displayName}</a>`;
        }

        pathNavigation.appendChild(partItem);
    }

    document.querySelectorAll('.path-navigation a, .path-navigation span').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const path = this.getAttribute('data-path');
            const type = this.getAttribute('data-type');
            navigateToPath(path, type);
        });
    });
}

// Điều hướng đến đường dẫn và tải nội dung
function navigateToPath(path, type, filters = {}) {
    const parts = path.split('/').filter(part => part);
    console.log('Navigating to:', { path, type, parts, filters });
    if (type === 'school' || path === '/') {
        fetchSchools(filters);
    } else if (type === 'faculty') {
        const schoolId = parts[0];
        fetchFaculties(schoolId, filters);
    } else if (type === 'subject') {
        const facultyId = parts[1];
        fetchSubjects(facultyId, filters);
    } else if (type === 'year') {
        const subjectId = parts[1];
        fetchYears(subjectId, filters);
    } else if (type === 'document') {
        const subjectId = parts[1];
        const year = parts[2];
        fetchDocuments(subjectId, year, filters);
    }
    navigateTo(path);
}

// Render danh sách mục
function renderItems(items, type) {
    const fileTableBody = document.getElementById('fileTableBody');
    fileTableBody.innerHTML = '';

    if (currentPath !== '/' && items.length > 0) {
        const parentPath = getParentPath(currentPath);
        const parentRow = document.createElement('tr');
        parentRow.innerHTML = `
            <td>
                <div style="display: flex; align-items: center;">
                    <i class="fas fa-folder-open file-icon" style="color: #54aeff;"></i>
                    <a href="#" class="file-name" data-path="${parentPath}" data-type="parent">..</a>
                </div>
            </td>
            <td class="file-meta">Thư mục</td>
            <td class="file-meta">-</td>
            <td class="file-meta">-</td>
        `;
        fileTableBody.appendChild(parentRow);
    }

    const sortedItems = sortItems(items);

    sortedItems.forEach(item => {
        const row = document.createElement('tr');
        let icon = '';
        let itemType = '';
        let name, path, id, year, size, updated;

        if (['school', 'faculty', 'subject'].includes(type)) {
            icon = '<i class="fas fa-folder file-icon" style="color: #54aeff;"></i>';
            itemType = 'Thư mục';
            name = item.name;
            path = `${currentPath}/${item.id}`;
            id = item.id || '';
            year = '';
            size = item.total_size || '0 KB';
            updated = item.latest_updated ? new Date(item.latest_updated).toLocaleDateString('vi-VN') : '-';
        } else if (type === 'year') {
            icon = '<i class="fas fa-folder file-icon" style="color: #54aeff;"></i>';
            itemType = 'Thư mục';
            name = item.year;
            path = `${currentPath}/${encodeURIComponent(item.year)}`;
            id = currentSubjectId || '';
            year = item.year;
            size = item.total_size || '0 KB';
            updated = item.latest_updated ? new Date(item.latest_updated).toLocaleDateString('vi-VN') : '-';
        } else if (type === 'document') {
            const extension = item.file_name?.split('.').pop()?.toLowerCase();
            switch (extension) {
                case 'pdf':
                    icon = '<i class="fas fa-file-pdf file-icon" style="color: #e34c26;"></i>';
                    itemType = 'PDF';
                    break;
                case 'doc':
                case 'docx':
                    icon = '<i class="fas fa-file-word file-icon" style="color: #2b579a;"></i>';
                    itemType = 'Word';
                    break;
                case 'xls':
                case 'xlsx':
                    icon = '<i class="fas fa-file-excel file-icon" style="color: #217346;"></i>';
                    itemType = 'Excel';
                    break;
                case 'ppt':
                case 'pptx':
                    icon = '<i class="fas fa-file-powerpoint file-icon" style="color: #d24726;"></i>';
                    itemType = 'PowerPoint';
                    break;
                case 'jpg':
                case 'jpeg':
                case 'png':
                case 'gif':
                    icon = '<i class="fas fa-file-image file-icon" style="color: #f1c40f;"></i>';
                    itemType = 'Hình ảnh';
                    break;
                case 'zip':
                case 'rar':
                    icon = '<i class="fas fa-file-archive file-icon" style="color: #e67e22;"></i>';
                    itemType = 'Nén';
                    break;
                default:
                    icon = '<i class="fas fa-file file-icon" style="color: var(--text-light);"></i>';
                    itemType = item.document_type ? item.document_type.charAt(0).toUpperCase() + item.document_type.slice(1) : 'Tài liệu';
            }
            name = item.file_name;
            path = item.file_path;
            id = item.id || '';
            year = item.year || '';
            size = item.file_size || '0 KB';
            updated = item.created_at || '-';
        }

        row.innerHTML = `
            <td>
                <div style="display: flex; align-items: center;">
                    ${icon}
                    <a href="#" class="file-name" data-path="${path}" data-type="${type}" 
                       data-id="${id}" data-year="${year}">${name}</a>
                </div>
            </td>
            <td class="file-meta">${itemType}</td>
            <td class="file-meta">${size}</td>
            <td class="file-meta">${updated}</td>
        `;
        fileTableBody.appendChild(row);
    });

    addItemClickEvents();
}

// Sắp xếp danh sách mục
function sortItems(items) {
    return [...items].sort((a, b) => {
        let valueA, valueB;
        switch(currentSortColumn) {
            case 'name':
                valueA = typeof a === 'string' ? a.toLowerCase() : (a.name || a.file_name || a.year || '').toLowerCase();
                valueB = typeof b === 'string' ? b.toLowerCase() : (b.name || b.file_name || b.year || '').toLowerCase();
                break;
            case 'type':
                valueA = a.type || (typeof a === 'string' ? 'Thư mục' : a.document_type || '');
                valueB = b.type || (typeof b === 'string' ? 'Thư mục' : a.document_type || '');
                break;
            case 'size':
                valueA = parseFileSize(a.total_size || a.file_size || '0 KB');
                valueB = parseFileSize(b.total_size || b.file_size || '0 KB');
                break;
            case 'updated':
                if (typeof a === 'object' && (a.latest_updated || a.created_at)) {
                    valueA = new Date(a.latest_updated || a.created_at || '2000-01-01');
                } else {
                    valueA = new Date('2000-01-01');
                }
                if (typeof b === 'object' && (b.latest_updated || b.created_at)) {
                    valueB = new Date(b.latest_updated || b.created_at || '2000-01-01');
                } else {
                    valueB = new Date('2000-01-01');
                }
                break;
            default:
                valueA = typeof a === 'string' ? a.toLowerCase() : (a.name || a.file_name || a.year || '').toLowerCase();
                valueB = typeof b === 'string' ? b.toLowerCase() : (b.name || b.file_name || b.year || '').toLowerCase();
        }
        return (valueA < valueB ? -1 : 1) * (sortDirection === 'asc' ? 1 : -1);
    });
}

// Chuyển đổi kích thước file
function parseFileSize(size) {
    if (!size || size === '0 KB' || size === '-') return 0;
    const units = { 'KB': 1, 'MB': 2, 'GB': 3, 'B': 0 };
    const [number, unit] = size.split(' ');
    return parseFloat(number) * Math.pow(1024, units[unit] || 0);
}

// Lấy đường dẫn thư mục cha
function getParentPath(path) {
    const parts = path.split('/').filter(part => part);
    parts.pop();
    return parts.length ? `/${parts.join('/')}` : '/';
}

// Thêm sự kiện click cho các mục
function addItemClickEvents() {
    document.querySelectorAll('.file-name').forEach(link => {
        link.addEventListener('click', async function(e) {
            e.preventDefault();
            const path = this.getAttribute('data-path');
            const type = this.getAttribute('data-type');
            const id = this.getAttribute('data-id');
            const year = this.getAttribute('data-year');

            console.log('Item clicked:', { path, type, id, year });

            if (type === 'parent') {
                const parts = path.split('/').filter(part => part);
                if (parts.length === 0) {
                    fetchSchools();
                } else if (parts.length === 1) {
                    fetchFaculties(parts[0]);
                } else if (parts.length === 2) {
                    fetchSubjects(parts[1]);
                } else if (parts.length === 3) {
                    fetchYears(parts[2]);
                }
                navigateTo(path);
            } else if (type === 'school') {
                fetchFaculties(id);
                navigateTo(path);
            } else if (type === 'faculty') {
                fetchSubjects(id);
                navigateTo(path);
            } else if (type === 'subject') {
                fetchYears(id);
                navigateTo(path);
            } else if (type === 'year') {
                if (!id || isNaN(id)) {
                    showError(`ID môn học không hợp lệ: ${id}`);
                    return;
                }
                fetchDocuments(id, year);
                navigateTo(path);
            } else if (type === 'document') {
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
                                window.location.href = '/quydoi';
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
                    showError(`Không thể mở tài liệu: ${error.message}`);
                }
            }
        });
    });
}

// Cập nhật tùy chọn bộ lọc
function updateFilterOptions(type, items) {
    const elements = {
        school: document.getElementById('filterSchool'),
        faculty: document.getElementById('filterFaculty'),
        subject: document.getElementById('filterSubject'),
        year: document.getElementById('filterYears')
    };
    
    if (type === 'year') {
        elements[type].innerHTML = items.map(item => `
            <label class="filter-option">
                <input type="checkbox" value="${item.year}" checked> ${item.year}
            </label>
        `).join('');
    } else {
        elements[type].innerHTML = `<option value="">Tất cả ${type}</option>` + 
            items.map(item => `<option value="${item.id}">${item.name}</option>`).join('');
    }
}

// Điều hướng đến đường dẫn
function navigateTo(path) {
    currentPath = path;
    navigationHistory.push(path);
    renderPathNavigation(path);
    updateSortIndicator();
}

// Cập nhật chỉ báo sắp xếp
function updateSortIndicator() {
    document.querySelectorAll('.sortable').forEach(th => {
        th.classList.remove('asc', 'desc');
        if (th.getAttribute('data-sort') === currentSortColumn) {
            th.classList.add(sortDirection);
        }
    });
}

// Hàm debounce để giới hạn tần suất gọi hàm
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Sự kiện chính khi tải trang
document.addEventListener('DOMContentLoaded', function() {
    fetchSchools();
    renderPathNavigation(currentPath);

    document.querySelectorAll('.sortable').forEach(th => {
        th.addEventListener('click', function() {
            const column = this.getAttribute('data-sort');
            if (currentSortColumn === column) {
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                currentSortColumn = column;
                sortDirection = 'asc';
            }
            const parts = currentPath.split('/').filter(part => part);
            if (parts.length === 0) {
                fetchSchools();
            } else if (parts.length === 1) {
                fetchFaculties(parts[0]);
            } else if (parts.length === 2) {
                fetchSubjects(parts[1]);
            } else if (parts.length === 3) {
                fetchYears(parts[2]);
            } else if (parts.length >= 4) {
                fetchDocuments(parts[1], parts[2]);
            }
        });
    });

    const filterModal = document.getElementById('filterModal');
    const filterModalBtn = document.getElementById('filterModalBtn');
    const filterModalClose = document.getElementById('filterModalClose');
    const filterApplyBtn = document.getElementById('filterApplyBtn');
    const filterResetBtn = document.getElementById('filterResetBtn');

    filterModalBtn.addEventListener('click', () => filterModal.classList.add('active'));
    filterModalClose.addEventListener('click', () => filterModal.classList.remove('active'));

    filterApplyBtn.addEventListener('click', () => {
        filterModal.classList.remove('active');

        // Thu thập giá trị bộ lọc
        const filters = {
            schoolId: document.getElementById('filterSchool').value,
            facultyId: document.getElementById('filterFaculty').value,
            subjectId: document.getElementById('filterSubject').value,
            years: Array.from(document.querySelectorAll('#filterYears input[type="checkbox"]:checked')).map(cb => cb.value)
        };

        console.log('Applying filters:', filters);

        // Xác định cấp hiện tại từ currentPath
        const parts = currentPath.split('/').filter(part => part);
        const type = parts.length === 0 ? 'school' :
                     parts.length === 1 ? 'faculty' :
                     parts.length === 2 ? 'subject' :
                     parts.length === 3 ? 'year' : 'document';

        // Gọi hàm fetch tương ứng với bộ lọc
        if (type === 'school') {
            fetchSchools(filters);
        } else if (type === 'faculty') {
            fetchFaculties(parts[0], filters);
        } else if (type === 'subject') {
            fetchSubjects(parts[1], filters);
        } else if (type === 'year') {
            fetchYears(parts[1], filters);
        } else if (type === 'document') {
            fetchDocuments(parts[1], parts[2], filters);
        }
    });

    filterResetBtn.addEventListener('click', () => {
        document.querySelectorAll('#filterModal input[type="checkbox"]').forEach(cb => cb.checked = true);
        document.querySelectorAll('#filterModal select').forEach(select => select.selectedIndex = 0);
        // Tải lại danh sách không có bộ lọc
        const parts = currentPath.split('/').filter(part => part);
        if (parts.length === 0) {
            fetchSchools();
        } else if (parts.length === 1) {
            fetchFaculties(parts[0]);
        } else if (parts.length === 2) {
            fetchSubjects(parts[1]);
        } else if (parts.length === 3) {
            fetchYears(parts[1]);
        } else if (parts.length >= 4) {
            fetchDocuments(parts[1], parts[2]);
        }
    });

    const searchModal = document.getElementById('searchModal');
    const searchModalBtn = document.getElementById('searchModalBtn');
    const searchModalClose = document.getElementById('searchModalClose');
    const searchCancelBtn = document.getElementById('searchCancelBtn');
    const searchSubmitBtn = document.getElementById('searchSubmitBtn');
    const searchInput = document.getElementById('searchInput');
    const searchDocumentType = document.getElementById('searchDocumentType');
    const searchResults = document.getElementById('searchResults');
    const searchPlaceholder = document.getElementById('searchPlaceholder');
    const searchLoading = document.getElementById('searchLoading');
    const searchResultContent = document.getElementById('searchResultContent');

    searchModalBtn.addEventListener('click', () => {
        searchModal.classList.add('active');
        searchInput.focus();
    });
    searchModalClose.addEventListener('click', () => {
        searchModal.classList.remove('active');
        resetSearch();
    });
    searchCancelBtn.addEventListener('click', () => {
        searchModal.classList.remove('active');
        resetSearch();
    });
    searchSubmitBtn.addEventListener('click', performSearch);

    // Gắn sự kiện input với debounce
    const debouncedSearch = debounce(performSearch, 300);
    searchInput.addEventListener('input', () => {
        debouncedSearch();
    });

    function performSearch() {
        const query = searchInput.value.trim();
        const documentType = searchDocumentType.value;

        if (!query) {
            searchPlaceholder.style.display = 'block';
            searchResultContent.style.display = 'none';
            searchLoading.style.display = 'none';
            searchResultContent.innerHTML = '';
            return;
        }

        searchPlaceholder.style.display = 'none';
        searchResultContent.style.display = 'none';
        searchLoading.style.display = 'block';

        const searchParams = new URLSearchParams();
        searchParams.append('keyword', query);
        if (documentType) {
            searchParams.append('document_type', documentType);
        }

        fetch(`/api/documents?${searchParams.toString()}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: Không thể tải kết quả tìm kiếm`);
                }
                return response.json();
            })
            .then(documents => {
                searchLoading.style.display = 'none';
                searchResultContent.style.display = 'block';

                if (documents.length === 0) {
                    searchResultContent.innerHTML = '<p style="color: var(--text-light); text-align: center;">Không tìm thấy tài liệu nào</p>';
                    return;
                }

                const keywords = query.toLowerCase().split(/\s+/);

                searchResultContent.innerHTML = documents.map(doc => {
                    let highlightedName = doc.file_name;
                    keywords.forEach(kw => {
                        const regex = new RegExp(`(${kw})`, 'gi');
                        highlightedName = highlightedName.replace(regex, '<span style="background-color: #FFFF99; font-weight: 600;">$1</span>');
                    });

                    return `
                        <div style="padding: 0.75rem; border-bottom: 1px solid var(--border);">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <i class="fas fa-file-pdf file-icon" style="color: #e34c26;"></i>
                                <a href="#" class="file-name" data-path="${doc.file_path}" data-type="document">${highlightedName}</a>
                            </div>
                            <div style="font-size: 0.85rem; color: var(--text-light); margin-top: 0.25rem;">
                                <span>${doc.document_type === 'exam' ? 'Đề thi' : 'Đề cương'}</span> • 
                                <span>${doc.year}</span> • 
                                <span>${doc.file_size}</span> • 
                                <span>${doc.created_at}</span>
                            </div>
                            <div style="font-size: 0.85rem; color: var(--text-lighter);">
                                ${doc.school_name} > ${doc.faculty_name} > ${doc.subject_name}
                            </div>
                        </div>
                    `;
                }).join('');

                document.querySelectorAll('#searchResultContent .file-name').forEach(link => {
                    link.addEventListener('click', async function(e) {
                        e.preventDefault();
                        const path = this.getAttribute('data-path');
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
                                        window.location.href = '/quydoi';
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
                            showError(`Không thể mở tài liệu: ${error.message}`);
                        }
                    });
                });
            })
            .catch(error => {
                searchLoading.style.display = 'none';
                searchResultContent.style.display = 'block';
                searchResultContent.innerHTML = `<p style="color: var(--error); text-align: center;">${error.message}</p>`;
            });
    }

    function resetSearch() {
        searchInput.value = '';
        searchDocumentType.value = '';
        searchPlaceholder.style.display = 'block';
        searchLoading.style.display = 'none';
        searchResultContent.style.display = 'none';
        searchResultContent.innerHTML = '';
    }

    window.addEventListener('click', (e) => {
        if ([filterModal, searchModal].includes(e.target)) {
            e.target.classList.remove('active');
            if (e.target === searchModal) resetSearch();
        }
    });
});