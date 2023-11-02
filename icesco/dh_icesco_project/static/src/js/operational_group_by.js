odoo.define('invoice.action_button', function (require) {
"use strict";
/**
 * Button 'Create' is replaced by Custom Button
**/

var core = require('web.core');
var ListController = require('web.ListController');
ListController.include({
   renderButtons: function($node) {
   this._super.apply(this, arguments);
       if (this.$buttons) {
         this.$buttons.find('.o_list_tender_button_group_none').click(this.proxy('action_groupe_none'));
         this.$buttons.find('.o_list_tender_button_group_goal').click(this.proxy('action_groupe_goal'));
         this.$buttons.find('.o_list_tender_button_group_expert').click(this.proxy('action_groupe_expert'));
         this.$buttons.find('.o_list_tender_button_group_sector').click(this.proxy('action_groupe_sector'));
         this.$buttons.find('.o_list_tender_button_group_goal_task').click(this.proxy('action_groupe_goal_task'));
         this.$buttons.find('.o_list_tender_button_group_expert_task').click(this.proxy('action_groupe_expert_task'));
         this.$buttons.find('.o_list_tender_button_group_sector_task').click(this.proxy('action_groupe_sector_task'));
         this.$buttons.find('.o_list_tender_button_indicators_details_task').click(this.proxy('action_indicators_details_task'));
         this.$buttons.find('.o_list_tender_button_indicators_reduit_task').click(this.proxy('action_indicators_reduit_task'));
         this.$buttons.find('.o_list_tender_button_indicators_details').click(this.proxy('action_indicators_details'));

       }
    },

    //--------------------------------------------------------------------------
    // Define Handler for new Custom Button
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {MouseEvent} event
     */
    action_groupe_none: function (e) {
        var self = this;
        var active_id = this.model.get(this.handle).getContext()['active_ids'];
        var model_name = this.model.get(this.handle).getContext()['active_model'];
            this._rpc({
                    model: 'dh.icesco.operational.plan',
                    method: 'view_group_by_none',
                    args: [this.initialState.domain],
                }).then(function (result) {
                    self.do_action(result);
                });
   },

   action_groupe_goal: function (e) {
        var self = this;
        var active_id = this.model.get(this.handle).getContext()['active_ids'];
        var model_name = this.model.get(this.handle).getContext()['active_model'];
            this._rpc({
                    model: 'dh.icesco.operational.plan',
                    method: 'view_group_by_goal',
                    args: [this.initialState.domain],
                }).then(function (result) {
                    self.do_action(result);
                });
   },

   action_groupe_expert: function (e) {
        var self = this;
        var active_id = this.model.get(this.handle).getContext()['active_ids'];
        var model_name = this.model.get(this.handle).getContext()['active_model'];
            this._rpc({
                    model: 'dh.icesco.operational.plan',
                    method: 'view_group_by_expert',
                    args: [this.initialState.domain],
                }).then(function (result) {
                    self.do_action(result);
                });
   },

   action_groupe_sector: function (e) {
        var self = this;
        var active_id = this.model.get(this.handle).getContext()['active_ids'];
        var model_name = this.model.get(this.handle).getContext()['active_model'];
            this._rpc({
                    model: 'dh.icesco.operational.plan',
                    method: 'view_group_by_sector',
                    args: [this.initialState.domain],
                }).then(function (result) {
                    self.do_action(result);
                });
   },

   action_indicators_details: function (e) {
        var self = this;
        var active_id = this.model.get(this.handle).getContext()['active_ids'];
        var model_name = this.model.get(this.handle).getContext()['active_model'];
            this._rpc({
                    model: 'dh.icesco.operational.indicators',
                    method: 'view_indicators_details',
                    args: [this.initialState.domain],
                }).then(function (result) {
                    self.do_action(result);
                });
   },

   action_groupe_goal_task: function (e) {
        var self = this;
        var active_id = this.model.get(this.handle).getContext()['active_ids'];
        var model_name = this.model.get(this.handle).getContext()['active_model'];
            this._rpc({
                    model: 'project.task',
                    method: 'view_group_by_goal',
                    args: [this.initialState.domain],
                }).then(function (result) {
                    self.do_action(result);
                });
   },

   action_groupe_expert_task: function (e) {
        var self = this;
        var active_id = this.model.get(this.handle).getContext()['active_ids'];
        var model_name = this.model.get(this.handle).getContext()['active_model'];
            this._rpc({
                    model: 'project.task',
                    method: 'view_group_by_expert',
                    args: [this.initialState.domain],
                }).then(function (result) {
                    self.do_action(result);
                });
   },

   action_groupe_sector_task: function (e) {
        var self = this;
        var active_id = this.model.get(this.handle).getContext()['active_ids'];
        var model_name = this.model.get(this.handle).getContext()['active_model'];
            this._rpc({
                    model: 'project.task',
                    method: 'view_group_by_sector',
                    args: [this.initialState.domain],
                }).then(function (result) {
                    self.do_action(result);
                });
   },

   action_indicators_details_task: function (e) {
        var self = this;
        var active_id = this.model.get(this.handle).getContext()['active_ids'];
        var model_name = this.model.get(this.handle).getContext()['active_model'];
        console.log('this', self.initialState.domain)
            this._rpc({
                    model: 'project.task',
                    method: 'view_indicators_details',
                    args: [this.initialState.domain],
                }).then(function (result) {
                    self.do_action(result);
                });
   },

   action_indicators_reduit_task: function (e) {
        var self = this;
        var active_id = this.model.get(this.handle).getContext()['active_ids'];
        var model_name = this.model.get(this.handle).getContext()['active_model'];
            this._rpc({
                    model: 'project.task',
                    method: 'view_indicators_reduits',
                    args: [this.initialState.domain],
                }).then(function (result) {
                    self.do_action(result);
                });
   },
});
});