function copyToClipboard(){
    var message_box = document.getElementById('response_text')
    text = window.location.href;
    console.log(text);
    navigator.clipboard.writeText(text);
    message_box.innerText = 'Link copied to clipboard!';
  }