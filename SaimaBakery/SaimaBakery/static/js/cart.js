// gets all the elements with the class update cart
var updateBtns = document.getElementsByClassName('update-cart');

// for loop through cart updating buttons and click events for evry button
for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        //gets product ID and action
        var productId = this.dataset.product;
        var action = this.dataset.action;

        console.log('productId:', productId, 'Action:', action);
        console.log('USER:', user);
        // cookies to update cart for anonymous user or just updates cart if admin/logged in user
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    });
}

// for updating carts using cookies so it works for anonymous users
function addCookieItem(productId, action) {
    console.log('User is not authenticated');
    //actions performed on cart
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1};
        } else {
            cart[productId]['quantity'] += 1;
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted');
            delete cart[productId];
        }
    }
    // update cart cookies and reloads page
    console.log('CART:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();
}

// update cart for logged in users (admin users only currently) by sending a POST request
function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,   // CSRF token for security
        },
        body: JSON.stringify({'productId': productId, 'action': action}) //sends poduct id and action as JSON
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload();
    });
}
