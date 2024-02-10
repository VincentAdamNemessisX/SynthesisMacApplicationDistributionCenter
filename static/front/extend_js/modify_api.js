function thumb_software_or_not(csrf_token, thumb_type, software_id) {
	let flag = false;
	$.ajax({
		url: 'software/api/thumb/',
		type: 'POST',
		dataType: 'json',
		data: {
			csrfmiddlewaretoken: csrf_token,
			thumb_type: thumb_type,
			sotware_id: software_id
		},
		success: function (data) {
			if (data.code === 200) {
				Swal.fire({
					icon: 'success',
					title: '点赞成功',
				})
				flag = true;
			} else {
				Swal.fire({
					icon: 'error',
					title: '出错了',
					text: "错误代码" + data.code + "," + data.error + "!",
					footer: '<a href="/help">需要帮助?</a>'
				})
				flag = false;
			}
		},
		error: function (data) {
			Swal.fire({
				icon: 'error',
				title: '出错了',
				text: '后台严重异常，请联系站长!',
				footer: '<a href="/help">需要帮助?</a>'
			})
			flag = false;
		}
	})
	return flag;
}