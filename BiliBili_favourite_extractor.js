// 自动提取 B 站个人收藏页面中所有视频的链接
// 打开 B 站收藏页面，在控制台粘贴以下代码，回车，等待五秒即可
// 结合 Python 包 you-get，即可下载所有链接对应的视频

function get_list() {
    var result = "";
    $(".fav-video-list > li > a.title").each(function() {
        result += '&nbsp;<a href="' + $(this).attr("href") + '" target=_blank>https:' + $(this).attr("href") + '</a>&nbsp;';
    });
    return result;
}
var html = "";

function main() {
    html += get_list();
    if ($(".be-pager-next:visible").length == 0) {
        document.write(html);
        return;
    } else {
        $(".be-pager-next").click();
        setTimeout("main()", 5000);
    }
}
main();