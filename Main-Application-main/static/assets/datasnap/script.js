const toggle_button = document.getElementById("toggle")
const root = document.querySelector(':root');
var rs = getComputedStyle(root);
const write = document.getElementById('write')

var contentbg = '#0e1a24'
var bg = 'black'
var t1 = 'white'

var temp = 'white'

toggle_button.addEventListener("click", () => {
    if(toggle_button.className === "day")
    {
        root.style.setProperty('--verydarkblue', 'white');
        root.style.setProperty('--black', '#f2f8fb');
        root.style.setProperty('--white', 'black');
        temp = 'black'
        toggle_button.className = "night"
        write.style.content = "url('rsc/write-black.png')"
    }
    else
    {
        root.style.setProperty('--verydarkblue', contentbg);
        root.style.setProperty('--black', bg);
        root.style.setProperty('--white', t1);
        toggle_button.className = "day"
        write.style.content = "url('rsc/write-big.png')"
    }
})

const menu_btn = document.getElementsByClassName("menu-icon")[0]
const close_btn = document.getElementsByClassName("close")[0]
const side_panel = document.getElementById("side-panel")
const container = document.getElementsByClassName('outer-container')[0]

menu_btn.addEventListener("click", () => {
    side_panel.style.display = "block"
    side_panel.style.transition = "0.1s"
    container.style.filter = "blur(5px)"
    container.style.position = "fixed"
})

close_btn.addEventListener("click", () => {
    side_panel.style.display = "none"
    container.style.filter = "none"
    container.style.position = "relative"
})