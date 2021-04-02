function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


let comment_div = document.createElement('comment_div');
function addTextField() {
    /* Добавляет блок с полем для ввода и кнопку на отправку ответа */

    if (comment_div.innerHTML !== ''){
        return false;
    }
    const event_id = JSON.parse(document.getElementById('event_id').textContent);
    const event_reg = JSON.parse(document.getElementById('events_register_url').textContent);
    comment_div.innerHTML = `
<div class="row-py-2">
    <div class="col">
        <div class="form-group">
            <label for="fromControlTextarea1">Описание причины</label>
            <div class="invalid-feedback" style="display: none">Ответ не может быть пустым!</div>
            <textarea class="form-control" id="fromControlTextarea1" rows="3"></textarea>
        </div>
    </div>
</div>
<div class="row py-2">
    <div class="col">
        <a href="javascript:sendCancelFormData();"
           class="btn btn-primary stretched-link" style="width: 100%">Отправить</a>
    </div>
</div>
`;

    document.querySelector("body > div.container.py-sm-3 > div > div > div > div.col-md-4.py-2 > div:nth-child(6)").after(comment_div);
    return false;
}


async function sendCancelFormData(){
    /* Отправляет даннны из формы на сервер */

    const csrftoken = getCookie('csrftoken');
    const event_reg = JSON.parse(document.getElementById('events_register_url').textContent);
    let form_textarea = document.getElementById("fromControlTextarea1");

    console.log(form_textarea.value.length)
    if ( form_textarea.value.length < 5){
        comment_div = document.getElementsByClassName('invalid-feedback')[0];
        comment_div.style.display = 'block';
        return false;
    }

    let promise = await fetch(event_reg, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({user_comment: form_textarea.value})
    }).then(function (response){
        if (response.status === 200) {
            window.location.reload();
        } else {
            alert('Не удалось передать данные');
            window.location.reload();
        }
    });
}
