        document.addEventListener('DOMContentLoaded', function() {
            const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
            const sidebar = document.querySelector('.sidebar');
            const modal = document.getElementById('announcementModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalMeta = document.getElementById('modalMeta');
            const modalBody = document.getElementById('modalBody');
            const modalClose = document.querySelector('.modal-close');
            const readMoreLinks = document.querySelectorAll('.read-more');

            // Announcement data
            const announcements = {
                1: {
    title: 'Cập nhật phiên bản 3.0.0',
    meta: '15/05/2025 | Nguyễn Ngọc Trường',
    body: `
        <p>Chúng tôi rất vui mừng thông báo phiên bản 3.0.0 của <strong>dethihocphan.com</strong> đã chính thức ra mắt với diện mạo hoàn toàn mới!</p>
        
        <h3>Có gì mới?</h3>
        <ul>
            <li><i class="fas fa-check-circle"></i> Giao diện được thiết kế lại hiện đại và trực quan hơn.</li>
            <li><i class="fas fa-check-circle"></i> Tối ưu hóa trải nghiệm người dùng trên cả máy tính và thiết bị di động.</li>
            <li><i class="fas fa-check-circle"></i> Tốc độ tải trang nhanh hơn, thao tác mượt mà hơn.</li>
        </ul>

        <p>Chúng tôi hy vọng giao diện mới sẽ mang đến cho bạn trải nghiệm sử dụng dễ dàng và thú vị hơn. Mọi góp ý xin vui lòng gửi về <a href="mailto:support@dethihocphan.com">support@dethihocphan.com</a>. Cảm ơn bạn đã đồng hành!</p>
    `
},

                2: {
                    title: 'Ra mắt tính năng quản lý thành viên mới',
                    meta: '10/05/2025 | Đội ngũ Bếp Chung',
                    body: `
                        <p>Chúng tôi tự hào giới thiệu tính năng quản lý thành viên hoàn toàn mới, giúp việc tổ chức nhóm trở nên dễ dàng và hiệu quả hơn bao giờ hết.</p>
                        <ul>
                            <li><i class="fas fa-check-circle"></i>Hỗ trợ tối đa 50 thành viên mỗi nhóm.</li>
                            <li><i class="fas fa-check-circle"></i>Giao diện trực quan để thêm, xóa, hoặc phân quyền thành viên.</li>
                            <li><i class="fas fa-check-circle"></i>Thông báo tự động khi có thay đổi trong danh sách thành viên.</li>
                        </ul>
                        <p>Hãy thử ngay và cho chúng tôi biết ý kiến của bạn qua mục "Trò chuyện"!</p>
                    `
                },
                3: {
                    title: 'Kế hoạch phát triển phiên bản 2.2.0',
                    meta: '01/05/2025 | Đội ngũ Bếp Chung',
                    body: `
                        <p>Chúng tôi đang nỗ lực để mang đến những cải tiến đột phá trong phiên bản 2.2.0, dự kiến ra mắt vào tháng 7/2025.</p>
                        <h3>Tính năng sắp ra mắt</h3>
                        <ul>
                            <li><i class="fas fa-check-circle"></i>Phân tích dinh dưỡng: Xem thông tin dinh dưỡng chi tiết cho mỗi món ăn trong thực đơn.</li>
                            <li><i class="fas fa-check-circle"></i>Dự đoán chi phí mua sắm: Sử dụng AI để ước tính chi phí dựa trên thực đơn và giá cả thị trường.</li>
                            <li><i class="fas fa-check-circle"></i>Tích hợp lịch cá nhân: Đồng bộ lịch nấu ăn với Google Calendar hoặc Outlook.</li>
                        </ul>
                        <p>Góp ý của bạn sẽ giúp chúng tôi hoàn thiện phiên bản này. Hãy gửi ý kiến qua support@bepchung.vn!</p>
                    `
                },
                4: {
                    title: 'Bảo trì hệ thống định kỳ',
                    meta: '25/04/2025 | Đội ngũ Bếp Chung',
                    body: `
                        <p>Để đảm bảo hiệu suất và trải nghiệm tốt nhất, chúng tôi sẽ tiến hành bảo trì hệ thống định kỳ.</p>
                        <ul>
                            <li><i class="fas fa-check-circle"></i>Thời gian: 01:00 - 03:00, 20/05/2025.</li>
                            <li><i class="fas fa-check-circle"></i>Nội dung: Nâng cấp máy chủ và tối ưu hóa cơ sở dữ liệu.</li>
                            <li><i class="fas fa-check-circle"></i>Ảnh hưởng: Hệ thống sẽ tạm ngưng trong khoảng thời gian trên.</li>
                        </ul>
                        <p>Xin lỗi vì bất kỳ sự bất tiện nào. Liên hệ support@bepchung.vn nếu bạn cần hỗ trợ.</p>
                    `
                }
            };


            // Modal handling
            readMoreLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const id = this.getAttribute('data-id');
                    const announcement = announcements[id];
                    
                    if (announcement) {
                        modalTitle.textContent = announcement.title;
                        modalMeta.textContent = announcement.meta;
                        modalBody.innerHTML = announcement.body;
                        modal.style.display = 'flex';
                    }
                });
            });

            modalClose.addEventListener('click', function() {
                modal.style.display = 'none';
            });

            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });

            // Close modal with Escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && modal.style.display === 'flex') {
                    modal.style.display = 'none';
                }
            });
        });
