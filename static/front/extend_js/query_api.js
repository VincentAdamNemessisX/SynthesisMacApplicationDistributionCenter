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
							width: '70%',
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
			software_id: encrypt_param(software_id.toString())
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
							width: '70%',
							padding: '3em',
							confirmButtonText: '我已知晓！'
						})
					} else {
						Swal.fire({
							title: data.data[0].title,
							html: data.data[0].content + "<br/><p style='color: #999999'>更新时间：" +
								toDate(data.data[0].created_time) + "</p>",
							width: '70%',
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
	let url = ''; //初始化url
	if (init === 1) { //根据init参数决定请求的url
		url = '/commentswitharticles/api/get/init/comments/';
	} else if (init === 0) {
		url = '/commentswitharticles/api/load/more/comments/';
	}
	if (csrftoken === '' || csrftoken === null || csrftoken === undefined) {
		console.error('csrftoken missed')
		return null;
	}
	if (type === '' || type === null || type === undefined) {
		console.error('request type missed')
		return null;
	}
	if (query_id === '' || query_id === null || query_id === undefined) {
		console.log('request query id missed')
		return null;
	}
	let data = {
		query_id: query_id.toString(),
		type: type.toString(),
	}; //封装请求体数据
	return await fetch(url, { //返回promise供后续代码调用fetch得到的数据
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
		.then((response) => response.json()) //转化返回结果为json数据
		.then((full_data) => { //取得json数据并根据数据提供的code代码决定返回数据或者异常字符串
			if (parseInt(full_data.code) === 200) {
				return full_data.data;
			} else {
				console.log(full_data.code + ":" + full_data.msg);
				return null;
			}
		})
		.catch((error) => { //捕获fetch过程中可能会碰到的异常并将其输出在控制台
			console.error("Error:", error);
		}); //返回promise以供后续代码使用promise链式访问其中数据
}

function get_category_tags(csrf_token, category_id) {
	$.ajax({
		url: "/category/api/get/category/tags/",
		type: "POST",
		dataType: "json",
		data: {
			category_id: category_id,
			csrfmiddlewaretoken: csrf_token
		},
		success: function (data) {
			if (data.code === 200) {
				let tags = data.data;
				let tag_html = '';
				if (tags !== undefined && tags !== null && tags.length > 0) {
					for (let i = 0; i < tags.length; i++) {
						tag_html += `
                            <li class="pagenumber nav-item">
                                <a class="nav-link tab-noajax active load"
                                   data-toggle="pill"
                                   href="#tab-${30 * (i+1)}-${30 * (i+1)}">${tags[i].name}</a>
                            </li>
						`;
					}
					document.querySelector('#category-tags').innerHTML += tag_html;
				} else {
					document.querySelector('#category-tags').parentElement.parentElement.remove();
				}
			}
		},
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