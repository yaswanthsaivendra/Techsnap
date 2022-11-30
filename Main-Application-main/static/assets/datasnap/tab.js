const myfeed_btn = document.getElementById('myfeed')
const featured_btn = document.getElementById('featured')
const recent_btn = document.getElementById('recent')

const myfeed_content = document.getElementsByClassName('my-feed')[0]
const featured_content = document.getElementsByClassName('featured')[0]
const recent_content = document.getElementsByClassName('recent')[0]

const myfeed_text = document.getElementById("myfeed-text")
const featured_text = document.getElementById("featured-text")
const recent_text = document.getElementById("recent-text")

const myfeed_img = document.getElementById("myfeed-img")
const featured_img = document.getElementById("featured-img")
const recent_img = document.getElementById("recent-img")

featured_btn.addEventListener("click", () => {
    myfeed_content.style.display = "none"
    featured_content.style.display = "block"
    recent_content.style.display = "none"
    featured_btn.style.borderBottom = "4px solid #0072FF"
    featured_text.style.color = "#0072FF"
    myfeed_btn.style.borderBottom = "none"
    myfeed_text.style.color = "#7f848b"
    recent_btn.style.borderBottom = "none"
    recent_text.style.color = "#7f848b"
    featured_img.style.filter = "none"
    myfeed_img.style.filter = "grayscale(80%)"
    recent_img.style.filter = "grayscale(80%)"
})
recent_btn.addEventListener("click", () => {
    myfeed_content.style.display = "none"
    featured_content.style.display = "none"
    recent_content.style.display = "block"
    featured_btn.style.borderBottom = "none"
    featured_text.style.color = "#7f848b"
    myfeed_btn.style.borderBottom = "none"
    myfeed_text.style.color = "#7f848b"
    recent_btn.style.borderBottom = "4px solid #0072FF"
    recent_text.style.color = "#0072FF"
    featured_img.style.filter = "grayscale(80%)"
    myfeed_img.style.filter = "grayscale(80%)"
    recent_img.style.filter = "none"
})
myfeed_btn.addEventListener("click", () => {
    myfeed_content.style.display = "block"
    featured_content.style.display = "none"
    recent_content.style.display = "none"
    featured_btn.style.borderBottom = "none"
    featured_text.style.color = "#7f848b"
    myfeed_btn.style.borderBottom = "4px solid #0072FF"
    myfeed_text.style.color = "#0072FF"
    recent_btn.style.borderBottom = "none"
    recent_text.style.color = "#7f848b"
    featured_img.style.filter = "grayscale(80%)"
    myfeed_img.style.filter = "none"
    recent_img.style.filter = "grayscale(80%)"
})