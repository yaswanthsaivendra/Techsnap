let btn = document.querySelector(".toggle");
let icon = document.querySelector(".fa-bars");
let nav = document.querySelector(".show-menu");

// btn.onclick = function () {
//   if (icon.classList.contains("fa-bars")) {
//     icon.classList.replace("fa-bars", "fa-times");
//     nav.style.display = "block";
//   } else {
//     icon.classList.replace("fa-times", "fa-bars");
//     nav.style.display = "none";
//   }
// };

let jobField = document.querySelector(".skill-content-job");

let softEng = document.querySelector("#software-eng");
let softEngRole = document.querySelector(".software-eng");

let webDev = document.querySelector("#web-dev");
let webDevRole = document.querySelector(".web-dev");

let qa = document.querySelector("#qa");
let qaRole = document.querySelector(".qa");

let devOps = document.querySelector("#cloud-devops");
let devOpsRole = document.querySelector(".cloud-devops");

let dataScience = document.querySelector("#data-science");
let dataScienceRole = document.querySelector(".data-science");

let cyber = document.querySelector("#cybersecurity");
let cyberRole = document.querySelector(".cybersecurity");

let softEngTag = document.getElementsByClassName(".software-eng-tag");
let webDevTag = document.getElementsByClassName(".web-dev-tag");
let qaTag = document.getElementsByClassName(".qa-tag");
let devOpsTag = document.getElementsByClassName(".cloud-devops-tag");
let dataScienceTag = document.getElementsByClassName(".data-science-tag");
let cyberTag = document.getElementsByClassName(".cybersecurity-tag");

softEng.onclick = () => {
  if (
    !softEng.classList.contains("active") &&
    !softEngRole.classList.contains("active")
  ) {
    console.log("clicked");
    softEng.classList.add("active");
    softEngRole.classList.add("active");

    webDev.classList.remove("active");
    webDevRole.classList.remove("active");

    qa.classList.remove("active");
    qaRole.classList.remove("active");

    devOps.classList.remove("active");
    devOpsRole.classList.remove("active");

    dataScience.classList.remove("active");
    dataScienceRole.classList.remove("active");

    cyber.classList.remove("active");
    cyberRole.classList.remove("active");
    cyberTag.classList.remove("active");
  }

  // if (!softEngTag.classList.contains("active")) {
  //   console.log("clicked");
  //   softEngTag.classList.add(active);
  // }
};

webDev.onclick = () => {
  if (
    !webDev.classList.contains("active") &&
    !webDevRole.classList.contains("active")
  ) {
    console.log("clicked");
    webDev.classList.add("active");
    webDevRole.classList.add("active");

    softEng.classList.remove("active");
    softEngRole.classList.remove("active");

    qa.classList.remove("active");
    qaRole.classList.remove("active");

    devOps.classList.remove("active");
    devOpsRole.classList.remove("active");

    dataScience.classList.remove("active");
    dataScienceRole.classList.remove("active");

    cyber.classList.remove("active");
    cyberRole.classList.remove("active");
  }
};

qa.onclick = () => {
  if (
    !qa.classList.contains("active") &&
    !qaRole.classList.contains("active")
  ) {
    console.log("clicked");

    qa.classList.add("active");
    qaRole.classList.add("active");

    webDev.classList.remove("active");
    webDevRole.classList.remove("active");

    softEng.classList.remove("active");
    softEngRole.classList.remove("active");

    devOps.classList.remove("active");
    devOpsRole.classList.remove("active");

    dataScience.classList.remove("active");
    dataScienceRole.classList.remove("active");

    cyber.classList.remove("active");
    cyberRole.classList.remove("active");
  }
};

devOps.onclick = () => {
  if (
    !devOps.classList.contains("active") &&
    !devOpsRole.classList.contains("active")
  ) {
    console.log("clicked");
    devOps.classList.add("active");
    devOpsRole.classList.add("active");

    qa.classList.remove("active");
    qaRole.classList.remove("active");

    webDev.classList.remove("active");
    webDevRole.classList.remove("active");

    softEng.classList.remove("active");
    softEngRole.classList.remove("active");

    dataScience.classList.remove("active");
    dataScienceRole.classList.remove("active");

    cyber.classList.remove("active");
    cyberRole.classList.remove("active");
  }
};

dataScience.onclick = () => {
  if (
    !dataScience.classList.contains("active") &&
    !dataScienceRole.classList.contains("active")
  ) {
    console.log("clicked");
    dataScience.classList.add("active");
    dataScienceRole.classList.add("active");

    qa.classList.remove("active");
    qaRole.classList.remove("active");

    webDev.classList.remove("active");
    webDevRole.classList.remove("active");

    softEng.classList.remove("active");
    softEngRole.classList.remove("active");

    devOps.classList.remove("active");
    devOpsRole.classList.remove("active");

    cyber.classList.remove("active");
    cyberRole.classList.remove("active");
  }
};

cyber.onclick = () => {
  if (
    !cyber.classList.contains("active") &&
    !cyberRole.classList.contains("active")
  ) {
    console.log("clicked");
    cyber.classList.add("active");
    cyberRole.classList.add("active");

    qa.classList.remove("active");
    qaRole.classList.remove("active");

    webDev.classList.remove("active");
    webDevRole.classList.remove("active");

    softEng.classList.remove("active");
    softEngRole.classList.remove("active");

    devOps.classList.remove("active");
    devOpsRole.classList.remove("active");

    dataScience.classList.remove("active");
    dataScienceRole.classList.remove("active");
  }
};