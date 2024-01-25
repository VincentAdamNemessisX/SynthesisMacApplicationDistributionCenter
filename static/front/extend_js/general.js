function toDate(dateStr) {
	let date = new Date(dateStr);
	let year = date.getFullYear();
	let month = date.getMonth() + 1;
	let day = date.getDate();
	let hour = date.getHours();
	let minute = date.getMinutes();
	let seconds = date.getSeconds();
	return year + "年" + month + "月" + day + "日"
		+ hour + "时" + minute + "分" + seconds + "秒";
}