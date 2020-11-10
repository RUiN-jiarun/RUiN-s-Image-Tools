var sFile   = "";
var sType   = "png";
var file      = document.getElementById("src"),
    wm        = document.getElementById("wm"),
    sourceImg = document.getElementById("source_img"),
    wmImg     = document.getElementById("wm_img"),
    canvas    = document.getElementById("canvas"),
    turnTo    = document.getElementById("turnTo"),
    download  = document.getElementById("download");

var canDownload = document.getElementById("canDownload").innerHTML;

function fileChange(){
    file.addEventListener("change",function()
    {
        var files = file.files[0];
        var reader = new FileReader();
        reader.onload = function(e){
            e = e || event;
            sourceImg.src = e.target.result;
        };
        reader.readAsDataURL(files);
    },false);
}

function downloadPic() {
//    console.log(canDownload)
    if(canDownload == 'True')
    {
        var imgData = wmImg.src;
        var down = document.getElementById("downIMG");
        down.href = imgData;
        down.download = (new Date()).toLocaleString()+"."+(sType?sType:"jpg");
        var mouseEv = document.createEvent("MouseEvents");
        mouseEv.initMouseEvent("click",false,false,window,0,0,0,0,0,false,false,false,false,0,null);
        down.dispatchEvent(mouseEv);
    }
    else
    {
        alert('No result image!');
    }

}

function init(){
    fileChange();
}

init();