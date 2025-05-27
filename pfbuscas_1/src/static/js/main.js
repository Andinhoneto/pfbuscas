// Arquivo JavaScript para funcionalidades adicionais do PFBuscas
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se há um CPF na URL (vindo do histórico)
    const urlParams = new URLSearchParams(window.location.search);
    const cpfParam = urlParams.get('cpf');
    
    if (cpfParam && document.getElementById('cpfInput')) {
        document.getElementById('cpfInput').value = cpfParam;
        // Acionar a busca automaticamente
        document.getElementById('searchForm').dispatchEvent(new Event('submit'));
    }
    
    // Adicionar máscara ao CPF quando disponível
    const cpfInput = document.getElementById('cpfInput');
    if (cpfInput) {
        cpfInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) {
                value = value.substring(0, 11);
            }
            e.target.value = value;
        });
    }
    
    // Adicionar funcionalidade de toggle para o sidebar em dispositivos móveis
    const navbarToggler = document.querySelector('.navbar-toggler');
    const sidebar = document.querySelector('.sidebar');
    
    if (navbarToggler && sidebar) {
        navbarToggler.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }
    
    // Fechar sidebar ao clicar em um link (em dispositivos móveis)
    const sidebarLinks = document.querySelectorAll('.sidebar .nav-link');
    
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth < 768) {
                sidebar.classList.remove('show');
            }
        });
    });
    
    // Adicionar tooltips para melhorar a experiência do usuário
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Função para formatar CPF
function formatCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    if (cpf.length === 11) {
        return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
    }
    return cpf;
}

// Função para mostrar notificações
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Remover após 5 segundos
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}
