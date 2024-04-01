function save_link(){
    link = document.getElementsByName('save-link-input')[0].value;
    name = document.getElementsByName('save-name-input')[0].value;
    if(link==="" || name===""){
        document.getElementById('save-link-error').innerHTML = "Please add a link and name to save."
        return
    }
    try {
        url = new URL(link)
    } catch (error) {
        document.getElementById('save-link-error').innerHTML = "The link you are trying to is invalid."
        return
    }
    

    if(url.host!=="files.jcrayb.com"){
        document.getElementById('save-link-error').innerHTML = "The link you are trying to save isn't from files.jcrayb.com."
        return
    }
    append_to_local_storage('files', name, link);
    display_saved_links('files');
    window.Location.reload();
}

function append_to_local_storage(property_name, name, value){
    let current_value = JSON.parse(localStorage.getItem(property_name))
    console.log(current_value, typeof(current_value))
    if (current_value===null){
        localStorage.setItem(property_name, JSON.stringify([[name, value]]))
    }else if(current_value.includes(value)===true){
        document.getElementById('save-link-error').innerHTML = "This link has already been saved"
    }else{
        current_value.push([name, value])
        localStorage.setItem(property_name, JSON.stringify(current_value))
    }
}

function remove_from_local_storage(property_name, index){
    let current_value = JSON.parse(localStorage.getItem(property_name))
    console.log(current_value, typeof(current_value))
    current_value.splice(index, 1)
    localStorage.setItem(property_name, JSON.stringify(current_value))
}

function display_saved_links(property_name){
    saved_links_array = JSON.parse(localStorage.getItem(property_name))
    saved_links_container = document.getElementById('saved-links-container')

    saved_links_container.innerHTML = ''
    index = 0
    saved_links_array.forEach(link => {
        saved_links_container.innerHTML += `
        <div id="link-${index}">
            <div class="card p-2 my-2">
                <div class="row">
                    <a href="${link[1]}" class="text-decoration-none col-10 text-dark" themed-text>
                        <div>
                            <p class="m-0">Name: &ensp; ${link[0]}</p> 
                            <p class="m-0">Link: &ensp; ${link[1]}</p>
                        </div>
                    </a>
                    <div class="col-2 d-flex justify-content-end align-items-center">
                        <button type="button" class="btn-close" aria-label="Close" onclick="remove_link(${index})"></button>
                    </div>
                </div>
            </div>
            
        </div>
        `
        index += 1
    });
}

function remove_link(index){
    document.getElementById(`link-${index}`).remove();
    remove_from_local_storage('files', index);
    display_saved_links('files');
    window.Location.reload();
}