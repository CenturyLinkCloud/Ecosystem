

/* Generate guuid

   'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
       var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
       return v.toString(16);
   });
*/


/******* Bootstrap ******/
uuid_el = $("#builder_el_tpl").clone().removeAttr("id");
uuid_el.find(".el_btn_menu").html("");
uuid_el.find(".name_span").html("UUID");
uuid_el.find("input.name").val("uuid").hide();
uuid_el.find(".el_details").html("");
uuid_el.find(".el_help").html("Each package must have a globally unique 32 character GUID.  A new value has been generated for you.  If this is replacing an existing package place update with your current GUID.  Blueprints connect to Packages using this GUID so to prevent breaking for minior changes reuse the GUID.  Likewise to create a new incompatible package release choose a new GUID.");
uuid_el.appendTo("#built_els").show();

name_el = $("#builder_el_tpl").clone().removeAttr("id");
name_el.find(".el_btn_menu").html("");
name_el.find(".el_details").html("");
name_el.appendTo("#built_els");

description = $("#builder_el_tpl").clone().removeAttr("id");
description.appendTo("#built_els");


