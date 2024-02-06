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
