// Retail Order Platform Frontend JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // Dynamic order line items in Create Order page
    const addItemBtn = document.getElementById('btn-add-item');
    const itemsContainer = document.getElementById('items-container');
    const createOrderForm = document.getElementById('create-order-form');

    if (addItemBtn && itemsContainer) {
        let itemCount = 1;

        addItemBtn.addEventListener('click', () => {
            const firstRow = itemsContainer.querySelector('.item-line');
            if (!firstRow) return;

            const newRow = firstRow.cloneNode(true);
            newRow.id = `item-line-${itemCount}`;
            
            // Reset fields
            const productSelect = newRow.querySelector('.product-select');
            productSelect.selectedIndex = 0;
            const qtyInput = newRow.querySelector('.item-quantity');
            qtyInput.value = 1;

            const removeBtn = newRow.querySelector('.btn-remove-item');
            removeBtn.disabled = false;
            removeBtn.addEventListener('click', () => {
                newRow.remove();
            });

            itemsContainer.appendChild(newRow);
            itemCount++;
        });

        // Enable remove on cloned items
        itemsContainer.querySelectorAll('.btn-remove-item').forEach(btn => {
            btn.addEventListener('click', function() {
                const row = this.closest('.item-line');
                if (itemsContainer.querySelectorAll('.item-line').length > 1) {
                    row.remove();
                }
            });
        });
    }

    if (createOrderForm) {
        createOrderForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const errorAlert = document.getElementById('form-error-alert');
            const successAlert = document.getElementById('form-success-alert');
            errorAlert.classList.add('d-none');
            successAlert.classList.add('d-none');

            const customerId = document.getElementById('customer_id').value;
            const paymentMethod = document.getElementById('payment_method').value;
            const shippingAddress = document.getElementById('shipping_address').value;

            const items = [];
            const itemLines = document.querySelectorAll('.item-line');
            for (const line of itemLines) {
                const prodId = line.querySelector('.product-select').value;
                const qty = line.querySelector('.item-quantity').value;
                if (prodId && qty) {
                    items.push({
                        product_id: parseInt(prodId),
                        quantity: parseInt(qty)
                    });
                }
            }

            if (items.length === 0) {
                errorAlert.textContent = 'Please add at least one product item.';
                errorAlert.classList.remove('d-none');
                return;
            }

            const payload = {
                customer_id: parseInt(customerId),
                payment_method: paymentMethod,
                shipping_address: shippingAddress,
                items: items
            };

            try {
                const resp = await fetch('/api/orders', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                const data = await resp.json();

                if (!resp.ok) {
                    errorAlert.textContent = data.error || 'Failed to create order.';
                    errorAlert.classList.remove('d-none');
                } else {
                    successAlert.textContent = `Order ${data.order.order_number} created successfully! Redirecting...`;
                    successAlert.classList.remove('d-none');
                    setTimeout(() => {
                        window.location.href = `/orders/${data.order.order_id}`;
                    }, 1200);
                }
            } catch (err) {
                errorAlert.textContent = 'Network error while creating order.';
                errorAlert.classList.remove('d-none');
            }
        });
    }
});
