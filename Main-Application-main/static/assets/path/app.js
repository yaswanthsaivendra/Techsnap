const showMoreFaqBtn = document.querySelector('#more');
const faqMoreItems = document.querySelectorAll('.faq_more');
showMoreFaqBtn.addEventListener('click', () => {
	faqMoreItems.forEach((i) => {
		if (i.style.display === 'flex') {
			i.style.display = 'none';
			showMoreFaqBtn.innerHTML = 'More Lessons';
		} else {
			i.style.display = 'flex';
			showMoreFaqBtn.innerHTML = 'Less Lessons';
		}
	});
});
const header = document.querySelector('.header');
const navLink = document.querySelectorAll('.nav_item');
const ham = document.querySelector('.ham');
console.log(ham);
window.addEventListener('scroll', () => {
	const top = window.innerHeight * (15 / 100);
	if (window.scrollY <= top) {
		header.style.background = 'rgb(26, 25, 29)';
		ham.style.background = 'transparent';

		header.style.height = '60px';
		navLink.forEach((i) => {
			i.style.color = '#fff';
		});
	}
	if (window.scrollY > top) {
		header.style.background = '#fff';
		ham.style.background = '#0a33ec';
		header.style.height = '55px';
		navLink.forEach((i) => {
			i.style.color = '#000';
		});
	}
});

const Close = document.querySelector('.Close');
const DropMenu = document.querySelector('.dropMenu');
ham.addEventListener('click', () => {
	DropMenu.classList.add('MenuAnimation');
	console.log('sdsd');
});
Close.addEventListener('click', () => {
	DropMenu.classList.remove('MenuAnimation');
});


const Profile = document.querySelector('.avatar');
const Profile_dropDown = document.querySelector('.profile_dropDown');
Profile.addEventListener('click', () => {
	if (Profile_dropDown.style.opacity === '1') {
		Profile_dropDown.style.opacity = '0';
		Profile_dropDown.style.pointerEvents = 'none';
	} else {
		Profile_dropDown.style.opacity = '1';
		Profile_dropDown.style.pointerEvents = 'all';
	}
});
document.addEventListener('click', function (event) {
	var isClickInsideElement = Profile.contains(event.target);
	if (!isClickInsideElement) {
		Profile_dropDown.style.opacity = '0';
	}
});



