

$("#welcome_modal").modal('show');

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
			// Standard Params
			case 'param_string':
				/* TODO - move to custom and apply regex option */
				GenerateGenericParamEl(ui.draggable[0].id,ui.helper,"Free-form string.","String");
				break;
			case 'param_numeric':
				GenerateGenericParamEl(ui.draggable[0].id,ui.helper,"Numeric string.","Numeric");
				break;
			case 'param_password':
				GenerateGenericParamEl(ui.draggable[0].id,ui.helper,"Numeric string.","Password");
				break;
			case 'param_network':
				GenerateGenericParamEl(ui.draggable[0].id,ui.helper,"Drop down to select an available network.","Network");
				break;
			case 'param_serverip':
				GenerateGenericParamEl(ui.draggable[0].id,ui.helper,"Drop down to select an available server - both already existing and those scheduled to be built with the current Blueprint.  Returns the IP address of the selected server.","ServerIP");
				break;
			case 'param_server':
				GenerateGenericParamEl(ui.draggable[0].id,ui.helper,"Drop down to select an available server - both already existing and those scheduled to be built with the current Blueprint.  Returns the name selected server.","Server");
				break;

			// System params.  These don't need any el_details
			// TODO - add hidden name parameter to these on construction
			case 'param_user':
				GenerateSystemParamEl(ui.draggable[0].id,ui.helper,"Include the control portal username that is initiating the deployment.","T3.Identity.User");
				break;
			case 'param_name':
				GenerateSystemParamEl(ui.draggable[0].id,ui.helper,"Include the name of server deployment is executing on.","T3.Server.Name");
				break;
			case 'param_ip':
				GenerateSystemParamEl(ui.draggable[0].id,ui.helper,"Include the IP of server deployment is executing on.","T3.Server.IPAddress");
				break;
			case 'param_serverpassword':
				GenerateSystemParamEl(ui.draggable[0].id,ui.helper,"Include the password for the server on which the deployment is executing.","T3.Server.Password");
				break;

			// Option params
			case 'param_select':
				GenerateOptionParamEl(ui.draggable[0].id,ui.helper,"Select one option from a list of several.","MultiSelect");
				break;
			case 'param_option':
				GenerateOptionParamEl(ui.draggable[0].id,ui.helper,"Select zero or more options from a list of several.","Option");
				break;
		};
	},
});



function GenerateGenericParamEl(src_id,example_el,help_text,type)
{
	el = $("#builder_el_tpl").clone().removeAttr("id").addClass(src_id);
	el.find(".example_field").append(example_el[0].innerHTML);
	el.find("input[name=type]").val(type);
	el.find(".el_help").prepend(help_text);
	el.appendTo("#built_els");
}


function GenerateSystemParamEl(src_id,example_el,help_text,name)
{
	el = $("#builder_el_tpl").clone().removeAttr("id").addClass(src_id);
	el.find(".example_field").append(example_el[0].innerHTML);
	el.find("input[name=name]").val(name).attr("disabled","true");
	el.find(".el_details").hide();
	el.find(".el_help").removeClass("col-md-offset-1").removeClass("col-md-5").addClass("col-md-11").html(help_text);
	el.find("select[name=prompt]").val("None");
	el.find("input[name=type]").val("String");
	el.appendTo("#built_els");
}


function GenerateOptionParamEl(src_id,example_el,help_text,type)
{
	el = $("#builder_el_tpl").clone().removeAttr("id").addClass(src_id);
	el.find(".example_field").append(example_el[0].innerHTML);
	el.find("input[name=type]").val(type);
	el.find(".el_help").prepend(help_text);
	if (type == "MultiSelect")  el.find(".frm_default").hide();
	el.find(".el_details").append($("#options_tpl").clone().removeAttr("id"));
	el.appendTo("#built_els");
}



/******* Panel accordions ******/
$("#built_els").on("click",".builder_el .panel-heading",function(e){
	if ($(e.target).hasClass(".el_btn_menu") || $(e.target).parents(".el_btn_menu").length)  {
		// no-op - clicking the button menu
	}  else if ($(e.target).hasClass("name") && !$(this).parents(".builder_el").hasClass("inactive"))  {
		// no-op - editting name field and already expanded
	}  else if ($(this).parents(".builder_el").hasClass("inactive"))  {
		$("#built_els .builder_el").addClass("inactive").removeClass("panel-info");
		$(this).parents(".builder_el").toggleClass("inactive").toggleClass("panel-info");
	}  else  {
		$(this).parents(".builder_el").toggleClass("inactive").toggleClass("panel-info");
	}
});


