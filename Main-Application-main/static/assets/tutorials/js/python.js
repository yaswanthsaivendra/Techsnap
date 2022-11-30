var slider_content_show_element = document.getElementsByClassName("slider-content-show");
var slider_content_left_element = document.getElementsByClassName("slider-content-left");
var slider_content_right_element = document.getElementsByClassName("slider-content-right");
var index =0;
function increase_slider_content(){
    index++;
    if(index>slider_content_show_element.length-1){
        index=0;
    }
    for(var loop1=0; loop1<=slider_content_left_element.length-1; loop1++){
        if(loop1==index){
            slider_content_show_element[index].style.display = "block";
            slider_content_right_element[index].style.display = "block";
            slider_content_left_element[index].style.display = "block";
        }
        else{
            slider_content_show_element[loop1].style.display = "none";
            slider_content_left_element[loop1].style.display = "none";
            slider_content_right_element[loop1].style.display = "none";
        }
    }
    console.log(index);
}
function decrease_slider_content(){
    index--;
    if(index<0){
        index=slider_content_show_element.length-1;
    }
    for(var loop1=0; loop1<=slider_content_left_element.length-1; loop1++){
        if(loop1==index){
            slider_content_show_element[index].style.display = "block";
            slider_content_left_element[index].style.display = "block";
            slider_content_right_element[index].style.display = "block";
        }
        else{
            slider_content_show_element[loop1].style.display = "none";
            slider_content_left_element[loop1].style.display = "none";
            slider_content_right_element[loop1].style.display = "none";
        }
    }
    console.log(index);
}
increase_slider_content();