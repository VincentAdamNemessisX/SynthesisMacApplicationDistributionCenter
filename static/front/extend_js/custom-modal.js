function download_modal(csrftoken, software) {
	let modal_html = `
			<div class="modal-header py-2 modal-header-simple">
				<span></span>
				<div class="text-md"><i class="iconfont icon-down mr-2">
				</i><span class="text-sm">${software.get('name')} - ${software.get('version')}</span>
				</div>
			</div>
	        <div class="p-4">
                <div class="row">
                    <div class="col-6 col-md-7">描述</div>
                    <div class="col-4 col-md-3">下载</div>
                </div>
                <div class="col-12 line-thead my-2" style="height:1px;background: rgba(136, 136, 136, 0.4);"></div>
                <div class="down_btn_list mb-4"></div>
                <div class="io-alert border-2w text-sm" role="alert"><i
                        class="iconfont icon-statement mr-2"></i><strong>声明：</strong>根据中华人民共和国《计算机软件保护条例》第十七条规定：“为了学习和研究软件内含的设计思想和原理，通过安装、显示、传输或者存储软件等方式使用软件的，可以不经软件著作权人许可，不向其支付报酬。”本站大部分下载资源收集于网络，只做学习和交流使用，版权归原作者所有。若您需要使用非免费的软件或服务，请购买正版授权并合法使用。本站发布的内容若侵犯到您的权益，请联系站长删除，我们将及时处理。用户本人下载后不能用作商业或非法用途，需在24小时之内删除，否则后果均由用户承担责任。
                </div>
            </div>`;
	modal_html = modal_html.replace('<div class="down_btn_list mb-4"></div>',
		'<div class="down_btn_list mb-4">' + append_download_links(csrftoken, software)
							+ '</div>');
	Swal.fire({
		width: '70%',
		html: modal_html,
		showConfirmButton: false,
		showCloseButton: true
	});
}

function append_download_links(csrftoken, software) {
	let download_block = '';
	if (software.get('link_adrive') !== '' && software.get('link_adrive') !== 'None' && software.get('link_adrive') !== undefined) {
		download_block += `
		<!--阿里云盘下载行-->
		<div class="row">
		    <div class="col-6 col-md-7">${software.get('name')} - ${software.get('version')}【要改后缀名】</div>
		    <div class="col-4 col-md-3 "><a
		            class="btn btn-danger custom_btn-d py-0 px-1 mx-auto down_count copy-data text-sm"
		            href="${software.get('link_adrive')}" onclick="auto_add_download_volume('${csrftoken.toString()}', ${software.get('id')})" target="_blank"
		            data-mmid="down-mm-0">阿里云盘下载</a>
		    </div>
		</div>
        <div class="col-12 line-thead my-2" style="height:1px;background: rgba(136, 136, 136, 0.2);"></div>
		`;
	}
	
	if (software.get('link_baidu') !== '' && software.get('link_baidu') !== 'None' && software.get('link_baidu') !== undefined) {
		download_block += `
		<!--百度云盘下载行-->
		<div class="row">
		    <div class="col-6 col-md-7">${software.get('name')} - ${software.get('version')}</div>
		    <div class="col-4 col-md-3 "><a
		            class="btn btn-danger custom_btn-d py-0 px-1 mx-auto down_count copy-data text-sm"
		            href="${software.get('link_baidu')}"
		             onclick="auto_add_download_volume(${csrftoken}, ${software.get('id')})"
		             target="_blank"
		            data-mmid="down-mm-0">百度云盘下载</a>
		    </div>
		</div>
        <div class="col-12 line-thead my-2" style="height:1px;background: rgba(136, 136, 136, 0.2);"></div>
		`;
	}
	
	if (software.get('link_direct') !== '' && software.get('link_direct') !== 'None' && software.get('link_direct') !== undefined) {
		download_block += `
		<!--直链下载行-->
		<div class="row">
		    <div class="col-6 col-md-7">${software.get('name')} - ${software.get('version')}</div>
		    <div class="col-4 col-md-3 "><a
		            class="btn btn-danger custom_btn-d py-0 px-1 mx-auto down_count copy-data text-sm"
		            href="${software.get('link_direct')}" target="_blank" onclick="auto_add_download_volume(${csrftoken}, ${software.get('id')})"
		            data-mmid="down-mm-0">本站直链下载</a>
		    </div>
		</div>
        <div class="col-12 line-thead my-2" style="height:1px;background: rgba(136, 136, 136, 0.2);"></div>
		`;
	}
	
	if (software.get('link_123') !== '' && software.get('link_123') !== 'None' && software.get('link_123') !== undefined) {
		download_block += `
		<!--123云盘下载行-->
		<div class="row">
		    <div class="col-6 col-md-7">${software.get('name')} - ${software.get('version')}</div>
		    <div class="col-4 col-md-3 "><a
		            class="btn btn-danger custom_btn-d py-0 px-1 mx-auto down_count copy-data text-sm"
		            href="${software.get('link_123')}" target="_blank"
		            onclick="auto_add_download_volume(${csrftoken}, ${software.get('id')})"
		            data-mmid="down-mm-0">123云盘下载</a>
		    </div>
		</div>
        <div class="col-12 line-thead my-2" style="height:1px;background: rgba(136, 136, 136, 0.2);"></div>
		`;
	}
	return download_block;
}
