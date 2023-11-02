odoo.define('website_project_kanbanview.kanban_view', function (require) {
	"use strict";
	var ajax = require('web.ajax')
	var rpc = require('web.rpc');

	$(document).ready(function () {
		var url = window.location.pathname;
		var type;
		$('.alert-warning').css('display','none')
		$('.o_portal_my_doc_table').show()

		if (window.location.href.indexOf('/my/kanban/tasks') > -1) {

// ------------------------
			$('.o_portal_my_doc_table').hide()
			var list_button = $(".task_list");
			var kanban_button = $(".kanban_task");
			var doc_quote_table = $('.o_portal_my_doc_table');
			var o_portal_search_panel = $('.o_portal_search_panel');
			var kanban_view = $(".task_kanban_view");

			kanban_button.css("background", "black");
			doc_quote_table.hide();

			kanban_view.show();

			if($('.column').length >= 1){
				$('.alert-warning').css('display','none')
			}
			else{
				$('.alert-warning').css('display','block')
			}

			list_button.click(function () {
				kanban_button.css("background", "#00A09D")
				list_button.css("background", "black")
				kanban_view.hide();
			})
		}


		if (window.location.href.indexOf('/my/tasks') > -1) {
			var list_button = $(".task_list");
			var kanban_button = $(".kanban_task");
			var doc_quote_table = $('.o_portal_my_doc_table');
			var o_portal_search_panel = $('.o_portal_search_panel');
			var kanban_view = $(".task_kanban_view");

			list_button.css("background", "black");
			kanban_view.hide();
			doc_quote_table.show();
			kanban_view.hide();

			if(doc_quote_table.length == 0){
				$('.alert-warning').css('display','block')
			}
			else{
				$('.alert-warning').css('display','none')
			}
			kanban_button.click(function () {
				kanban_button.css("background", "black")
				list_button.css("background", "#00A09D")
				doc_quote_table.hide();
			})
		}

		if (window.location.href.indexOf('/my/projects') > -1) {
			$('.o_portal_my_doc_table').hide()
			var list_button = $(".project_list");
			var kanban_button = $(".kanban_project");
			var doc_quote_table = $('.o_portal_my_doc_table');
			var kanban_view = $(".kanban_view_project");
			kanban_button.css("background", "black");
			kanban_view.show();
			doc_quote_table.hide()

			list_button.click(function () {
				kanban_button.css("background", "#00A09D")
				list_button.css("background", "black")
				doc_quote_table.show();
				kanban_view.hide();
				$('#list_sort_by').show()
				$(".o_portal_pager").show()
			})

			kanban_button.click(function () {
				kanban_button.css("background", "black")
				list_button.css("background", "#00A09D")
				doc_quote_table.hide();
				kanban_view.show();
			})
		}
	});

});