/******* Button click handlers  ******/
$("#foundation_advanced_btn").click(function(){
	$(this).remove();
	$("#builder_el_preamble .advanced").show();
});
$("#mode").change(function(){
	$("#command").val($("select[name=package_mode]").val()=="Ssh"? "install.sh":"install.ps1");
});

$("#built_els").on("click",".delete_btn",function(){
	$(this).parents(".builder_el").remove();
}).on("click",".clone_btn",function(){
	$(this).parents(".builder_el").clone().insertAfter($(this).parents(".builder_el"));
}).on("click",".remove_option_btn",function(){
	$(this).parent().remove();
}).on("click",".add_option_btn",function(){
	el = $(this).prev().clone();
	el.find("input").val("");
	el.insertBefore(this);
});


/******* Bootstrap ******/
$("#uuid").val('xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
	var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
	return v.toString(16);
}));


/******* Data extract ******/
$("#export_bash_btn").click(function(){
	manifest_obj = BuildManifest();
	if (!manifest_obj)  return(false);

	// Edit content
	install_sh = install_sh_tpl
	variables = Array();
	$.each(manifest_obj.variables,function(i){
		variables.push(this.toUpperCase()+"=\"${"+(i+1)+"}\"\n");
	});
	install_sh = install_sh.replace(/<BEGINVARIABLES>/g,variables.join(""));

	// Publish Gist
	PublishGist(manifest_obj.execution.command_script,manifest_obj.metadata.name+" "+manifest.execution.command_script+" Template File",install_sh)
});


$("#export_powershell_btn").click(function(){
	manifest_obj = BuildManifest();
	if (!manifest_obj)  return(false);

	// Edit content
	install_ps1 = install_ps1_tpl
	variables = Array();
	$.each(manifest_obj.variables,function(i){
		variables.push("	[string]$"+this.toUpperCase()+" = \"\"");
	});
	install_ps1 = install_ps1.replace(/<BEGINVARIABLES>/g,variables.join(",\n"));

	// Publish Gist
	PublishGist(manifest_obj.execution.command_script,manifest_obj.metadata.name+" "+manifest.execution.command_script+" Template File",install_ps1)
});


$("#export_xml_btn").click(function(){
	manifest_obj = BuildManifest();
	if (!manifest_obj)  return(false);

	// Generate XML
	parameters = Array();
	$.each(manifest_obj.parameters,function(i,o){
		switch (o.type)  {
			case 'String':
			case 'Numeric':
			case 'Network':
			case 'Password':
			case 'Server':
			case 'ServerIP':
				parameters.push("        <Parameter Name=\""+o.name+"\" Hint=\""+o.hint+"\" Type=\""+o.type+"\" Variable=\""+o.variable+"\" Prompt=\""+o.prompt+"\" Global=\""+o.global+"\" Default=\""+o.default+"\" Required=\""+o.required+"\"/>");
				break;

			case 'Option':
			case 'MultiSelect':
				options = Array()
				$.each(o.options,function(){
					options.push("            <Option Name=\""+this.name+"\" Value=\""+this.value+"\"/>\n");
				});
				parameters.push("        <Parameter Name=\""+o.name+"\" Hint=\""+o.hint+"\" Type=\""+o.type+"\" Variable=\""+o.variable+"\" Prompt=\""+o.prompt+"\" Global=\""+o.global+"\" Default=\""+o.default+"\" Required=\""+o.required+"\">\n"+options.join("")+"        </Parameter>\n");
				break;
		};
	});
	manifest = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
	          +"<Manifest>\n"
			  +"    <Metadata>\n"
			  +"        <UUID>"+manifest_obj.metadata.uuid+"</UUID>\n"
			  +"        <Name>"+manifest_obj.metadata.name+"</Name>\n"
			  +"        <Description>"+manifest_obj.metadata.description+"</Description>\n"
			  +"    </Metadata>\n"
			  +"    <Parameters>\n"
			  +     parameters.join("\n") + "\n"
			  +"    </Parameters>\n"
			  +"    <Execution>\n"
			  +"        <Mode>"+manifest_obj.execution.mode+"</Mode>\n"
			  +"        <Command>"+manifest_obj.execution.command+"</Command>\n"
			  +"        <Persistent>"+manifest_obj.execution.persistent+"</Persistent>\n"
			  +"        <RebootOnSuccess>"+manifest_obj.execution.reboot_on_success+"</RebootOnSuccess>\n"
			  +"    </Execution>\n"
	          +"</Manifest>\n";

	// Publish Gist
	PublishGist('package.manifest',manifest_obj.metadata.name+" package.manifest File",manifest)
});


