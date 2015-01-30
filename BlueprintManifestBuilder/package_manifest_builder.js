

/* Generate guuid

   'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
       var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
       return v.toString(16);
   });
*/

/******* Setup parameters ******/
$("#chooser_container .parameter").draggable({
	revert: "invalid",
	helper: "clone",
	cancel: "",
});

$("#built_els").droppable({
	accept: ".parameter",
	hoverClass: "built_parameter_hover",
	drop:  function(event,ui){
		switch(ui.draggable[0].id)  {
			case 'param_string':
		};
	},
});




/******* Bootstrap ******/
uuid_el = $("#builder_el_tpl").clone().removeAttr("id");
uuid_el.find(".el_btn_menu").html("");
uuid_el.find(".name_span").html("UUID").show();
uuid_el.find("input.name").removeClass("col-md-2").addClass("col-md-10").val('xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
	var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
	return v.toString(16);
}));
uuid_el.find("input.example_field").remove();
uuid_el.find(".el_details").remove();
uuid_el.find(".el_help").removeClass("col-md-offset-1").removeClass("col-md-5").addClass("col-md-11").html("Each package must have a globally unique 32 character GUID.  A new value has been generated for you.  If this is replacing an existing package place update with your current GUID.  Blueprints connect to Packages using this GUID so to prevent breaking for minior changes reuse the GUID.  Likewise to create a new incompatible package release choose a new GUID.");
uuid_el.appendTo("#built_els").show();

name_el = $("#builder_el_tpl").clone().removeAttr("id");
name_el.find(".el_btn_menu").html("");
name_el.find(".name_span").html("Name").show();
name_el.find("input.name").removeClass("col-md-2").addClass("col-md-10").attr("placeholder","Package Name");
name_el.find("input.example_field").remove();
name_el.find(".el_details").remove();
name_el.find(".el_help").removeClass("col-md-offset-1").removeClass("col-md-5").addClass("col-md-11").html("Package name.  This is searchable and displayed when choosing the package.  CenturyLink has defined a <a href='https://t3n.zendesk.com/entries/56566304-Creating-Public-Blueprint-Packages'>naming standard for public packages</a> which you may leverage.");
name_el.appendTo("#built_els");

description_el = $("#builder_el_tpl").clone().removeAttr("id");
description_el.find(".el_btn_menu").html("");
description_el.find(".name_span").removeClass("col-md-2").addClass("col-md-12").html("Package Description").show();
description_el.find("input.name").remove();
description_el.find("input.example_field").remove();
description_el.find(".el_help").remove();
description_el.find(".el_details").removeClass("col-md-5").addClass("col-md-12").html("<textarea style='width: 100%; height: 6em;' placeholder='Enter package description'></textarea>");
description_el.appendTo("#built_els");

