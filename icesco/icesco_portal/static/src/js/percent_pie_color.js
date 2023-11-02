odoo.define('icesco_portal.percent_pie_color', function (require) {
"use strict";
var core = require('web.core');
var utils = require('web.utils');
var Widget = require('web.Widget');
var FieldRegistry = require('web.field_registry');
var FieldPercentPie = require('web.basic_fields').FieldPercentPie;

FieldPercentPie.include({
    _render_value: function (v) {
        var value = this.value;
        var max_value = this.max_value;
        if (!isNaN(v)) {
            if (this.edit_max_value) {
                max_value = v;
            } else {
                value = v;
            }
        }
        value = value || 0;
        max_value = max_value || 0;
        var widthComplete;
        if (value <= max_value) {
            widthComplete = value/max_value * 100;
        } else {
            widthComplete = 100;
        }
//         this.$('.o_pie').toggleClass('o_pie_overflow', value > max_value)
//             .attr('aria-valuemin', '0')
//             .attr('aria-valuemax', max_value)
//             .attr('aria-valuenow', value);
//        this.$('.o_progressbar_complete').css('width', widthComplete + '%');
        this.$('.o_pie').toggleClass('o_progress_red',widthComplete>0 && widthComplete<=50);
        this.$('.o_pie').toggleClass('o_progress_yellow',widthComplete>50 && widthComplete<=80);
        this.$('.o_pie').toggleClass('o_progress_light_green',widthComplete>80 && widthComplete<=100);
//         this.$('.o_progressbar_complete').toggleClass('o_progress_green',widthComplete>90 && widthComplete<=100).css('width', widthComplete + '%');
        if (!this.write_mode) {
            if (max_value !== 100) {
                this.$('.o_pie_value').text(utils.human_number(value) + " / " + utils.human_number(max_value));
            } else {
                this.$('.o_pie_value').text(utils.human_number(value) + "%");
            }
        } else if (isNaN(v)) {
            this.$('.o_pie_value').val(this.edit_max_value ? max_value : value);
            this.$('.o_pie_value').focus().select();
        }
        this.$('.o_pie_value').toggleClass('o_progress_red',widthComplete>0 && widthComplete<=40);
    },
});
});