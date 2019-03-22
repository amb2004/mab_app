
function get(name,obj,cropper){
    var rect = obj[name]
    // console.log(rect)
    // cropper.setData(rect)
   



    return rect
}


document.getElementById("reset").addEventListener("click", function(){
    //    console.log("Hello World");
    document.getElementById("get_title").className = "btn btn-info btn-arrow-right"
    document.getElementById("get_drawing").className = "btn btn-info btn-arrow-right"
    document.getElementById("get_project").className = "btn btn-info btn-arrow-right"
    document.getElementById("revision").className = "btn btn-info btn-arrow-right"
     
    obj["title"]=null
    obj["project_number"]=null
    obj["revsion"]=null

    

    });



document.getElementById("get_title").className = "btn btn-success";
document.getElementById("get_drawing").className = "btn btn-success";
document.getElementById("revision").className = "btn btn-success";
          
document.getElementById("get_title").addEventListener("click",function(){

    if (obj["title"]==null){
        var aa=cropper.getData()
        obj["title"]=JSON.stringify(aa)
        document.getElementById("get_title").className = "btn btn-success";
    }
    else{
        var recta =get("title",obj)
        try {
        recta=JSON.parse(recta)
        }
        catch(e){

        }
        cropper.setData(recta)
    }

    
    
})

document.getElementById("get_drawing").addEventListener("click",function(){

    if (obj["project_number"]==null){
        var aa=cropper.getData()
        obj["project_number"]=JSON.stringify(aa)
        document.getElementById("get_drawing").className = "btn btn-success";
    }
    else{
        var recta =get("project_number",obj)
        try{
        recta=JSON.parse(recta)
    }
    catch(e){

    }
        cropper.setData(recta)
    }
    
})

document.getElementById("revision").addEventListener("click",function(){

    if (obj["revsion"]==null){
        var aa=cropper.getData()
        obj["revsion"]=JSON.stringify(aa)
        document.getElementById("revision").className = "btn btn-success";
    }
    else{
        var recta =get("revsion",obj)
        try{
        recta=JSON.parse(recta)
    }catch(e){
        
    }
        cropper.setData(recta)
    }

})

var image = document.getElementById('blah');

var cropper = new Cropper(image, {


      
      crop: function(e) {




        document.getElementById("dataX").value = e.detail.x;
        document.getElementById("dataY").value = e.detail.y;
        document.getElementById("dataWidth").value = e.detail.width;
        document.getElementById("dataHeight").value = e.detail.height;
        document.getElementById("dataRotate").value = e.detail.rotate;
  
        var img=cropper.getCroppedCanvas({height:200}).toDataURL('image/jpeg')

          $("#uploader-preview").attr("src", img);



        
      }
      
    });


    document.getElementById('zoom_button').addEventListener('click', function(){
        cropper.zoom(0.1)
        })
        document.getElementById('un_zoom_button').addEventListener('click', function(){
        cropper.zoom(-0.1)
        })
        document.getElementById('set_drag_mode').addEventListener('click', function(){
        cropper.setDragMode("move")
        
        })
        document.getElementById('set_crop_mode').addEventListener('click', function(){
        cropper.setDragMode("crop")
        
        })
        
        document.getElementById('move_left').addEventListener('click', function(){
        cropper.move(10,0)
        
        })
        document.getElementById('move_right').addEventListener('click', function(){
        cropper.move(10,0)
        
        })
        
        document.getElementById('move_up').addEventListener('click', function(){
        cropper.move(0,-10)
        
        })
        document.getElementById('move_down').addEventListener('click', function(){
        cropper.move(0,10)
        
        })
        
        
        document.getElementById('rotat_plus').addEventListener('click', function(){
        cropper.rotate(90)
        
        })
        
        
        document.getElementById('rotat_moin').addEventListener('click', function(){
        cropper.rotate(-90)
        
        })

    document.getElementById('finish_btn').addEventListener('click', function(){
        $.ajax({
            url: '/save_edit',
            type: 'POST',
            data: JSON.stringify(obj),
            dataType: 'json',
            success : function(response){
                            console.log(response)
                            window.location.replace("/display")
                        }
        });
        
        })