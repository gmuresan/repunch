function initiate_facebook_login(app_id, redirect_uri) {
    window.open('https://www.facebook.com/dialog/oauth?client_id='+app_id+'&redirect_uri='+redirect_uri+'&scope=&response_type=token',"mywindow","menubar=1,resizable=1,width=350,height=250");
}