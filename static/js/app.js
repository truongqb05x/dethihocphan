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
});
// check login
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch('/check-session', {
      method: 'GET',
      credentials: 'same-origin'
    });
    const data = await response.json();
    if (!data.loggedIn) {
      // Chưa login → chuyển đến trang login
      window.location.href = '/login';
    }
    // Nếu đã login, bạn có thể dùng data.user_id, data.username...
  } catch (err) {
    // Lỗi mạng hoặc server, cũng redirect để an toàn
    window.location.href = '/login';
  }
});

