var acc = document.getElementsByClassName('accordion1');
var i;

for (i = 0; i < acc.length; i++) {
	acc[i].addEventListener('click', function () {
		this.classList.toggle('active');
		var panel = this.nextElementSibling;
		// if (panel.style.maxHeight) {
		// 	panel.style.maxHeight = null;
		// } else {
		// 	panel.style.maxHeight = panel.scrollHeight + 'px';
		// }
		if (panel.style.display === 'flex') {
			panel.style.display = 'none';
		} else {
			panel.style.display = 'flex';
		}
	});
}
