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

async function thumb_article_or_not(csrftoken, type, article_id) {
	let url = '/commentswitharticles/api/thumb/article/'; //初始化url
	let data = {
		article_id: encrypt_param(article_id.toString()),
		thumb_type: type.toString(),
	}; //封装请求体数据
	return await fetch(url, { //返回promise供后续代码调用fetch得到的数据
		method: 'POST', // 指定请求方法
		mode: 'cors', // 请求的模式
		cache: 'default', // 缓存模式
		credentials: 'same-origin', // 是否应该发送Cookie
		headers: {
			'Content-Type': 'application/json', // 请求的内容类型
			'X-CSRFToken': csrftoken.toString() // CSRF令牌
		},
		redirect: 'follow', // 重定向模式
		referrerPolicy: 'no-referrer', // 引用策略
		body: JSON.stringify(data) // 请求的body
	})
		.then((response) => response.json()) //转化返回结果为json数据
		.then((full_data) => { //取得json数据并根据数据提供的code代码决定返回数据或者异常字符串
			let returned_code = parseInt(full_data.code);
			if (returned_code === 200) {
				let tt = '';
				if (type === 'thumb') {
					tt = '点赞成功！';
				} else if (type === 'de_thumb') {
					tt = '取消点赞成功';
				} else {
					tt = 'unknown request';
				}
				Swal.fire({
					icon: 'success',
					title: tt,
				}).then(function () {
					let t = document.getElementById('article-' + article_id);
					if (type === 'thumb') {
						t.setAttribute('onclick', "thumb_article('" + article_id + "',2)")
						t.children[1].innerText = parseInt(t.children[1].innerText) + 1;
					} else if (type === 'de_thumb') {
						t.setAttribute('onclick', "thumb_article('" + article_id + "',1)")
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
		})
		// .catch((error) => { //捕获fetch过程中可能会碰到的异常并将其输出在控制台
		// 		Swal.fire({
		// 			icon: 'error',
		// 			title: '出错了',
		// 			text: "错误代码" + error.code + "," + error.msg + "!",
		// 			footer: '<a href="/help">需要帮助?</a>'
		// 		})
		// }); //返回promise以供后续代码使用promise链式访问其中数据
}

function load_img(file) {

}

function unload_img(src){

}