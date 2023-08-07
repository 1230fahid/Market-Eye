const addStock = () => {
    const element = document.getElementById('wl');
    const watchlistList = document.getElementById('wl-l');

    console.dir(element);
    const div = document.createElement('div')
    div.id = 'addDiv';
    div.style.backgroundColor = 'black';
    div.style.border = '1px solid #E6BE8A';
    div.style.borderRadius = '10px';
    div.style.width = 'fit-content';
    div.style.height = 'fit-content';
    div.style.position = 'absolute';
    div.style.marginTop = '10%';
    div.style.padding = '2%';

    const form = document.createElement('form');
    //form.method = 'POST';
    //form.action = window.location.origin + '/Stock/Add';

    const h2 = document.createElement('h2');
    h2.innerText = 'Add Stock'
    h2.style.color = '#E6BE8A'
    h2.style.textAlign = 'center';

    const span = document.createElement('span')
    span.style.color = 'red';
    span.style.visibility = 'hidden';

    const br = document.createElement('br')

    const tick = document.createElement('input');
    tick.type = 'text';
    tick.style.backgroundColor = 'black';
    tick.style.border = 'none';
    tick.style.borderBottom = '1px solid #E6BE8A';
    tick.id = 'tick';
    tick.placeholder = 'TICK....';
    tick.style.color = '#E6BE8A';
    tick.name = 'symbol';
    tick.oninput = () => {
        if (tick.value === '')
        {
            addButton.style.backgroundColor = 'rgba(0,0,255,0.5)';
            addButton.disabled = true;
            //form.action = window.location.origin + '/Stock/Add';
        }
        else
        {
            addButton.style.backgroundColor = 'rgba(0,0,255,1)';
            addButton.disabled = false;
            //form.action = window.location.origin + '/Stock/Add?symbol=' + tick.value;
        }

        if (span.style.visibility === 'visible')
        {
            span.style.visibility = 'hidden';
            span.innerText = '';
        }
    };
    tick.style.margin = '5px 0';

    const tickLabel = document.createElement('label');
    tickLabel.htmlFor = 'tick';
    tickLabel.innerText = 'Stock Tick:';
    tickLabel.style.color = '#E6BE8A';

    const cancelButton = document.createElement('button');
    const addButton = document.createElement('button');

    const flexDiv = document.createElement('div');
    flexDiv.style.display = 'flex';
    flexDiv.style.flexDirection = 'row';
    flexDiv.style.justifyContent = 'center';
    flexDiv.style.marginTop = '5px';

    cancelButton.style.color = 'white';
    cancelButton.style.backgroundColor = 'red';
    cancelButton.style.padding = '5px';
    cancelButton.innerText = 'Cancel'
    cancelButton.style.textAlign = 'center';
    cancelButton.style.border = '1px solid red';
    cancelButton.style.marginRight = '1%';
    cancelButton.onclick = () => {
        const addDiv = document.getElementById('addDiv');
        addDiv.remove();
        const element = document.getElementById('wl');
        const watchlistList = document.getElementById('wl-l');
        element.style.backgroundColor = 'black';
        watchlistList.style.backgroundColor = 'rgba(123, 123, 123, 0.6)';
    }

    addButton.style.color = 'white';
    addButton.style.backgroundColor = 'rgba(0,0,255,0.5)';
    addButton.style.padding = '5px';
    addButton.innerText = 'Add'
    addButton.style.textAlign = 'center';
    addButton.style.border = '1px solid blue';
    addButton.disabled = true;
    addButton.type = 'submit';

    flexDiv.appendChild(cancelButton);
    flexDiv.appendChild(addButton);

    form.appendChild(h2);
    form.appendChild(tickLabel);
    form.appendChild(tick);
    form.appendChild(br);
    form.appendChild(span);
    form.appendChild(flexDiv);

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState === 4 && xhttp.status === 400) {
            span.innerText = xhttp.responseText;
            span.style.visibility = 'visible';
        }
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        let request = window.location.origin + '/Stock/Add'

        //Be very careful with post request configuration because a preflight response may be added depending on headers you add
        xhttp.open('POST', request)
        xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhttp.send('symbol=' + tick.value);
    })

    div.appendChild(form);

    element.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    watchlistList.style.backgroundColor = 'rgba(123, 123, 123, 0.2)';
    element.appendChild(div);
    
}
