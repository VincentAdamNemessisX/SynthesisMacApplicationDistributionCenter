function get_notice_to_all() {
	$.ajax({
		url: "/api/notice/to/all/",
		type: "GET",
		dataType: "json",
		success: function (data) {
			if (data.code === 200) {
				if (data.data.length > 0) {
					if (data.data[0].image == null) {
						Swal.fire({
							title: data.data[0].title,
							html: data.data[0].content + "<br/>更新时间：" +
								toDate(data.data[0].date)
						})
					} else {
						Swal.fire({
							title: data.data[0].title,
							html: data.data[0].content + "<br/>更新时间：" +
								toDate(data.data[0].date),
							width: 800,
							padding: '3em',
							imageUrl: data.data[0].image,
							imageWidth: 400,
							imageHeight: 200,
							imageAlt: '公告图片',
							confirmButtonText: '我已了解！'
						})
					}
				} else {
					Swal.fire({
						icon: 'error',
						title: '出错了，' + data.code,
						text: data.msg + '，API返回数据为空，请联系站长!',
						footer: '<a href="/help">需要帮助?</a>'
					})
				}
			} else {
				Swal.fire({
					icon: 'error',
					title: '出错了',
					text: 'API返回数据异常，请联系站长!',
					footer: '<a href="/help/">需要帮助</a>?'
				})
			}
		}
		,
		error: function (data) {
			if (data) {
				Swal.fire({
					icon: 'error',
					title: '出错了，' + data.code,
					text: data.msg + '，API调用失败，请联系站长!',
					footer: '<a href="/help">需要帮助?</a>'
				})
			} else {
				Swal.fire({
					icon: 'error',
					title: '出错了',
					text: '后台严重异常，请联系站长!',
					footer: '<a href="/help">需要帮助?</a>'
				})
			}
		}
	})
}

function get_notice_to_specific_app(app_id) {
	$.ajax({
		url: "/api/notice/to/specific/app/",
		type: "GET",
		data: {'app_id': app_id},
		dataType: "json",
		success: function (data) {
			if (data.code === 200) {
				if (data.data.length > 0) {
					if (data.data[0].image == null) {
						Swal.fire({
							title: data.data[0].title,
							html: data.data[0].content + "<br/>更新时间：" +
								toDate(data.data[0].date),
							width: 800,
							padding: '3em',
							confirmButtonText: '我已知晓！'
						})
					} else {
						Swal.fire({
							title: data.data[0].title,
							html: data.data[0].content + "<br/>更新时间：" +
								toDate(data.data[0].date),
							width: 800,
							padding: '3em',
							imageUrl: data.data[0].image,
							imageWidth: 400,
							imageHeight: 200,
							imageAlt: '公告图片',
							confirmButtonText: '我已了解！'
						})
					}
				} else {
					Swal.fire({
						icon: 'error',
						title: '出错了，' + data.code,
						text: data.msg + '，API返回数据为空，请联系站长!',
						footer: '<a href="/help">需要帮助?</a>'
					})
				}
			} else {
				Swal.fire({
					icon: 'error',
					title: '出错了',
					text: 'API返回数据异常，请联系站长!',
					footer: '<a href="/help/">需要帮助</a>?'
				})
			}
		}, error: function (data) {
			if (data) {
				Swal.fire({
					icon: 'error',
					title: '出错了，' + data.code,
					text: data.msg + '，API调用失败，请联系站长!',
					footer: '<a href="/help">需要帮助?</a>'
				})
			} else {
				Swal.fire({
					icon: 'error',
					title: '出错了',
					text: '后台严重异常，请联系站长!',
					footer: '<a href="/help">需要帮助?</a>'
				})
			}
		}
	})
}

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