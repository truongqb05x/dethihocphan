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


// mở ads
(function() {
  var url = 'https://www.profitableratecpm.com/ircmb2h62j?key=4edd137a108f62b6443ab2704692e9b6';
  var storageKey = 'redirectTarget';
  var waitingKey = 'waitingForClick';
  var countdownInterval;

  // Hiển thị hộp thông báo tùy chỉnh với nút OK, sau đó callback()
  function showCustomNotice(callback) {
    var overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.background = 'rgba(0,0,0,0.5)';
    overlay.style.zIndex = '9999';
    overlay.innerHTML = `
      <div style="
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        background: #fff;
        padding: 20px;
        border-radius: 4px;
        max-width: 300px;
        text-align: center;
        font-family: sans-serif;
      ">
        <p>Nhằm mục đích duy trì trang web, chúng tôi sẽ mở một tab quảng cáo.<br>
        Bạn đừng quan tâm nó, có thể đóng lại ngay khi mở.</p>
        <button id="rr_ok_btn" style="
          margin-top: 12px;
          padding: 6px 12px;
          cursor: pointer;
        ">OK</button>
      </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector('#rr_ok_btn').addEventListener('click', function() {
      document.body.removeChild(overlay);
      callback();
    }, { once: true });
  }

  function startCycle() {
    if (localStorage.getItem(waitingKey) === 'true') {
      console.log('[Redirect Timer] Đang đợi click, không đếm lại.');
      listenOnceForClick();
      return;
    }

    var target = parseInt(localStorage.getItem(storageKey), 10);
    if (isNaN(target) || target <= Date.now()) {
      var seconds = Math.floor(Math.random() * 60) + 1;
      target = Date.now() + seconds * 1000;
      localStorage.setItem(storageKey, target);
      console.log('[Redirect Timer] Tạo chu kỳ mới, đếm ngẫu nhiên ' + seconds + ' giây');
    } else {
      var remaining = Math.ceil((target - Date.now()) / 1000);
      console.log('[Redirect Timer] Tiếp tục chu kỳ cũ, còn lại ' + remaining + ' giây');
    }

    if (countdownInterval) clearInterval(countdownInterval);

    countdownInterval = setInterval(function() {
      var now = Date.now();
      var diff = target - now;
      if (diff <= 0) {
        clearInterval(countdownInterval);
        console.log('[Redirect Timer] Hết thời gian, sẵn sàng lắng nghe click.');
        localStorage.setItem(waitingKey, 'true');
        listenOnceForClick();
      } else {
        console.log('[Redirect Timer] Còn lại ' + Math.ceil(diff / 1000) + ' giây');
      }
    }, 1000);
  }

  function listenOnceForClick() {
    document.addEventListener('click', function handler(event) {
      if (localStorage.getItem(waitingKey) !== 'true') return;

      document.removeEventListener('click', handler);
      localStorage.removeItem(waitingKey);
      console.log('[Redirect Timer] Đã click tại:', event.pageX, event.pageY);

      // Thay alert bằng custom notice
      showCustomNotice(function() {
        // Mở quảng cáo sau khi user nhấn OK
        var a = document.createElement('a');
        a.href = url;
        a.target = '_blank';
        a.style.display = 'none';
        document.body.appendChild(a);
        console.log('[Redirect Timer] Mở link:', url);
        a.click();
        document.body.removeChild(a);
        console.log('[Redirect Timer] Đã dọn thẻ <a>.');

        // Reset chu kỳ
        localStorage.removeItem(storageKey);
        startCycle();
      });

    }, { once: true });
  }

  // Khởi động
  startCycle();
})();
