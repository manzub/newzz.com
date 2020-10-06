var tl = window.location.pathname
var at = /signup?(.*)/.exec(tl)
if(at!=null){
    var ttl = window.location.pathname == '/login' ? 'login' : at[0]
}else{
    var ttl = window.location.pathname
}
if(ttl != 'login' && ttl != 'signup'){
    if(!document.getElementById('ECKckuBYwZaP')){
        document.getElementsByTagName('body')[0].innerHTML = "<p>Please Disable Ad Blocker</p>"
    } 
}
var nav_links=[document.getElementsByClassName("nav__link")[0],document.getElementsByClassName("nav__link")[1]];function closeToasti(t){var a=document.getElementById(t);a.parentNode.removeChild(a)}function showToasti(t=[]){for(var a=0;a<t.length;a++)document.getElementsByTagName("body")[0].innerHTML+=""+`<div id="toasti${a}" class="toasti">\n        <div class="toasti-body">\n            <span>${t[a]}</span>\n            <span onclick="closeToasti('toasti${a}')" class="toasti-close">&times;</span>\n        </div>\n    </div>`}function addbalance(t){var a=JSON.parse(sessionStorage.getItem("is_read")),e=[];for(let t=0;t<a.length;t++)e.push(a[t]);$.ajax({url:"/api/add_balance/1",type:"GET",data:"",success:function(a){1==a.status&&(e.push(parseInt(t)),sessionStorage.setItem("is_read",JSON.stringify(e)),showToasti([a.message]))}})}if(document.getElementsByClassName("nav__link")[0]&&nav_links.forEach(function(t){t.getAttribute("href")==window.location.pathname&&(t.className+=" --active")}),$(document).ready(function(){setTimeout(function(){$(".preloader").fadeOut("slow")},700)}),$(function(){$("div.newzz-card").click(function(t){var a=$(this).attr("href");return window.location.href=a,!1})}),$(function(){var t=window.location.pathname,a=/read(.*)/.exec(t);if(null!=a){var e=0;!function(){var t=document.getElementsByClassName("timeout-bar")[0],s=0,n=setInterval(function(){s>=100?(clearInterval(n),$(window).scroll(function(){if($(window).scrollTop()+$(window).height()>$(document).height()-100){var t=JSON.parse(sessionStorage.getItem("is_read"));if(0==e){var s=a[1].split("/")[1];e+=1,null!=t?t.includes(parseInt(s))?showToasti(["Reward Already claimed"]):addbalance(s):(sessionStorage.setItem("is_read",JSON.stringify([0])),addbalance(s))}}})):(s++,t.style.width=s+"%")},80)}()}}),"/cashout"==window.location.pathname){var cashout_opt={amount:"",opt:""};$("#amount_to1").click(function(t){$("#amount_to3").removeClass(" selected"),$("#amount_to2").removeClass(" selected"),$(this).addClass(" selected"),cashout_opt.amount=1}),$("#amount_to2").click(function(t){$("#amount_to1").removeClass(" selected"),$("#amount_to3").removeClass(" selected"),$(this).addClass(" selected"),cashout_opt.amount=2}),$("#amount_to3").click(function(t){$("#amount_to1").removeClass(" selected"),$("#amount_to2").removeClass(" selected"),$(this).addClass(" selected"),cashout_opt.amount=3}),$("#payopt_to").click(function(t){$(this).addClass(" selected"),cashout_opt.opt=$(this).attr("data-opt")}),$("#cashout").click(function(t){$.ajax({url:"/api/cashout/"+parseInt(cashout_opt.opt),type:"GET",data:"",success:function(t){t&&showToasti([t.message])}})})}function all_cashouts(t=0){if("/admin/mynewzzadmin"==window.location.pathname){var a=document.getElementById("all_cashouts_div"),e=document.getElementById("rows");e.innerHTML="LOADING...",$.ajax({url:"/api/all_cashouts/"+t,type:"GET",data:"",success:function(t){if(e.innerHTML="",a)if(t.length>0)for(let a=0;a<t.length;a++)e.innerHTML+=`<tr>\n                                <td>${a+1}</td>\n                                <td>${t[a].user_email}</td>\n                                <td>$${parseInt(t[a].amount)/1e5}</td>\n                                <td>${t[a].payout_type}</td>\n                                <td><button class='btn btn-success' id='accept-req' data-id='${t[a].id}'>ACCEPT</button></td>\n                                <td><button class='btn btn-danger' id='reject-req' data-id='${t[a].id}'>REJECT</button></td>\n                            </tr>`;else e.innerHTML+="<td colspan='5'>No Requests Available</td>"}})}}all_cashouts(),$(document).on("click","button#accept-req",function(t){var a=$(this).attr("data-id");$.ajax({url:"/api/cashout_actions/"+a,type:"POST",data:"",success:function(t){all_cashouts(),showToasti([t.message])}})}),$(document).on("click","button#reject-req",function(t){console.log("reject");var a=$(this).attr("data-id");$.ajax({url:"/api/cashout_actions/"+a,type:"DELETE",data:"",success:function(t){all_cashouts(),showToasti([t.message])}})});
var dir_link='//graizoah.com/afu.php?zoneid=3608293'
var ads_div = document.querySelectorAll('.display-ads')
for(let i=0;i<ads_div.length;i++){
    ads_div[i].onclick = function(){ad2content();}
}
var count_dads = 0
function ad2content(){
    if (count_dads < 2) {
        count_dads+=1
        window.open(dir_link,"ad")
    }else if (count_dads == 2){
        $.ajax({
            url:'/api/add_balance/2',
            type:'GET',
            data:'',
            success:function(data){
                showToasti([data.message])
            }
        })
    }
}
function copyRefLink(){
    var ref_link  = document.getElementsByClassName('ref-link')[0].innerText
    var elem = document.createElement('textarea')
    document.body.appendChild(elem)
    elem.value = ref_link
    elem.select()
    document.execCommand('copy')
    document.body.removeChild(elem)
    document.getElementsByClassName('tooltiptext')[0].innerText = 'copied'
}

if(document.getElementsByClassName('pagination')[0]){
    var ul = document.getElementsByClassName('pagination')[0]
    $.ajax({
        url:'/api/pages',
        type:'GET',
        data:'',
        success:function(data){
            for(let i=0;i<data.pages.length;i++){
                ul.innerHTML += '<li class="page-item"><a onclick="all_cashouts(10*parseInt('+i+'))" class="page-link">'+i+'</a></li>'
            }
        }
    })
}