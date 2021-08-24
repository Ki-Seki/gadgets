// 打开 B 站收藏页面，在控制台粘贴以下代码，回车，等待五秒即可

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