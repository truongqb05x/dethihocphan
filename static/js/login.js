document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const elements = {
        form: document.getElementById('authForm'),
        username: document.getElementById('username'),
        password: document.getElementById('password'),
        confirmPassword: document.getElementById('confirmPassword'),
        confirmPasswordGroup: document.getElementById('confirmPasswordGroup'),
        togglePassword: document.getElementById('togglePassword'),
        toggleConfirmPassword: document.getElementById('toggleConfirmPassword'),
        usernameError: document.getElementById('username-error'),
        passwordError: document.getElementById('password-error'),
        confirmPasswordError: document.getElementById('confirmPassword-error'),
        authButton: document.getElementById('authButton'),
        themeToggle: document.getElementById('themeToggle'),
        toggleAuth: document.getElementById('toggleAuth'),
        formTitle: document.getElementById('formTitle'),
        formSubtitle: document.getElementById('formSubtitle'),
        toggleText: document.getElementById('toggleText'),
        serverError: document.getElementById('serverError')
    };

    // State
    let isLoginMode = true;

    // Validation rules
    const validators = {
        username: (value) => {
            if (value.trim() === '') {
                elements.usernameError.textContent = 'Vui lòng nhập tên đăng nhập';
                    return false;
            }
            return true;
        },
        password: (value) => {
            if (value === '') {
                elements.passwordError.textContent = 'Vui lòng nhập mật khẩu';
                return false;
            }
            return true;
        },
        confirmPassword: (value, password) => {
            if (value !== password) {
                elements.confirmPasswordError.textContent = 'Mật khẩu không khớp';
                return false;
            }
            return true;
        }
    };

    // Show/hide error messages
    const showError = (element, errorElement, show) => {
        errorElement.style.display = show ? 'block' : 'none';
        element.classList[show ? 'add' : 'remove']('error');
    };

    // Validate field
    const validateField = (field, errorElement, validator, compareValue = null) => {
        const isValid = compareValue ? validator(field.value, compareValue) : validator(field.value);
        showError(field, errorElement, !isValid);
        return isValid;
    };

    // Show server error
    const showServerError = (message) => {
        elements.serverError.textContent = message;
        elements.serverError.style.display = 'block';
        setTimeout(() => {
            elements.serverError.style.display = 'none';
        }, 5000);
    };

    // Toggle password visibility
    const togglePasswordVisibility = (input, toggle) => {
        toggle.addEventListener('click', () => {
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            toggle.classList.toggle('fa-eye-slash');
            toggle.classList.toggle('fa-eye');
        });
    };

    // API request
    const sendAuthRequest = async (endpoint, data) => {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || 'Đã có lỗi xảy ra');
        }
        return result;
    } catch (error) {
        throw error;
    }
};


    // Handle authentication
const handleAuth = async () => {
    elements.authButton.disabled = true;
    elements.authButton.classList.add('btn-loading');
    try {
        const data = {
            username: elements.username.value.trim(),
            password: elements.password.value
        };
        if (!isLoginMode) {
            data.confirmPassword = elements.confirmPassword.value;
        }
        const endpoint = isLoginMode ? '/login' : '/register';
        const result = await sendAuthRequest(endpoint, data);

        elements.authButton.disabled = false;
        elements.authButton.classList.remove('btn-loading');
        alert(result.message);

        if (isLoginMode) {
            // Nếu là login, redirect về trang chính
            window.location.href = '/';
        } else {
            // Nếu là register, chuyển sang form login
            toggleAuthMode();
            // Có thể focus vào ô username để UX tốt hơn
            elements.username.focus();
        }
    } catch (error) {
        elements.authButton.disabled = false;
        elements.authButton.classList.remove('btn-loading');
        showServerError(error.message);
    }
};


    // Theme toggle
    const toggleTheme = () => {
        const currentTheme = document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.body.setAttribute('data-theme', currentTheme);
        localStorage.setItem('theme', currentTheme);
        elements.themeToggle.innerHTML = `<i class="fas fa-${currentTheme === 'dark' ? 'sun' : 'moon'}"></i>`;
    };

    // Initialize theme
    const initTheme = () => {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.body.setAttribute('data-theme', savedTheme);
        elements.themeToggle.innerHTML = `<i class="fas fa-${savedTheme === 'dark' ? 'sun' : 'moon'}"></i>`;
    };

    // Toggle between login and register
    const toggleAuthMode = () => {
        isLoginMode = !isLoginMode;
        elements.formTitle.textContent = isLoginMode ? 'Đăng nhập hệ thống' : 'Đăng ký tài khoản';
        elements.formSubtitle.textContent = isLoginMode ? 'Vui lòng nhập thông tin tài khoản của bạn' : 'Tạo tài khoản mới để bắt đầu';
        elements.authButton.innerHTML = `<i class="fas fa-${isLoginMode ? 'sign-in-alt' : 'user-plus'}" style="margin-right: 8px;"></i> ${isLoginMode ? 'Đăng nhập' : 'Đăng ký'}`;
        elements.toggleText.innerHTML = isLoginMode ? 
            'Chưa có tài khoản? <a href="#" class="login-link" id="toggleAuth">Đăng ký ngay</a>' : 
            'Đã có tài khoản? <a href="#" class="login-link" id="toggleAuth">Đăng nhập ngay</a>';
        elements.confirmPasswordGroup.style.display = isLoginMode ? 'none' : 'block';
        elements.form.reset();
        [elements.usernameError, elements.passwordError, elements.confirmPasswordError, elements.serverError].forEach(el => el.style.display = 'none');
        [elements.username, elements.password, elements.confirmPassword].forEach(el => el.classList.remove('error'));
        
        // Reattach toggle event to new link
        const newToggle = document.getElementById('toggleAuth');
        newToggle.addEventListener('click', (e) => {
            e.preventDefault();
            toggleAuthMode();
        });
    };

    // Real-time validation
    elements.username.addEventListener('input', () => validateField(elements.username, elements.usernameError, validators.username));
    elements.password.addEventListener('input', () => {
        validateField(elements.password, elements.passwordError, validators.password);
        if (!isLoginMode) {
            validateField(elements.confirmPassword, elements.confirmPasswordError, validators.confirmPassword, elements.password.value);
        }
    });
    elements.confirmPassword.addEventListener('input', () => 
        validateField(elements.confirmPassword, elements.confirmPasswordError, validators.confirmPassword, elements.password.value));

    // Form submission
    elements.form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const isUsernameValid = validateField(elements.username, elements.usernameError, validators.username);
        const isPasswordValid = validateField(elements.password, elements.passwordError, validators.password);
        let isConfirmPasswordValid = true;

        if (!isLoginMode) {
            isConfirmPasswordValid = validateField(elements.confirmPassword, elements.confirmPasswordError, validators.confirmPassword, elements.password.value);
        }

        if (isUsernameValid && isPasswordValid && isConfirmPasswordValid) {
            await handleAuth();
        }
    });

    // Initialize
    togglePasswordVisibility(elements.password, elements.togglePassword);
    togglePasswordVisibility(elements.confirmPassword, elements.toggleConfirmPassword);
    elements.toggleAuth.addEventListener('click', (e) => {
        e.preventDefault();
        toggleAuthMode();
    });
    elements.themeToggle.addEventListener('click', toggleTheme);
    initTheme();
});
