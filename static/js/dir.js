function fetch_tiling(){
    folder = document.getElementById('path').innerHTML
    fetch('/api/images?dir='+folder, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        console.log(data['images'])//.length)

        if(Object.keys(data['images']).length === 0 && data['files'].length === 0 && data['folders'].length === 0){
            document.getElementById('error_message').innerHTML = 'Directory is empty'
            return
        }
        console.log(1)
        
        console.log(data['folders'])

        resize_containers();
        generate_tiling(data['images']);
        list_files(data['files']);
        list_folders(data['folders']);
        
    }
    ).catch(error=>{
        console.error(error)
    })
}

function resize_containers(){
    container_files = document.getElementById('file-container');
    container_folder = document.getElementById('folder-container');
    width =  document.getElementById('main-container').offsetWidth;

    container_folder.style.cssText = `grid-template-columns: repeat(${Math.floor(width/164)}, 164px);`;
    container_files.style.cssText = `grid-template-columns: repeat(${Math.floor(width/164)}, 164px);`;
}

function list_files(data){
    container_files = document.getElementById('file-container')
    if(data.length === 0){
        container_files.classList.add('d-none');
    }

    data.forEach(element =>{
            container_files.innerHTML += `
            <a href="/pretty/${element[1]}" class='d-flex align-content-center justify-content-center'>
                <div class='folder' >
                <img src="/static/file.png" style='display: block;'>
                <p>${element[0]}</p>
                </div>
            </a>
            `
    })
}

function list_folders(data){
    container_folder = document.getElementById('folder-container')
    if(data.length === 0){
        container_folder.classList.add('d-none');
    }
    data.forEach(element =>{
        container_folder.innerHTML += `
            <a href="/${element[1]}" class='d-flex align-content-center justify-content-center'>
                <div class='folder' >
                <img src="/static/folder.png" style='display: block;'>
                <p>${element[0]}</p>
                </div>
            </a>
            `
    })
}

function generate_tiling(data){
    console.log(data)
    body = document.getElementById('img-container')
    body.innerHTML = '';
    columns = 6

    window.localStorage.setItem('images', JSON.stringify(data))
    total_width = document.body.offsetWidth
    
    width = body.offsetWidth

    //offset = total_width/2-width/2
    //console.log(total_width, offset)

    width_column = width/columns
    height_row = width_column
    if(width> 578){
        Array.from(Object.keys(data)).forEach(index=>{
            
            obj = data[index]
            size = obj['size']
            position = obj['position']
            body.innerHTML += `
            <a href=/${obj['link']}>
            <div style="background-image: url('https://files.jcrayb.com/compressed/${String(obj['link'])}?dim=[${size}]'); 
            height:${height_row*size[0]-5}px; 
            width:${width_column*size[1]-5}px; 
            position:absolute; 
            left:${position[1]*width_column}px;
            top:${position[0]*height_row}px;
            background-size:cover;
            background-repeat:   no-repeat;
            background-position: center center;">
            </div></a>
            `})
            
    }else{
        Array.from(Object.keys(data)).forEach(index=>{
            
            obj = data[index]
            size = obj['size']
            position = obj['position']
            body.innerHTML += `
            <a href=/${obj['link']}>
            <div style="background-image: url('https://files.jcrayb.com/compressed/${String(obj['link'])}?dim=[2,2]'); 
            height:250px; 
            background-size:cover;
            background-repeat:   no-repeat;
            background-position: center center;
            margin: 5px 5px 5px 0px;" 
            class="w-100">
            </div></a>
            `})  
            console.log(3)
    }
    console.log(2)
}

function resize_tiling(){
    images = JSON.parse(window.localStorage.getItem('images'))
    generate_tiling(images)
}