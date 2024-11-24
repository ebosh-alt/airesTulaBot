function show() {
    element = document.querySelector('.other_div');
    element.style.visibility = 'visible';
}

function submitForm() {
    var selectedSaleId = window.location.pathname.split('/');
    var selectedStatus = document.getElementById("statusSelect").value;
    var selectedDate = document.getElementById('date').value;
    var selectedComment = document.getElementById('comment').value;


    var data = {
        status: selectedStatus,
        date: selectedDate,
        comment: selectedComment,
        deal_id: selectedSaleId[3]
    };

    const url = "http://localhost:3000/update";

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(result => {
            document.getElementById('result').innerText = "";

        })
    // .catch(error => {
    //     document.getElementById('result').innerText = "";
    // });
    alert('Данные отправлены в CRM')

    setTimeout(function () {
        location.reload();
    }, 3000);
}


