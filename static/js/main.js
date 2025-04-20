/**
 * 信息管理系统主JavaScript文件
 */

// DOM 加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    
    // 添加页面过渡动画
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
    
    // 自动关闭提示信息
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // 确认删除
    const deleteButtons = document.querySelectorAll('.delete-btn');
    if (deleteButtons) {
        deleteButtons.forEach(function(button) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                const url = this.getAttribute('href');
                
                Swal.fire({
                    title: '确定要删除吗？',
                    text: "删除后数据将无法恢复！",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#ef476f',
                    cancelButtonColor: '#6c757d',
                    confirmButtonText: '是，删除!',
                    cancelButtonText: '取消'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = url;
                    }
                });
            });
        });
    }
    
    // 表格行点击效果
    const tableRows = document.querySelectorAll('tbody tr');
    if (tableRows) {
        tableRows.forEach(function(row) {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function(e) {
                // 如果点击的不是按钮区域
                if (!e.target.closest('.btn') && !e.target.closest('.btn-group')) {
                    // 找到当前行中的查看按钮并触发点击
                    const viewBtn = this.querySelector('.view-btn');
                    if (viewBtn) {
                        viewBtn.click();
                    }
                }
            });
            
            // 添加鼠标悬停效果
            row.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.transform = '';
                this.style.boxShadow = '';
            });
        });
    }
    
    // 输入验证
    const forms = document.querySelectorAll('form');
    if (forms) {
        forms.forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                
                form.classList.add('was-validated');
            }, false);
        });
    }
    
    // 为表单输入框添加焦点动画
    const formControls = document.querySelectorAll('.form-control, .form-select');
    if (formControls) {
        formControls.forEach(function(control) {
            control.addEventListener('focus', function() {
                const inputGroup = this.closest('.input-group');
                if (inputGroup) {
                    inputGroup.style.boxShadow = '0 0 0 3px rgba(67, 97, 238, 0.15)';
                    inputGroup.style.borderColor = '#4361ee';
                }
            });
            
            control.addEventListener('blur', function() {
                const inputGroup = this.closest('.input-group');
                if (inputGroup) {
                    inputGroup.style.boxShadow = '';
                    inputGroup.style.borderColor = '';
                }
            });
        });
    }
    
    // 仪表板表格中的徽章添加悬停效果
    const badges = document.querySelectorAll('.badge');
    if (badges) {
        badges.forEach(function(badge) {
            badge.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.1)';
            });
            
            badge.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        });
    }
    
    // 监听主题切换 (基于用户系统设置)
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)');
    
    function updateTheme(e) {
        if (e.matches) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    }
    
    // 设置初始主题
    updateTheme(prefersDarkMode);
    
    // 监听系统主题变化
    prefersDarkMode.addEventListener('change', updateTheme);
    
    // SweetAlert 库的加载
    if (typeof Swal === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/sweetalert2@11';
        document.head.appendChild(script);
    }
});