function PublishGist(filename,description,content)
{
	// TODO - publish first, add link to manifest, then edit original
	data = {
		description: description,
		public: true,
		files: {},
	};
	data['files'][filename] = { content: content };
	$.ajax({
		url: "https://api.github.com/gists",
		type: "POST",
		data: JSON.stringify(data),
		success: function(o){
			$("#alerts").append("<div class='alert alert-success' role='alert'>"+filename+" template file saved to <a href=\""+o.html_url+"\" target=\"_blank\">"+o.html_url+"</a>.</div>");
		}})
}


function BuildManifest()
{
	// Clear any existing alerts
	$("#alerts").html("");

	// Foundational els
	// TODO - validate foundational els
	manifest = {
		'metadata': {
			'name': $("input[name=package_name]").val(),
	     	'description': $("textarea[name=package_description]").val(),
	     	'uuid': $("input[name=package_uuid]").val(),
		},
		'execution': {
			'mode': $("select[name=package_mode]").val(),
			'command': $("input[name=package_command]").val(),
			'command_script': $("input[name=package_command]").val(),
			'reboot_on_success': $("select[name=package_reboot]").val(),
			'persistent': $("select[name=package_persistent]").val(),
		},
		'parameters': [],
		'names': [],
		'variables': [],
	};

	// variable parameters
	$(".builder_el:not(#builder_el_preamble):not(#builder_el_tpl)").each(function(){
		name = $(this).find("input[name=name]").val();  manifest.names.push(name);
		variable = name.replace(/[^a-z0-9_\.]/gi,"_");  manifest.variables.push(variable);
		if (name=="")  {
			$("#alerts").append("<div class='alert alert-danger' role='alert'>Must assign a name to all parameters before exporting.</div>");
			return (false);
		}
		manifest.execution.command += " '${"+variable+"}'"
		switch (true)  {
			// Standard Params
			case ($(this).hasClass('param_string')):
			case ($(this).hasClass('param_numeric')):
			case ($(this).hasClass('param_password')):
			case ($(this).hasClass('param_network')):
			case ($(this).hasClass('param_serverip')):
			case ($(this).hasClass('param_server')):

			// System params.  
			case ($(this).hasClass('param_user')):
			case ($(this).hasClass('param_name')):
			case ($(this).hasClass('param_ip')):
			case ($(this).hasClass('param_serverpassword')):
				manifest.parameters.push({
						'name': name, 
						'hint': $(this).find(".frm_hint input[name=hint]").val(),
						'required': $(this).find(".frm_required select[name=required]").val(),
						'prompt': $(this).find(".frm_prompt select[name=prompt]").val(),
						'default': $(this).find(".frm_default input[name=default]").val(),
						'type': $(this).find("input[name=type]").val(),
						'global': $(this).find(".frm_prompt select[name=prompt]").val()=='Global'? 'true':'false',
						'variable': variable,
				});
				break;

			// Option params
			case ($(this).hasClass('param_select')):
			case ($(this).hasClass('param_option')):
				options = Array()
				$(this).find(".option_container").each(function(){
					opt_name = $(this).find("input.lable").val()
					opt_value = $(this).find("input.value").val()
					if (!opt_name.length || !opt_value.length)  {
						$("#alerts").append("<div class='alert alert-danger' role='alert'>Must populate both fields for all options ("+name+").</div>");
						return (false);
					}  else  options.push({'name': opt_name, 'value': opt_value});
				});

				manifest.parameters.push({
						'name': name, 
						'hint': $(this).find(".frm_hint input[name=hint]").val(),
						'required': $(this).find(".frm_required select[name=required]").val(),
						'prompt': $(this).find(".frm_prompt select[name=prompt]").val(),
						'default': $(this).find(".frm_default input[name=default]").val(),
						'options': options,
						'type': $(this).find("input[name=type]").val(),
						'global': $(this).find(".frm_prompt select[name=prompt]").val()=='Global'? 'true':'false',
						'variable': variable,
				});
				break;
		}
	});

	// Exit if errors
	if ($("#alerts").html().length)  return(false);
	else  return(manifest);
};


