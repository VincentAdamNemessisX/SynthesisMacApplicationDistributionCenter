// 用于获取API数据
async function get_notice_to_all(csrftoken) {
	$.ajax({
		url: "/announcements/api/notice/to/all/",
		type: "POST",
		dataType: "json",
		data: {
			csrfmiddlewaretoken: csrftoken
		},
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

function get_notice_to_specific_app(csrftoken, software_id) {
	$.ajax({
		url: "/announcements/api/notice/to/specific/software/",
		type: "POST",
		data: {
			csrfmiddlewaretoken: csrftoken,
			software_id: software_id
		},
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
				}
			} else {
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


async function get_comments_for_software_or_articles(csrftoken, type, query_id, init = 1) {
	let url = '';
	if (init === 1) {
		url = '/commentswitharticles/api/get/init/comments/';
	} else if (init === 0) {
		url = '/commentswitharticles/api/load/more/comments/';
	}
	let data = {
		query_id: query_id.toString(),
		type: type.toString(),
	};
	let response = await fetch(url, {
		method: 'POST', // 指定请求方法
		mode: 'cors', // 请求的模式
		cache: 'default', // 缓存模式
		credentials: 'same-origin', // 是否应该发送Cookie
		headers: {
			'Content-Type': 'application/json', // 请求的内容类型
			'X-CSRFToken': csrftoken // CSRF令牌
		},
		redirect: 'follow', // 重定向模式
		referrerPolicy: 'no-referrer', // 引用策略
		body: JSON.stringify(data) // 请求的body
	})
		.then((response) => response.json())
		.then((full_data) => {
			if(parseInt(full_data.code) === 200) {
				return full_data.data;
			} else {
				return full_data.code + ":" + full_data.msg;
			}
		})
		.catch((error) => {
			console.error("Error:", error);
		});
	return response;
}