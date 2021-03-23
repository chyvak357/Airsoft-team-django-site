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


function addTextField() {

    let comment_div = document.createElement('comment_div');
    const event_id = JSON.parse(document.getElementById('event_id').textContent);
    const event_reg = JSON.parse(document.getElementById('events_register_url').textContent);
    // alert()
    comment_div.innerHTML = `
<div class="row-py-2">
    <div class="col">
        <div class="form-group">
            <label for="fromControlTextarea1">Указание причины</label>
            <textarea class="form-control" id="fromControlTextarea1" rows="3"></textarea>
        </div>
    </div>
</div>
<div class="row py-2">
    <div class="col">
<!--        <a href="javascript:showInputMassage();"-->
        <a href="javascript:sendCancelFormData();"
           class="btn btn-primary stretched-link" style="width: 100%">Отправить</a>
    </div>
</div>
`;

    document.querySelector("body > div.container.py-sm-3 > div > div > div > div.col-md-4.py-2 > div:nth-child(5)").after(comment_div);
    return false;
}

function showInputMassage() {
    let form_textarea = document.getElementById("fromControlTextarea1");
    alert(form_textarea.value);
    return false;
}

async function sendCancelFormData(){
    const csrftoken = getCookie('csrftoken');

    // if (act_type === 'reg'){

    // } else if (act_type) ==
    const event_reg = JSON.parse(document.getElementById('events_register_url').textContent);


    let form_textarea = document.getElementById("fromControlTextarea1");
    // let promise = fetch(event_reg);
    console.log(JSON.stringify({user_comment: form_textarea.value}));

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
            alert('Не удалось передать данные')
            window.location.reload();
        }
    });
}

function testData(){
    // let chat = document.querySelector("#chat");
    // let input = document.querySelector("#message-input");
    // let btnSubmit = document.querySelector("#btn-submit");
    const event_id = JSON.parse(document.getElementById('event_id').textContent);
    // const user_id = JSON.parse(document.getElementById('user_id').textContent);
    // const username = JSON.parse(document.getElementById('username').textContent);
    alert(event_id)

    return false;
}