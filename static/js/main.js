
document.addEventListener('DOMContentLoaded', function() {
    console.log('Turizm Shop initialized');
    
    
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

  
    initializeToasts();
});


function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const bgClass = type === 'success' ? 'bg-success' : 
                    type === 'error' ? 'bg-danger' : 'bg-warning';
    
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'x-circle' : 'exclamation-circle'}"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();
    
   
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}


function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'position-fixed top-0 end-0 p-3';
    container.style.zIndex = '11';
    document.body.appendChild(container);
    return container;
}


function initializeToasts() {

    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**

 * @param {number} productId - ID товара
 * @param {string} url - URL для добавления в корзину
 */
async function addToCart(productId, url) {
    const button = document.querySelector(`[data-product-id="${productId}"]`);
    const originalText = button.innerHTML;
    
  
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Добавление...';
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            showToast('Товар добавлен в корзину!', 'success');
            
            
            updateCartCount(data.cart_count);
        } else {
            throw new Error('Ошибка при добавлении товара');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Ошибка при добавлении товара в корзину', 'error');
    } finally {
     
        button.disabled = false;
        button.innerHTML = originalText;
    }
}


function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
           document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
}


function updateCartCount(count) {
    const cartBadge = document.querySelector('.navbar-nav .badge');
    if (cartBadge) {
        cartBadge.textContent = count;
        cartBadge.style.display = count > 0 ? 'inline' : 'none';
    }
}


async function loadProductsFromAPI(endpoint) {
    const container = document.getElementById('products-container');
    if (!container) return;
    

    container.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                <span class="visually-hidden">Загрузка...</span>
            </div>
            <p class="mt-3">Загрузка товаров...</p>
        </div>
    `;
    
    try {
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error('Ошибка загрузки данных');
        }
        
        const products = await response.json();
        renderProducts(products, container);
        
    } catch (error) {
        console.error('Error loading products:', error);
        container.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle"></i>
                Ошибка при загрузке товаров. Пожалуйста, обновите страницу.
            </div>
        `;
        showToast('Ошибка при загрузке товаров', 'error');
    }
}


function renderProducts(products, container) {
    if (products.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info text-center">
                <i class="bi bi-info-circle fs-1 d-block mb-3"></i>
                <h5>Товары не найдены</h5>
            </div>
        `;
        return;
    }
    
    let html = '<div class="row g-4">';
    
    products.forEach(product => {
        html += `
            <div class="col-sm-6 col-md-4 col-lg-3">
                <div class="card h-100 shadow-sm product-card">
                    ${product.image ? 
                        `<img src="${product.image}" class="card-img-top" alt="${product.name}" style="height: 200px; object-fit: cover;">` :
                        `<div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 200px;">
                            <i class="bi bi-image text-muted fs-1"></i>
                        </div>`
                    }
                    <div class="card-body d-flex flex-column">
                        <h6 class="card-title">${product.name}</h6>
                        <p class="card-text text-muted small flex-grow-1">
                            ${product.description ? product.description.substring(0, 100) + '...' : ''}
                        </p>
                        <div class="d-flex justify-content-between align-items-center mt-3">
                            <span class="fs-5 fw-bold text-primary">${product.price} ₽</span>
                            <a href="/catalog/${product.id}/" class="btn btn-sm btn-outline-primary">
                                <i class="bi bi-eye"></i> Подробнее
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}


 
let searchTimeout;
function handleSearch(input, callback) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        callback(input.value);
    }, 500); 
}


window.TurizmShop = {
    addToCart,
    showToast,
    loadProductsFromAPI,
    handleSearch
};