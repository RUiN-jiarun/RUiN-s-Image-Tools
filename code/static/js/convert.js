var sFile   = "";
var sType   = "png";

var file      = document.getElementById("file"),
    sourceImg = document.getElementById("source_img"),
    previewImg= document.getElementById("preview_img"),
    canvas    = document.getElementById("canvas"),
    turnTo    = document.getElementById("turnTo"),
    download  = document.getElementById("download");

var mimeTypeGet,
    canDownload = false;

function fileChange(){
    file.addEventListener("change",function()
    {
        var files = file.files[0];
        var reader = new FileReader();
        reader.onload = function(e){
            e = e || event;
            sourceImg.src = e.target.result;
            transformImg();
        };
        reader.readAsDataURL(files);
    },false);
}

function downloadPic(){
    download.onclick = function(){
        if(canDownload)
        {
            // 加工image data，替换mime type
            var imgData = previewImg.src.replace(mimeTypeGet,'image/octet-stream');
            var down = document.getElementById("downIMG");
            down.href = imgData;
            down.download = (new Date()).toLocaleString()+"."+(sType?sType:"jpg");
            var mouseEv = document.createEvent("MouseEvents");
            mouseEv.initMouseEvent("click",false,false,window,0,0,0,0,0,false,false,false,false,0,null);
            down.dispatchEvent(mouseEv);
        }
    };
}

//转换
function transformImg(){
    turnTo.onclick = function(e){
        e = e || event;
        e.stopPropagation();
        e.preventDefault();
        var type = sType || "jpg" ,
            mimeType,
            newImage = new Image(),
            cv = canvas,
            ct = cv.getContext('2d');
        mimeType = "image/"+type;
        mimeTypeGet  = mimeType;
        newImage.src = sourceImg.src;
        previewImg.src=trans().src;

        function trans(){
            cv.width = newImage.width;
            cv.height= newImage.height;
            ct.drawImage(newImage,0,0);

            var newData = cv.toDataURL(mimeType);
            var nImage = new Image();
            nImage.src = newData;
            canDownload = true;
            downloadPic();
            return nImage;
        }
    };
}

function init(){
    fileChange();
}

init();