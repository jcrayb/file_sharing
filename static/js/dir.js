function fetch_tiling(){
    folder = document.getElementById('path').innerHTML
    fetch('/api/display_dir?dir='+folder, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        generate_tiling(data)
    }
    ).catch(error=>{
        console.error(error)
    })
}

function generate_tiling(data){
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
            <a href=${obj['link']}>
            <div style="background-image: url('https://files.jcrayb.com/${String(obj['link'])}'); 
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
            <a href=${obj['link']}>
            <div style="background-image: url('https://files.jcrayb.com/${String(obj['link'])}'); 
            height:250px; 
            background-size:cover;
            background-repeat:   no-repeat;
            background-position: center center;
            margin: 5px 5px 5px 0px;" 
            class="w-100">
            </div></a>
            `})  
    }
    
}

function resize_tiling(){
    images = JSON.parse(window.localStorage.getItem('images'))
    generate_tiling(images)
}