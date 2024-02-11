function thumb_software_or_not(csrf_token, thumb_type, software_id) {
	$.ajax({
		url: '/software/api/thumb/',
		type: 'POST',
		dataType: 'json',
		data: {
			csrfmiddlewaretoken: csrf_token,
			thumb_type: thumb_type,
			software_id: encrypt_param(software_id.toString())
		},
		success: function (data) {
			if (data.code === 200) {
				let tt = '';
				if (thumb_type === 'thumb') {
					tt = '点赞成功！';
				} else if (thumb_type === 'de_thumb') {
					tt = '取消点赞成功';
				} else {
					tt = 'unknown request'
				}
				Swal.fire({
					icon: 'success',
					title: tt,
				}).then(function () {
					let t = document.getElementById('software-' + software_id);
					if (thumb_type === 'thumb') {
						t.setAttribute('onclick', "thumb_software('" + software_id + "',2)")
						t.children[1].innerText = parseInt(t.children[1].innerText) + 1;
					} else if (thumb_type === 'de_thumb') {
						t.setAttribute('onclick', "thumb_software('" + software_id + "',1)")
						t.children[1].innerText = parseInt(t.children[1].innerText) - 1;
					}
				})
			} else {
				Swal.fire({
					icon: 'error',
					title: '出错了',
					text: "错误代码" + data.code + "," + data.error + "!",
					footer: '<a href="/help">需要帮助?</a>'
				})
			}
		},
		error: function (data) {
			Swal.fire({
				icon: 'error',
				title: '出错了',
				text: '后台严重异常，请联系站长!',
				footer: '<a href="/help">需要帮助?</a>'
			})
		}
	})
}