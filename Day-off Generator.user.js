// ==UserScript==
// @name         Day-off Generator
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Automatically change the time of the day-off pages so that you can freely walk off the school.
// @author       Ki Seki
// @match        *://49.122.0.29:8002/*
// @icon         
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    setInterval(function(){
        // get dates and time
        var today = new Date(), yesterday = new Date(), s_td, s_yd, time;
        today.setTime(today.getTime());
        yesterday.setTime(yesterday.getTime()-24*60*60*1000);
        s_td = today.getFullYear()+"-" + (today.getMonth()+1) + "-" + today.getDate();
        s_yd = yesterday.getFullYear()+"-" + (yesterday.getMonth()+1) + "-" + yesterday.getDate();
        time = "09:06:04";
        // selectors
        var s1 = "[name=qjsqForm] > div:nth-child(5) > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(3) > td:nth-child(2)"; // 请假开始时间
        var s2 = "[name=qjsqForm] > div:nth-child(5) > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(3) > td:nth-child(4)"; // 请假结束时间
        var s3 = "#shlccx_table > tbody > tr:nth-child(2) > td:nth-child(5)"; // 审核时间
        document.querySelector(s1).innerHTML = s_td;
        document.querySelector(s2).innerHTML = s_td;
        document.querySelector(s3).innerHTML = s_yd + " " + time;
    }, 1000);
})();