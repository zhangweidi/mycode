(function(){
    'use strict';

    var website = openerp.website;
    var _t = openerp._t;

    $(document).on('click', '.btn-factory-add', function (event) {
        var name = document.getElementById('fullname1').value;
        var person_id = document.getElementById('person_id1').value;
        console.log('ok');
        openerp.jsonRpc('/factory/adds', 'call', {'name': name, 'person_id': person_id}).then(function (data) {
            console.log(data);
            //dd.config({
            //    name: name,
            //    person_id: person_id,
            //    //signature: data,
            //});

        });
         alert("提交成功");
    });
    $(document).on('click', '.btn-factory-continue', function (event) {
    	//var name = '章玮迪';
    	//var person_id = '510108199511069878';

        //openerp.jsonRpc('/factory/check/', 'call', {}).then(function (data) {
        //	dd.config({
    		//    name: name,
    		//    person_id: person_id,
    		//    //signature: data,
    		//});

        alert("搜索完毕");

        });
})();

