function save_link(){
    link = document.getElementsByName('save-link-input')[0].value;
    name = document.getElementsByName('save-name-input')[0].value;
    if(link==="" || name===""){
        document.getElementById('save-link-error').innerHTML = "Please add a link and name to save."
        return
    }
    const url = new URL(link)

    if(url.host!=="files.jcrayb.com"){
        document.getElementById('save-link-error').innerHTML = "The link you are trying to save isn't from files.jcrayb.com."
    }
    append_to_local_storage('files', name, link)
    display_saved_links('files')
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

function display_saved_links(property_name){
    saved_links_array = JSON.parse(localStorage.getItem(property_name))
    saved_links_container = document.getElementById('saved-links-container')

    saved_links_container.innerHTML = ''

    saved_links_array.forEach(link => {
        saved_links_container.innerHTML += `
        <a href="${link[1]}" class="text-decoration-none">
            <div class="card p-2">
                <p class="m-0">Name:${link[0]}</p> 
                <p class="m-0">Link:${link[1]}</p>
            </div>
        </a>
        `
    });
    console.log(saved_links_array)
}