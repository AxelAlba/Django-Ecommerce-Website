var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function() {
        var productId =  this.dataset.product;
        var action = this.dataset.action;
        console.log('productId: ', productId, 'action: ', action);

        console.log('User: ', user);
        if(user === 'AnonymousUser'){
            console.log('Not logged in');
        }
        else{
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data...');

    var url = '/update_item/'
    fetch(url, { // sets the url, the type, pass in the data
        method: 'POST',
        headers:{
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken
        },
        body: JSON.stringify({
            'productId': productId, 
            'action' : action,
        }) // This would be the data sent to main.html
    })

    .then((response) => { //response turned into json value
        return response.json()
    })

    
    .then((data) => {
        console.log('Data: ', data)
    })
}
