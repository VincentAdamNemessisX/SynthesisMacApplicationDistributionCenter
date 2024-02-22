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

function encrypt_param(str) {
// 加密密钥，必须为16、24或32位，对应AES-128、AES-192或AES-256
	const key = CryptoJS.enc.Utf8.parse('frontendencryptx');
// 加密向量，必须为16位
	const iv = CryptoJS.enc.Utf8.parse('frontendencryptx');
// 进行AES加密
	const ciphertext = CryptoJS.AES.encrypt(str, key, {
		iv: iv,
		mode: CryptoJS.mode.CBC,
		padding: CryptoJS.pad.Pkcs7
	});
// 输出密文
// 	console.log(ciphertext.toString());
	return ciphertext.toString();
}

function decrypt_param(str) {
// 加密密钥，必须为16、24或32位，对应AES-128、AES-192或AES-256
	const key = CryptoJS.enc.Utf8.parse('frontendencryptx');
// 加密向量，必须为16位
	const iv = CryptoJS.enc.Utf8.parse('frontendencryptx');
	// 进行AES解密
	const bytes = CryptoJS.AES.decrypt(str, key, {
		iv: iv,
		mode: CryptoJS.mode.CBC,
		padding: CryptoJS.pad.Pkcs7
	});
// 将解密后的结果转换为字符串
	const decryptedText = bytes.toString(CryptoJS.enc.Utf8);
// 输出明文
// 	console.log(decryptedText);
	return decryptedText;
}


function split_tags(tags) {
	// 分词
	let x = tags.split(';');
	// 去重
	x = [...new Set(x)];
	// 去空
	return x.filter(function (t) {
		return t && t.trim();
	});
}

function generateCurrentPageQrcode() {
	// 生成当前页面二维码
	return new QRCode(document.getElementById("qr_code"), {
		text: window.location.href,
		width: 128,
		height: 128,
		colorDark: "#000000",
		colorLight: "#ffffff",
		correctLevel: QRCode.CorrectLevel.H
	});
}

function formatTimePeriod(timePeriod) {
	const seconds = Math.floor(timePeriod / 1000);
	const minutes = Math.floor(seconds / 60);
	const hours = Math.floor(minutes / 60);
	const days = Math.floor(hours / 24);
	const weeks = Math.floor(days / 7);
	const months = Math.floor(days / 30);
	const years = Math.floor(days / 365);
	
	if (years > 0) {
		return `${years}年前`;
	} else if (months > 0) {
		return `${months}个月前`;
	} else if (weeks > 0) {
		return `${weeks}周前`;
	} else if (days > 0) {
		return `${days}天前`;
	} else if (hours > 0) {
		return `${hours}小时前`;
	} else if (minutes > 0) {
		return `${minutes}分钟前`;
	} else if (seconds > 0) {
		return `${seconds}秒前`;
	} else {
		console.error('非法篡改时间！timePeriod is invalid!');
		return '非法篡改时间！';
	}
}