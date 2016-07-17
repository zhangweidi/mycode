function getsign(){
  	var jsapi_ticket = 'Xae8ROMhRYO7tZ7MYNxqyQVzTbBzw2ZEQvSBuHZgKC4WCbdsnPlmA2eGDcrGd90a53rWZ0qasEqsHXgin8zc7D';
    var nonceStr = '12345abcde';
    var timeStamp = '1614588745';
    var url = '';

    var plain = 'jsapi_ticket=' + jsapi_ticket ;
    
    alert(plain);
    var sha1 = crypto.createHash('sha1');
    sha1.update(plain, 'utf8');
    var signature = sha1.digest('hex');

    alert(signature);
}

function getDevNum() {
	dev_num = prompt("设备号:","11112222");
	if (dev_num == null)
	{
		alert("不能为空");
	}

	document.getElementById("devnum").value=dev_num;
}




function myFunction()
{
	dev_num = prompt("设备号:","11112222");
	if (dev_num == null)
	{
		alert("不能识别设备编号");
		var myModel = new openerp.web.Model('pratol.recod');
		myModel.call("reset_datainfo", []).then(function(result) {
	    });		
	}
	else
	{
		var myModel = new openerp.web.Model('pratol.recod');
		myModel.call("set_devinfo", [], {devNum:dev_num}).then(function(result) {
	        if (result == "null")
	        	alert("该设备未注册");
	    });   
	}
}

