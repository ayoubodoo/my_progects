odoo.define('cps_icesco.dh_kiosk_mode', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var core = require('web.core');
var Session = require('web.session');
var QWeb = core.qweb;
var KioskMode = require('hr_attendance.kiosk_mode');

var QWeb = core.qweb;
console.log('icii');

var DhKioskMode = AbstractAction.extend({

        events: {
        "click .o_dh_hr_attendance_button_employees": function() {
            this.do_action('cps_icesco.dh_hr_employee_attendance_action_kanban', {
                additional_context: {'no_group_by': true},
            });
        },
        "click .o_dh_mode_kiosk": function() {

            this.do_action('kzm_hr_pointeuse.dh_hr_attendance_action_kiosk_mode', {
                additional_context: {'no_group_by': true},
            });
        },
        "click .o_ddh_mode_kiosk": function() {

            this.do_action('hr_attendance.hr_attendance_action_kiosk_mode', {
                additional_context: {'no_group_by': true},
            });
        },
    },

    start: function () {
        var self = this;

        core.bus.on('barcode_scanned', this, this._onBarcodeScanned);
        self.session = Session;
//         var def = this._rpc({
//                 model: 'res.company',
//                 method: 'search_read',
//                 args: [[['id', '=', this.session.company_id]], ['name']],
//             })
//             .then(function (companies){
//                 self.company_name = companies[0].name;
//                 self.company_image_url = self.session.url('/web/image', {model: 'res.company', id: self.session.company_id, field: 'logo',});
//                 self.$el.html(QWeb.render("DhHrAttendanceKioskMode", {widget: self}));
//                 self.start_clock();
//             });

        var def = this._rpc({
                model: 'res.company',
                method: 'search_read',
                args: [[['id', '=', this.session.company_id]], ['name']],
            })
            .then(function (companies){
                Session.user_has_group('cps_icesco.icesco_administrator_pointage').then(function(has_group) {
                    if(has_group) {
                        self.has_group = has_group;
                        self.company_name = companies[0].name;
                        self.company_image_url = self.session.url('/web/image', {model: 'res.company', id: self.session.company_id, field: 'logo',});
                        self.$el.html(QWeb.render("DhHrAttendanceKioskMode", {widget: self}));
                        self.start_clock();
                    } else {
                        self.has_group = has_group;
                        self.company_name = companies[0].name;
                        self.company_image_url = self.session.url('/web/image', {model: 'res.company', id: self.session.company_id, field: 'logo',});
                        self.$el.html(QWeb.render("DhHrAttendanceKioskMode", {widget: self}));
                        self.start_clock();
                    }
                });

            });

        // Make a RPC call every day to keep the session alive
        self._interval = window.setInterval(this._callServer.bind(this), (60*60*1000*24));
        return Promise.all([def, this._super.apply(this, arguments)]);
    },

    _onBarcodeScanned: function(barcode) {
        var self = this;
        core.bus.off('barcode_scanned', this, this._onBarcodeScanned);

        this._rpc({
                    model: 'hr.attendance',
                    method: 'get_action_autorisation_sortie',
                    args: [""],
                }).then(function (result) {
                    if (window.location.href.includes(result) == true || window.location.href.includes('hr_dh_attendance_kiosk_confirm') == true) {
                        self._rpc({
                                model: 'hr.employee',
                                method: 'dh_attendance_scan',
                                args: [barcode, ],
                            })
                            .then(function (result) {
                                if (result.action) {
                                    self.do_action(result.action);
                                } else if (result.warning) {
                                    self.do_warn(result.warning);
                                    core.bus.on('barcode_scanned', self, self._onBarcodeScanned);
                                }
                            }, function () {
                                core.bus.on('barcode_scanned', self, self._onBarcodeScanned);
                            });
                        }
                });
    },

    start_clock: function() {
        this.clock_start = setInterval(function() {this.$(".o_hr_attendance_clock").text(new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit', second:'2-digit'}));}, 500);
        // First clock refresh before interval to avoid delay
        this.$(".o_hr_attendance_clock").show().text(new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit', second:'2-digit'}));
    },

    destroy: function () {
        core.bus.off('barcode_scanned', this, this._onBarcodeScanned);
        clearInterval(this.clock_start);
        clearInterval(this._interval);
        this._super.apply(this, arguments);
    },

    _callServer: function () {
        // Make a call to the database to avoid the auto close of the session
        return ajax.rpc("/hr_attendance/kiosk_keepalive", {});
    },

});

core.action_registry.add('dh_hr_attendance_kiosk_mode', DhKioskMode);

return DhKioskMode;

});
