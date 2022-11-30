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
const notification_bell = document.querySelector('.notification_bell');
const notification_dropDown = document.querySelector('.notification_dropdown');
notification_bell.addEventListener('click', () => {
	console.log('here');
	if (notification_dropDown.style.opacity === '1') {
		notification_dropDown.style.opacity = '0';
		notification_dropDown.style.pointerEvents = 'none';
	} else {
		notification_dropDown.style.opacity = '1';
		notification_dropDown.style.pointerEvents = 'all';
	}
});
//--------------------------------------------------------------------------
const goalsSection = document.querySelector('.goals_DropDown');
const goalButton = document.querySelector('.points');

const goalsDrop = () => {
	if (goalsSection.style.visibility == 'visible') {
		goalsSection.style.visibility = 'hidden';
	} else {
		goalsSection.style.visibility = 'visible';
	}
};
const powerSection = document.querySelector('.power_dropDown');
const coinSection = document.querySelector('.coin_dropDown');

const powerhandler = () => {
	if (powerSection.style.visibility == 'visible') {
		powerSection.style.visibility = 'hidden';
	} else {
		powerSection.style.visibility = 'visible';
	}
};
const Coinhandler = () => {
	if (coinSection.style.visibility == 'visible') {
		coinSection.style.visibility = 'hidden';
	} else {
		coinSection.style.visibility = 'visible';
	}
};
const power = document.querySelector('.shock');
const coin = document.querySelector('.coin');
//--------------------------------
document.addEventListener('click', function (event) {
	var isClickInsideAvatar = Profile.contains(event.target);
	var isClickInsideBell = notification_bell.contains(event.target);
	var isClickInsideDropdown = notification_dropDown.contains(event.target);
	var isClickInsideGoal = goalButton.contains(event.target);
	var isClickInsideGoalSection = goalsSection.contains(event.target);
	let isClickInsideShock = power.contains(event.target);
	let isClickInsideCoin = coin.contains(event.target);

	if (!isClickInsideAvatar) {
		Profile_dropDown.style.opacity = '0';
		Profile_dropDown.style.pointerEvents = 'none';
	}
	if (!isClickInsideShock) {
		powerSection.style.visibility = 'hidden';
	}
	if (!isClickInsideCoin) {
		coinSection.style.visibility = 'hidden';
	}
	if (!isClickInsideGoal && !isClickInsideGoalSection) {
		goalsSection.style.visibility = 'hidden';
	}
	if (!isClickInsideBell && !isClickInsideDropdown) {
		notification_dropDown.style.opacity = '0';
		notification_dropDown.style.pointerEvents = 'none';
	}
});

// ---------leaderboard data------------------------

const slideMenu = () => {
	const sideMenu = document.querySelector('.sideMenu');
	const ham = document.querySelector('#ham_icon');
	const blurBack = document.querySelector('.max_width_holder');

	if (sideMenu.style.left === '0px') {
		sideMenu.style.left = '-250px';
		ham.src = 'https://img.icons8.com/android/96/000000/menu.png';
		blurBack.style.pointerEvents = 'all';
		blurBack.style.filter = ' blur(0px)';
	} else {
		ham.src =
			'https://img.icons8.com/material-outlined/24/000000/delete-sign.png';
		sideMenu.style.left = '0';
		blurBack.style.pointerEvents = 'none';
		blurBack.style.filter = ' blur(5px)';
	}
};
const closeInfo = () => {
	const info = document.querySelector('.info_text');
	info.style.display = 'none';
};

const closeYellowTag = () => {
	let yellowTag = document.querySelector('.yellow_tag');
	yellowTag.style.opacity = '0';
	yellowTag.style.pointerEvents = 'none';
};
