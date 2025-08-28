async function cartUpdate(e) {
    const { data } = await axios(e.dataset.url)
    const { message, items_count } = data
    notyf.success({message,
        dismissible: true,
        icon: false
    })
    document.getElementById('cart-items-count').innerHTML = items_count
}


async function cartRemove(e) {
    await axios(e.dataset.url)
    location.reload()
}

function switchPaymentMethod(type, content) {
   const stripeCard = document.getElementById('stripe-card');
   
   if (type === 'stripe') {
       stripeCard.style.display = 'block';
   } else {
       stripeCard.style.display = 'none';
   }
}