// 用于获取API数据
function get_notice_to_all() {
	$.ajax({
		url: "/announcements/api/notice/to/all/",
		type: "GET",
		dataType: "json",
		success: function (data) {
			if (data.code === 200) {
				if (data.data.length > 0) {
					if (data.data[0].image == null) {
						Swal.fire({
							title: data.data[0].title,
							html: data.data[0].content + "<br/><p style='color: #999999'>更新时间：" +
								toDate(data.data[0].created_time) + "</p>",
						})
					} else {
						Swal.fire({
							title: data.data[0].title,
							html: data.data[0].content + "<br/><p style='color: #999999'>更新时间：" +
								toDate(data.data[0].created_time) + "</p>",
							width: 800,
							padding: '3em',
							imageUrl: data.data[0].image,
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
		url: "/announcements/api/notice/to/specific/app/",
		type: "GET",
		data: {'app_id': app_id},
		dataType: "json",
		success: function (data) {
			if (data.code === 200) {
				if (data.data.length > 0) {
					if (data.data[0].image == null) {
						Swal.fire({
							title: data.data[0].title,
							html: data.data[0].content + "<br/><p style='color: #999999'>更新时间：" +
								toDate(data.data[0].created_time) + "</p>",
							width: 800,
							padding: '3em',
							confirmButtonText: '我已知晓！'
						})
					} else {
						Swal.fire({
							title: data.data[0].title,
							html: data.data[0].content + "<br/><p style='color: #999999'>更新时间：" +
								toDate(data.data[0].created_time) + "</p>",
							width: 800,
							padding: '3em',
							imageUrl: data.data[0].image,
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