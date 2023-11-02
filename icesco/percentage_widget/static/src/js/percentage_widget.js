odoo.define('percentage_widget', function(require) {
	"use strict";

	var core = require('web.core');
	var AbstractField = require('web.AbstractField');
	var registry = require('web.field_registry');
	var relational_fields = require('web.relational_fields');

	var _t = core._t;
	var qweb = core.qweb;


	// Form View
	var PercentageWidget = AbstractField.extend({
        description: _lt("Percentage Widget"),
        template: 'PercentageWidget',
        supportedFieldTypes: ['integer', 'float'],

		render_value : function() {
			if (!this.get("effective_readonly")) {
				this._super();
			} else {
				var _value = parseFloat(this.get('value'));
				if (isNaN(_value)) {
					this.$el.find(".percentage_filed").text('');
				} else {
					this.$el.find(".percentage_filed").text(
							(_value).toFixed(0) + ' %');
				}
			}
		}
	});

	registry
    .add('dh_percentage', PercentageWidget);

    return {
    	PercentageWidget: PercentageWidget,
	}

});