# -*- coding: utf-8 -*-

import json
import werkzeug
from datetime import datetime, date
from odoo import http, _, tools
from odoo.addons.account.controllers.portal import PortalAccount
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request as req, local_redirect
from odoo.osv.expression import AND
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem
from operator import itemgetter
from datetime import date, datetime, timedelta
import base64
from odoo.exceptions import ValidationError
from odoo.http import content_disposition, request, route
from collections import OrderedDict

# from odoo.addons.website.controllers.main import Website
#
#
#
# class WebsiteSaleInherit(Website):
#     @http.route(website=True, auth="public", sitemap=False)
#     def web_login(self, redirect=None, *args, **kw):
#         response = super(Website, self).web_login(redirect=redirect, *args, **kw)
#         if not redirect and request.params['login_success']:
#             if request.env['res.users'].browse(request.uid).has_group('icesco_portal.group_portal_direct_acces'):
#                 redirect = '/my/account'
#             elif request.env['res.users'].browse(request.uid).has_group('base.group_user'):
#                 redirect = b'/web?' + request.httprequest.query_string
#             else:
#                 redirect = '/my'
#
#             return http.redirect_with_hash(redirect)
#         return response

class CustomerPortal(CustomerPortal):
    # MANDATORY_BILLING_FIELDS = ["name", "phone", "email", "street", "city", "country_id"]
    # OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name"]
    MANDATORY_BILLING_FIELDS = []
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name"]

    @http.route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = req.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and req.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key]
                          for key in self.MANDATORY_BILLING_FIELDS}
                values.update(
                    {key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})

                values.update({'zip': values.pop('zipcode', '')})
                if values.get('state_id') == '':
                    values.update({'state_id': False})
                values.update({'country_id': int(values.get('country_id', 1))})

                # Dynamic horizon
                # values.update({'official_country_name': post.get('official_country_name', False) if post.get(
                #     'official_country_name', False) else False})
                values.update({'commission_title': post.get('commission_title', False) if post.get('commission_title',
                                                                                                   False) else False})
                # values.update({'official_leaders': post.get('official_leaders', False) if post.get('official_leaders',
                #                                                                                    False) else False})

                values.update({'year_fondation_national_commission': post.get('year_fondation_national_commission', False).replace('T', ' ') if post.get('year_fondation_national_commission',
                                                                                                   False) else False})
                values.update({'location_national_commission': post.get('location_national_commission',
                                                                              False) if post.get(
                    'location_national_commission',
                    False) else False})
                values.update({'contact_national_commission': post.get('contact_national_commission',
                                                                        False) if post.get(
                    'contact_national_commission',
                    False) else False})
                values.update({'fax_national_commission': post.get('fax_national_commission',
                                                                        False) if post.get(
                    'fax_national_commission',
                    False) else False})
                values.update({'email_national_commission': post.get('email_national_commission',
                                                                        False) if post.get(
                    'email_national_commission',
                    False) else False})
                values.update({'website_national_commission': post.get('website_national_commission',
                                                                     False) if post.get(
                    'website_national_commission',
                    False) else False})

                values.update({'since': post.get('since',
                                                                       False) if post.get(
                    'since',
                    False) else False})

                IrAttachment = req.env['ir.attachment']
                photo = False
                if post.get('photo', False):
                    IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                    access_token = IrAttachment._generate_access_token()
                    photo = IrAttachment.create({
                        'name': post.get('photo', False).filename,
                        'datas': base64.b64encode(post.get('photo', False).read()),
                        # 'res_model': 'event.event',
                        # 'res_id': 0,
                        'access_token': access_token,
                    })

                values.update({'photo': [(6, 0, [photo.id])] if photo else [
                    (6, 0, partner.sudo().photo.ids)]})

                values.update({'name_head_national_commission': post.get('name_head_national_commission',
                                                 False) if post.get(
                    'name_head_national_commission',
                    False) else False})

                values.update({'tasks_head_national_commission': post.get('tasks_head_national_commission',
                                                 False) if post.get(
                    'tasks_head_national_commission',
                    False) else False})

                values.update({'official_name_deputy': post.get('official_name_deputy',
                                                 False) if post.get(
                    'official_name_deputy',
                    False) else False})

                values.update({'commission_title_deputy': post.get('commission_title_deputy',
                                                 False) if post.get(
                    'commission_title_deputy',
                    False) else False})

                values.update({'phone_commission_deputy': post.get('phone_commission_deputy',
                                                 False) if post.get(
                    'phone_commission_deputy',
                    False) else False})

                values.update({'email_commission_deputy': post.get('email_commission_deputy',
                                                 False) if post.get(
                    'email_commission_deputy',
                    False) else False})

                values.update({'since_deputy': post.get('since_deputy',
                                                 False) if post.get(
                    'since_deputy',
                    False) else False})

                IrAttachment = req.env['ir.attachment']
                photo_deputy = False
                if post.get('photo_deputy', False):
                    IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                    access_token = IrAttachment._generate_access_token()
                    photo_deputy = IrAttachment.create({
                        'name': post.get('photo_deputy', False).filename,
                        'datas': base64.b64encode(post.get('photo_deputy', False).read()),
                        # 'res_model': 'event.event',
                        # 'res_id': 0,
                        'access_token': access_token,
                    })

                values.update({'photo_deputy': [(6, 0, [photo_deputy.id])] if photo_deputy else [
                    (6, 0, partner.sudo().photo_deputy.ids)]})

                # if post.get('country_type', False):
                #     K = post.get('country_type', False)
                #     list_country_type = req.env['res.partner']._fields['country_type'].selection
                #     res = [sub[0] for sub in list_country_type if K in sub[1]]
                #     if len(res) > 0:
                #         values.update({'country_type': res[0]})
                values.update(
                    {'official_name': post.get('official_name', False) if post.get('official_name', False) else False})
                values.update(
                    {'work_official_name': post.get('work_official_name', False) if post.get('work_official_name', False) else False})
                values.update({'phone_commission': post.get('phone_commission', False) if post.get('phone_commission',
                                                                                                   False) else False})
                values.update({'email_commission': post.get('email_commission', False) if post.get('email_commission',
                                                                                                   False) else False})
                # values.update({'gpd_per_capital': post.get('gpd_per_capital', False) if post.get('gpd_per_capital',
                #                                                                                  False) else False})
                # values.update({'population': post.get('population', False) if post.get('population', False) else False})
                # values.update({'muslim_population': post.get('muslim_population', False) if post.get(
                #     'muslim_population', False) else False})
                # values.update(
                #     {'national_day': post.get('national_day', False) if post.get('national_day', False) else False})
                # values.update(
                #     {'name_national_day': post.get('name_national_day', False) if post.get('name_national_day', False) else False})
                # if not post.get('new_official_leaders_name', False):
                #     values.update({'country_capital': int(post.get('country_capital', False)) if int(
                #         post.get('country_capital', False)) != 0 else False})

                # if post.get('new_official_leaders_name', False):
                #     country_capital = req.env['res.city'].create({'name': post.get('new_official_leaders_name', False)})
                #     partner.sudo().write({'country_capital': country_capital.id})

                lines_title = []
                count_gov = 0
                for key, value in post.items():  # iter on both keys and values
                    if key.startswith('title'):
                        count_gov += 1

                if post.get('title'):
                    IrAttachment = req.env['ir.attachment']
                    attachment_photo = False
                    if post.get('photo_upload', False):
                        IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                        access_token = IrAttachment._generate_access_token()
                        attachment_photo = IrAttachment.create({
                            'name': post.get('photo_upload', False).filename,
                            'datas': base64.b64encode(post.get('photo_upload', False).read()),
                            # 'res_model': 'event.event',
                            # 'res_id': 0,
                            'access_token': access_token,
                        })
                    if not attachment_photo:
                        lines_title.append(
                            {'title': post.get('title') if post.get('title', False) != 0 else False,
                             'official_name': post.get('official_name') if post.get('official_name', False) != 0 else False,
                             'phone': post.get('phone', False) if post.get('phone', False) else False,
                             'contact_email': post.get('contact_email', False) if post.get('contact_email',
                                                                                           False) else False,
                             'position': post.get('position', False) if post.get('position', False) else False,
                             'since': post.get('since', False) if post.get('since', False) else False,
                             'website': post.get('website', False) if post.get('website', False) else False,
                             })
                    if attachment_photo:
                        lines_title.append(
                            {'title': post.get('title') if post.get('title', False) != 0 else False,
                             'official_name': post.get('official_name') if post.get('official_name',
                                                                                    False) != 0 else False,
                             'phone': post.get('phone', False) if post.get('phone', False) else False,
                             'contact_email': post.get('contact_email', False) if post.get('contact_email',
                                                                                           False) else False,
                             'position': post.get('position', False) if post.get('position', False) else False,
                             'since': post.get('since', False) if post.get('since', False) else False,
                             'website': post.get('website', False) if post.get('website', False) else False,
                             'photo': [(6, 0, [attachment_photo.id])]
                             })

                for i in range(count_gov):
                    if post.get('title_%s' % (i)):
                        IrAttachment = req.env['ir.attachment']
                        attachment_photo = False
                        if post.get('photo_upload_%s' % (i), False):
                            IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                            access_token = IrAttachment._generate_access_token()
                            attachment_photo = IrAttachment.create({
                                'name': post.get('photo_upload_%s' % (i), False).filename,
                                'datas': base64.b64encode(post.get('photo_upload_%s' % (i), False).read()),
                                # 'res_model': 'event.event',
                                # 'res_id': 0,
                                'access_token': access_token,
                            })
                        if not attachment_photo:
                            lines_title.append(
                                {'title': post.get('title_%s' % (i)) if post.get('title_%s' % (i), False) != 0 else False,
                                 'official_name': post.get('official_name_%s' % (i)) if post.get('official_name_%s' % (i),
                                                                                                 False) != 0 else False,
                                 'phone': post.get('phone_%s' % (i)) if post.get('phone_%s' % (i), False) != 0 else False,
                                 'contact_email': post.get('contact_email_%s' % (i), False) if post.get(
                                     'contact_email_%s' % (i), False) else False,
                                 'position': post.get('position_%s' % (i), False) if post.get(
                                     'position_%s' % (i), False) else False,
                                 'since': post.get('since_%s' % (i), False) if post.get(
                                     'since_%s' % (i), False) else False,
                                 'website': post.get('website_%s' % (i), False) if post.get(
                                     'website_%s' % (i), False) else False,
                                 })
                        if attachment_photo:
                            lines_title.append(
                                {'title': post.get('title_%s' % (i)) if post.get('title_%s' % (i), False) != 0 else False,
                                 'official_name': post.get('official_name_%s' % (i)) if post.get('official_name_%s' % (i),
                                                                                                 False) != 0 else False,
                                 'phone': post.get('phone_%s' % (i)) if post.get('phone_%s' % (i), False) != 0 else False,
                                 'contact_email': post.get('contact_email_%s' % (i), False) if post.get(
                                     'contact_email_%s' % (i), False) else False,
                                 'position': post.get('position_%s' % (i), False) if post.get(
                                     'position_%s' % (i), False) else False,
                                 'since': post.get('since_%s' % (i), False) if post.get(
                                     'since_%s' % (i), False) else False,
                                 'website': post.get('website_%s' % (i), False) if post.get(
                                     'website_%s' % (i), False) else False,
                                 'photo': [(6, 0, [attachment_photo.id])]
                                 })
                partner.sudo().write({'government_officials': False})
                values.update({'government_officials': [(0, 0, line) for line in lines_title]})

                lines_commission_team = []
                count = 0
                for key, value in post.items():  # iter on both keys and values
                    if key.startswith('title_commission_team'):
                        count += 1

                if post.get('title_commission_team'):
                    lines_commission_team.append(
                        {'title': post.get('title_commission_team') if post.get('title_commission_team', False) != 0 else False,
                         'official_name': post.get('official_name_commission_team') if post.get('official_name_commission_team',
                                                                                False) != 0 else False,
                         'phone': post.get('phone_commission_team', False) if post.get('phone_commission_team', False) else False,
                         'contact_email': post.get('contact_email_commission_team', False) if post.get('contact_email_commission_team',
                                                                                       False) else False,
                         })

                for i in range(count):
                    if post.get('title_commission_team_%s' % (i)):
                        lines_commission_team.append(
                            {'title': post.get('title_commission_team_%s' % (i)) if post.get('title_commission_team_%s' % (i),
                                                                             False) != 0 else False,
                             'official_name': post.get('official_name_commission_team_%s' % (i)) if post.get(
                                 'official_name_commission_team_%s' % (i),
                                 False) != 0 else False,
                             'phone': post.get('phone_commission_team_%s' % (i)) if post.get('phone_commission_team_%s' % (i),
                                                                             False) != 0 else False,
                             'contact_email': post.get('contact_email_commission_team_%s' % (i), False) if post.get(
                                 'contact_email_commission_team_%s' % (i), False) else False,
                             })

                partner.sudo().write({'commission_team_ids': False})
                values.update({'commission_team_ids': [(0, 0, line) for line in lines_commission_team]})

                # lines_flag_color = []
                # count = 0
                # for key, value in post.items():  # iter on both keys and values
                #     if key.startswith('hex'):
                #         count += 1
                # if post.get('hex'):
                #     lines_flag_color.append(
                #         {'hex': post.get('hex') if post.get('hex', False) != 0 else False,
                #          'rgb': int(post.get('rgb')) if post.get('rgb', False) != 0 else False,
                #          })
                #
                # for i in range(count):
                #     if post.get('hex_%s' % (i)):
                #         lines_flag_color.append(
                #             {'hex': post.get('hex_%s' % (i)) if post.get('hex_%s' % (i), False) != 0 else False,
                #              'rgb': int(post.get('rgb_%s' % (i))) if post.get('rgb_%s' % (i), False) != 0 else False,
                #
                #              })
                #
                # partner.sudo().write({'flag_color': False})
                # for line in lines_flag_color:
                #     flag_color = req.env['dh.flag.reference'].create({'hex': line['hex'], 'rgb': line['rgb']})
                #     partner.sudo().write({'flag_color': [(4, flag_color.id)]})

                lines_official_language = []
                count = 0
                for key, value in post.items():  # iter on both keys and values
                    if key.startswith('official_language'):
                        count += 1

                if post.get('official_language'):
                    if post.get('official_language', False) != 0:
                        lines_official_language.append(int(post.get('official_language')))

                for i in range(count):
                    if post.get('official_language_%s' % (i)):
                        if post.get('official_language_%s' % (i), False) != 0:
                            lines_official_language.append(int(post.get('official_language_%s' % (i))))

                partner.sudo().write({'official_language': False})
                for line in lines_official_language:
                    partner.sudo().write({'official_language': [(4, line)]})

                lines_used_language = []
                count = 0
                for key, value in post.items():  # iter on both keys and values
                    if key.startswith('used_language'):
                        count += 1

                if post.get('used_language'):
                    if post.get('used_language', False) != 0:
                        lines_used_language.append(int(post.get('used_language')))

                for i in range(count):
                    if post.get('used_language_%s' % (i)):
                        if post.get('used_language_%s' % (i), False) != 0:
                            lines_used_language.append(int(post.get('used_language_%s' % (i))))

                partner.sudo().write({'used_language': False})
                for line in lines_used_language:
                    partner.sudo().write({'used_language': [(4, line)]})

                # gggg
                # lines = []
                # count = 0
                # for key, value in post.items():  # iter on both keys and values
                #     if key.startswith('national_days'):
                #         count += 1
                #
                # req.env['dh.national.days'].search([('partner_id', '=', partner.sudo().id)]).unlink()
                # if post.get('national_days'):
                #     if post.get('national_days', False) != 0:
                #         req.env['dh.national.days'].create({'date': post.get('national_days', False).replace('T', ' '),
                #                                             'name': post.get('name_national_days', False),
                #                                             'partner_id': partner.sudo().id})
                #
                # for i in range(count):
                #     if post.get('national_days_%s' % (i)):
                #         if post.get('national_days_%s' % (i), False) != 0:
                #             req.env['dh.national.days'].create(
                #                 {'date': post.get('national_days_%s' % (i), False).replace('T', ' '),
                #                  'name': post.get('name_national_days_%s' % (i), False),
                #                  'partner_id': partner.sudo().id})

                # IrAttachment = req.env['ir.attachment']
                # attachment_flag = False
                # if post.get('country_flag', False):
                #     IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                #     access_token = IrAttachment._generate_access_token()
                #     attachment_flag = IrAttachment.create({
                #         'name': post.get('country_flag', False).filename,
                #         'datas': base64.b64encode(post.get('country_flag', False).read()),
                #         # 'res_model': 'event.event',
                #         # 'res_id': 0,
                #         'access_token': access_token,
                #     })
                #
                # values.update({'country_flag': [(6, 0, [attachment_flag.id])] if attachment_flag else [
                #     (6, 0, partner.sudo().country_flag.ids)]})
                # partner.sudo().write({'other_national_days': False})
                # for line in lines:
                #     partner.sudo().write({'other_national_days': [(4, line)]})
                # hhh
                # lines_date = []
                # count = 0
                # for key, value in post.items():  # iter on both keys and values
                #     if key.startswith('date'):
                #         count += 1
                # if post.get('date'):
                #     if post.get('date', False) != 0:
                #         lines_date.append(post.get('date'))
                #
                # for i in range(count):
                #     if post.get('date_%s' % (i)):
                #         if post.get('date_%s' % (i), False) != 0:
                #             lines_date.append({post.get('date_%s' % (i))})
                #
                # values.update({'other_national_days': [(4, line) for line in lines_date]})

                # lines = []
                # count = 0
                # for key, value in post.items():  # iter on both keys and values
                #     if key.startswith('date'):
                #         count += 1
                # if post.get('date'):
                #     lines.append(
                #         {'national_day_id': post.get('date') if post.get('date', False) != 0 else False,
                #          'date': post.get('date_%s' % (i)) if post.get('date_%s' % (i), False) != 0 else False,
                #          })
                #
                # for i in range(count):
                #     if post.get('date_%s' % (i)):
                #         lines.append(
                #             {'national_day_id': post.get('date_%s' % (i)) if post.get('date_%s' % (i), False) != 0 else False,
                #              'date': post.get('date_%s' % (i)) if post.get('date_%s' % (i), False) != 0 else False,
                #
                #
                #              })
                #     values.update({'other_national_days': [(0, 0, line) for line in lines]})

                partner.sudo().write(values)
                if redirect:
                    return req.redirect(redirect)
                return req.redirect('/my/home')

        countries = req.env['res.country'].sudo().search([])
        capital_countries = req.env['res.city'].sudo().search([])
        states = req.env['res.country.state'].sudo().search([])
        langagues = req.env['dh.lang'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'capital_countries': capital_countries,
            'official_languages': langagues,
            'used_languages': langagues,
            'states': states,
            'has_check_vat': hasattr(req.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = req.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    def details_form_validate(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.MANDATORY_BILLING_FIELDS:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        partner = request.env.user.partner_id
        if data.get("vat") and partner and partner.vat != data.get("vat"):
            if partner.can_edit_vat():
                if hasattr(partner, "check_vat"):
                    if data.get("country_id"):
                        data["vat"] = request.env["res.partner"].fix_eu_vat_number(int(data.get("country_id")),
                                                                                   data.get("vat"))
                    partner_dummy = partner.new({
                        'vat': data['vat'],
                        'country_id': (int(data['country_id'])
                                       if data.get('country_id') else False),
                    })
                    try:
                        partner_dummy.check_vat()
                    except ValidationError:
                        error["vat"] = 'error'
            else:
                error_message.append(
                    _('Changing VAT number is not allowed once document(s) have been issued for your account. Please contact us directly for this operation.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        # unknown = [k for k in data if k not in self.MANDATORY_BILLING_FIELDS + self.OPTIONAL_BILLING_FIELDS]
        # if unknown:
        #     error['common'] = 'Unknown field'
        #     error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message

class PortalAppraisal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalAppraisal, self)._prepare_portal_layout_values()
        domain = [('employee_id.is_member_state', '=', True)]
        orders_count = req.env['appraisal.appraisal'].sudo().search_count(
            domain)
        values['appraisal_count'] = orders_count
        return values

    def _appraisal_get_page_view_values(self, appraisal, access_token, **kwargs):
        values = {
            'page_name': 'appraisal',
            'appraisal': appraisal,
        }
        return self._get_page_view_values(appraisal, access_token, values,
                                          'my_appraisals_history', False, **kwargs)

    @http.route(['/my/appraisal', '/my/appraisal/page/<int:page>'], type='http', auth="user",
                website=True)
    def portal_my_appraisal(self, page=1, date_begin=None, date_end=None, search=None,
                        search_in='all',
                        groupby='employee_id', sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        appraisal = req.env['appraisal.appraisal'].sudo()
        domain = [('employee_id.is_member_state', '=', True)] # ,('create_uid', '=', req.env.uid)
        searchbar_sortings = {
            'evaluation_date': {'label': _('Newest'), 'order': 'evaluation_date desc'},
            'name': {'label': _('Appraisal Name'), 'order': 'name'},
            'employee_id': {'label': _('Pays'), 'order': 'employee_id'},
            'state': {'label': _('State'), 'order': 'state'},
        }

        # default sort by order id = top_menu_collapse
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'name': {'input': 'name', 'label': _('Appraisal Name')},
            'employee_id': {'input': 'employee_id', 'label': _('Pays')},
            'state': {'input': 'state', 'label': _('State')},
            'evaluation_date': {'input': 'evaluation_date', 'label': _('Appraisal Date')},
        }

        searchbar_inputs = {
            'name': {'input': 'name', 'label': _('Search in name')},
            'employee_id': {'input': 'employee_id', 'label': _('Search in pays')},
            # 'create_date': {'input': 'create_date', 'label': _('Search in create date')},
            # 'all': {'input': 'all', 'label': _('Search in name')},
            # 'ref_ext': {'input': 'ref_ext', 'label': _('Search in External Reference')},
        }

        if not sortby:
            sortby = 'evaluation_date'
        order = searchbar_sortings[sortby]['order']
        if search and search_in:
            search_domain = []
            # if search_in in ('content', 'all'):
            #     search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('employee_id', 'all'):
                search_domain = OR(
                    [search_domain, [('employee_id', 'ilike', search)]])

            # if search_in in ('create_date', 'all'):
            #     search_domain = OR(
            #         [search_domain, [('create_date', 'ilike', search)]])
            domain += search_domain

        # if search and search_in:
        #     domain = AND([domain, [('name', 'ilike', search)]])

        # count for pager
        appraisal_count = appraisal.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/appraisal",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby,
                      'search_in': search_in, 'groupby': groupby,
                      'search': search, },
            total=appraisal_count,
            page=page,
            step=self._items_per_page
        )

        archive_groups = self._get_archive_groups('appraisal.appraisal',
                                                  domain)

        # content according to pager and archive selected
        if groupby == 'state':
            order = "state, %s" % order
        if groupby == 'employee_id':
            order = "employee_id, %s" % order
        if groupby == 'evaluation_date':
            order = "evaluation_date, %s" % order

        appraisal = appraisal.search(domain, order=order, limit=self._items_per_page,
                             offset=pager['offset'])

        req.session['my_appraisals_history'] = appraisal.ids[:100]

        if groupby == 'state':
            grouped_appraisal = [req.env['appraisal.appraisal'].concat(*g) for
                             k, g in
                             groupbyelem(event, itemgetter('state'))]
        elif groupby == 'employee_id':
            grouped_appraisal = [req.env['appraisal.appraisal'].concat(*g) for
                             k, g in
                             groupbyelem(appraisal, itemgetter('employee_id'))]
        elif groupby == 'evaluation_date':
            grouped_appraisal = [req.env['appraisal.appraisal'].concat(*g) for k, g in
                             groupbyelem(appraisal, itemgetter('evaluation_date'))]
        else:
            grouped_appraisal = [appraisal]

        values.update({
            'date': date_begin,
            'grouped_appraisal': appraisal,
            'appraisal': appraisal,
            'grouped_event': grouped_appraisal,
            'page_name': 'appraisal',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/appraisal',
            # 'searchbar_sortings': searchbar_sortings,
            # 'searchbar_groupby': searchbar_groupby,
            # 'searchbar_inputs': searchbar_inputs,
            # 'search_in': search_in,
            # 'sortby': sortby,
            # 'groupby': groupby,
        })

        return req.render("icesco_portal.portal_my_appraisal", values)

    @http.route([
        "/my/appraisal/<int:appraisal_id>",
        "/my/appraisal<int:appraisal_id>/<access_token>"
    ], type='http', auth="public", website=True)
    def appraisal_followup(self, appraisal_id=None, access_token=None, **kw):
        try:
            appraisal_sudo = self._document_check_access('appraisal.appraisal',
                                                     appraisal_id, access_token)

        except (AccessError, MissingError):
            return req.redirect('/my')

        values = self._appraisal_get_page_view_values(appraisal_sudo, access_token, **kw)
        return req.render("icesco_portal.portal_appraisal_page", values)

    @http.route('/appraisal/create', type='http', auth="user", website=True)
    def view_appraisal_form_create(self, error=None, **kwargs):
        partner = req.env.user.partner_id.id
        categories = req.env['event.type'].sudo().search([])
        # child = ('id', 'in', req.env.user.partner_id.child_ids.ids if partner else [])
        users = req.env['res.users'].sudo().search([])

        members = req.env['res.country'].sudo().search([('is_member', '=', True)])

        # if error:
        #     error = eval(error)[0]

        values = {
            # 'users': users,
            # 'partners_ioc': partners_ioc,
            # 'partners_un': partners_un,
        }
        return req.render("icesco_portal.appraisal_submit", values)

    @http.route('/appraisal/submit_request', type='http', auth="user", website=True)
    def create_appraisal_record_request(self, **post):
        try:

            data = {
                'name': "Evaluation - %s" % (req.env.user.name),
                'employee_id': req.env.user.employee_id.id,
                'evaluation_date': date.today(),
                'model_evaluation_id': req.env['appraisal.model'].search([('evaluation_pays_member', '=', True)], limit=1).id,
            }
            appraisal = req.env['appraisal.appraisal'].sudo().create(data)
            appraisal.set_appraisal_line_ids()

            i=1
            for appraisal_line in appraisal.appraisal_line_ids:
                if int(post.get('question_%s' %(i))) != False:
                    note_id = req.env['appraisal.rating.factor.value'].search([('name', '=', int(post.get('question_%s' %(i)))), ('evaluation_pays_member', '=', True)], limit=1)
                    appraisal_line.write({'note_id': note_id.id})
                i=i+1

            appraisal.get_appraisal_note()
            appraisal.get_total_note()

            return local_redirect("/my/appraisal")

        except Exception as e:
            print(e)
            error = str(e)
            return self.view_appraisal_form_create(error=error)
        # except:
        #     error = str("Something went wrong")
        #     return self.view_event_form_create(error=error)

class PortalEvent(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalEvent, self)._prepare_portal_layout_values()
        domain = []
        orders_count = req.env['event.event'].sudo().search_count(
            domain)
        values['orders_count'] = orders_count
        return values

    def _event_get_page_view_values(self, event, access_token, **kwargs):
        values = {
            'page_name': 'event',
            'event': event,
        }
        return self._get_page_view_values(event, access_token, values,
                                          'my_events_history', False, **kwargs)

    @http.route(['/my/event', '/my/event/page/<int:page>'], type='http', auth="user",
                website=True)
    def portal_my_event(self, page=1, date_begin=None, date_end=None, search=None,
                        search_in='all',
                        groupby='user_id', sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        event = req.env['event.event'].sudo()
        domain = []
        # domain = [('create_uid', '=', req.env.uid)]
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('event number'), 'order': 'name'},
            'state': {'label': _('Statut'), 'order': 'state'},
            'user_id': {'label': _('Responsible'), 'order': 'user_id desc'},
        }

        # default sort by order id = top_menu_collapse
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'user_id': {'input': 'user_id', 'label': _('Responsible')},
            'state': {'input': 'state', 'label': _('Statut')},
            'create_date': {'input': 'create_date', 'label': _('Create date')},
        }

        searchbar_inputs = {
            'name': {'input': 'name', 'label': _('Search in name')},
            'user_id': {'input': 'user_id', 'label': _('Search in responsible')},
            # 'create_date': {'input': 'create_date', 'label': _('Search in create date')},
            # 'all': {'input': 'all', 'label': _('Search in name')},
            # 'ref_ext': {'input': 'ref_ext', 'label': _('Search in External Reference')},
        }

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        if search and search_in:
            search_domain = []
            # if search_in in ('content', 'all'):
            #     search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('user_id', 'all'):
                search_domain = OR(
                    [search_domain, [('user_id', 'ilike', search)]])

            # if search_in in ('create_date', 'all'):
            #     search_domain = OR(
            #         [search_domain, [('create_date', 'ilike', search)]])
            domain += search_domain

        # if search and search_in:
        #     domain = AND([domain, [('name', 'ilike', search)]])

        # count for pager
        event_count = event.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/event",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby,
                      'search_in': search_in, 'groupby': groupby,
                      'search': search, },
            total=event_count,
            page=page,
            step=self._items_per_page
        )

        archive_groups = self._get_archive_groups('event.event',
                                                  domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin),
                       ('create_date', '<=', date_end)]

        # content according to pager and archive selected
        if groupby == 'state':
            order = "state, %s" % order
        if groupby == 'user_id':
            order = "user_id, %s" % order
        if groupby == 'create_date':
            order = "create_date, %s" % order

        event = event.search(domain, order=order, limit=self._items_per_page,
                             offset=pager['offset'])

        req.session['my_events_history'] = event.ids[:100]

        if groupby == 'state':
            grouped_event = [req.env['event.event'].concat(*g) for
                             k, g in
                             groupbyelem(event, itemgetter('state'))]
        elif groupby == 'user_id':
            grouped_event = [req.env['event.event'].concat(*g) for
                             k, g in
                             groupbyelem(event, itemgetter('user_id'))]
        elif groupby == 'create_date':
            grouped_event = [req.env['event.event'].concat(*g) for k, g in
                             groupbyelem(event, itemgetter('create_date'))]
        else:
            grouped_event = [event]

        values.update({
            'date': date_begin,
            'event': event,
            'grouped_event': grouped_event,
            'page_name': 'event',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/event',
            # 'searchbar_sortings': searchbar_sortings,
            # 'searchbar_groupby': searchbar_groupby,
            # 'searchbar_inputs': searchbar_inputs,
            # 'search_in': search_in,
            # 'sortby': sortby,
            # 'groupby': groupby,
        })

        return req.render("icesco_portal.portal_my_event", values)

    @http.route([
        "/my/event/<int:event_id>",
        "/my/event<int:event_id>/<access_token>"
    ], type='http', auth="public", website=True)
    def event_followup(self, event_id=None, access_token=None, **kw):
        try:
            event_sudo = self._document_check_access('event.event',
                                                     event_id, access_token)

        except (AccessError, MissingError):
            return req.redirect('/my')

        values = self._event_get_page_view_values(event_sudo, access_token, **kw)
        return req.render("icesco_portal.portal_event_page", values)

    @http.route('/event/create', type='http', auth="user", website=True)
    def view_event_form_create(self, error=None, **kwargs):
        partner = req.env.user.partner_id.id
        categories = req.env['event.type'].sudo().search([])
        # child = ('id', 'in', req.env.user.partner_id.child_ids.ids if partner else [])
        users = req.env['res.users'].sudo().search([])
        states = [('draft', "Uncofirmed"), ('confirm', "Confirmed"),
                  ('cancel', "Cancelled"), ('done', "Done")]
        departments = req.env['hr.department'].sudo().search([])
        countries = req.env['res.country'].sudo().search([])
        rooms = req.env['cps.event.room'].sudo().search([])
        locations = [('icesco', "ICESCO"), ('external', "External"), ('online', "Online")]
        dg_participations = [('no', 'No Participation'), ('visit', 'Visit (In Person)'),
                             ('opening', 'Opening/ Closing address (In Person)'),
                             ('recorded', 'Recorded Video (Virtual)'),
                             ('video', 'Video Conference (Virtual)')]

        participation_levels = [('a+', 'A+: Two or more Presidents'), ('a', 'A: One President'),
                                ('b+', 'B+: Prime Minister or over Two ministers'), ('b', 'B: One Minister'),
                                ('c', 'C: Professionals')]
        # Initiative_requires = [('DG Approval', "DG Approval"), ('DG participation', "DG participation"),
        #                        ('Sector/Department participation', "Sector/Department participation"),
        #                        ('Estimated Budget', "Estimated Budget")]
        members = req.env['res.country'].sudo().search([('is_member', '=', True)])
        partners_ioc = req.env['res.partner'].sudo().search([('is_ioc_organization', '=', True)])
        partners_un = req.env['res.partner'].sudo().search([('is_un_organization', '=', True)])
        partners_au = req.env['res.partner'].sudo().search([('is_au_organization', '=', True)])
        partners_al = req.env['res.partner'].sudo().search([('is_al_organization', '=', True)])

        service_translation = req.env['dh.service.department'].sudo().search([("type_department", "=", 'translation')])
        service_designing = req.env['dh.service.department'].sudo().search(
            [("type_department", "=", 'designing_printing')])
        service_legal = req.env['dh.service.department'].sudo().search([("type_department", "=", 'legal')])
        service_finance = req.env['dh.service.department'].sudo().search([("type_department", "=", 'finance')])
        service_logistics = req.env['dh.service.department'].sudo().search([("type_department", "=", 'logistics')])
        service_procurement = req.env['dh.service.department'].sudo().search([("type_department", "=", 'procurement')])
        service_it = req.env['dh.service.department'].sudo().search([("type_department", "=", 'it')])
        service_media = req.env['dh.service.department'].sudo().search([("type_department", "=", 'media')])
        service_protocol = req.env['dh.service.department'].sudo().search([("type_department", "=", 'protocol')])
        service_others = req.env['dh.service.department'].sudo().search([("type_department", "=", 'others')])

        projects = req.env['project.project'].sudo().search([])
        tasks = req.env['project.task'].sudo().search([('project_id', '!=', False)])
        non_members = req.env['res.country'].sudo().search([('is_member', '=', False)])
        frequency = [('first', 'First time event'), ('regular', 'Regular activity'),
                     ('continuity', 'Continuity of previous collaboration')]
        initiatives = [('icesco_plan', 'Part of ICESCO plan'), ('new', 'New proposed activity'),
                       ('cooperation', 'Cooperation agreement')]

        state_engagements = [('high', 'High: Over 6 times in the same year'),
                             ('medium', 'Medium: Between 3 to 6 times in the same year'),
                             ('low', 'Low: Less than 3 times in the same year')]
        # if error:
        #     error = eval(error)[0]

        values = {
            'users': users,
            'partners_ioc': partners_ioc,
            'partners_un': partners_un,
            'partners_au': partners_au,
            'partners_al': partners_al,
            'service_translation': service_translation,
            'service_designing': service_designing,
            'service_legal': service_legal,
            'service_finance': service_finance,
            'service_logistics': service_logistics,
            'service_procurement': service_procurement,
            'service_it': service_it,
            'service_media': service_media,
            'service_protocol': service_protocol,
            'service_others': service_others,
            'categories': categories,
            'locations': locations,
            'projects': projects,
            'tasks': tasks,
            'dg_participations': dg_participations,
            'participation_levels': participation_levels,
            'departments': departments,
            'countries': countries,
            'state_engagements': state_engagements,
            'rooms': rooms,
            'states': states,
            'partner': req.env.user.partner_id,
            'initiatives': initiatives,
            # 'Initiative_requires': Initiative_requires,
            'frequency': frequency,
            'members': members,
            'non_members': non_members,
            'error': error,
        }
        return req.render("icesco_portal.event_submit", values)

    @http.route('/event/submit_request', type='http', auth="user", website=True)
    def create_event_record_request(self, **post):
        try:
            # print('fczfa', type(post.get('attach_invitation_id', False)))
            partner = req.env.user.sudo().partner_id.id
            # partners = req.env['res.partner']
            # countries = req.env['res.country']
            # destinations = req.env['sochepress.destination']
            # test_attachment = req.env['ir.attachment'].create({
            #     'content_length': ,
            #     'content_type': ,
            #     'filename': ,
            #     'headers': ,
            #     'mimetype': ,
            #     'name': ,
            #     'stream': ,
            #     'datas': base64.b64encode(post.get('attach_invitation_id', False)),
            # })

            IrAttachment = req.env['ir.attachment']
            access_token = False

            attachment_invitation = False
            if post.get('attach_invitation_id', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                attachment_invitation = IrAttachment.create({
                    'name': post.get('attach_invitation_id', False).filename,
                    'datas': base64.b64encode(post.get('attach_invitation_id', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })
            attachment_note = False
            if post.get('attach_note_id', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                attachment_note = IrAttachment.create({
                    'name': post.get('attach_note_id', False).filename,
                    'datas': base64.b64encode(post.get('attach_note_id', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })
            attachment_participants = False
            if post.get('attach_participants_id', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                attachment_participants = IrAttachment.create({
                    'name': post.get('attach_participants_id', False).filename,
                    'datas': base64.b64encode(post.get('attach_participants_id', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })

            attach_external_exports = False
            if post.get('attach_external_export', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                attach_external_exports = IrAttachment.create({
                    'name': post.get('attach_external_export', False).filename,
                    'datas': base64.b64encode(post.get('attach_external_export', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })

            if post.get('initiative', False) == 'new':
                if post.get('project_initiative_new', False) not in ['', False]:
                    project_id = req.env['project.project'].search(
                        [('id', '=', int(post.get('project_initiative_new', False)))]).id
                elif post.get('new_project', False):
                    project = req.env['project.project'].create({'name': post.get('new_project', False)})
                    project_id = project.id
                else:
                    project_id = False

            elif post.get('initiative', False) == 'icesco_plan':
                project_id = req.env['project.task'].search([('id', '=', int(post.get('task', False)))]).project_id.id
            else:
                project_id = False

            if post.get('new_task', False) not in ['', False] and post.get('initiative', False) == 'new':
                task = req.env['project.task'].create(
                    {
                        'name': post.get('new_task', False),
                        'project_id': project_id,
                        'translation': True if post.get('translation') == 'on' else False,
                        'is_support_designing': True if post.get('is_support_designing') == 'on' else False,
                        'is_support_legal': True if post.get('is_support_legal') == 'on' else False,
                        'is_support_logistics': True if post.get('is_support_logistics') == 'on' else False,
                        'is_support_protocol': True if post.get('is_support_protocol') == 'on' else False,
                        'is_support_finance': True if post.get('is_support_finance') == 'on' else False,
                        'is_support_admin': True if post.get('is_support_admin') == 'on' else False,
                        'is_support_it': True if post.get('is_support_it') == 'on' else False,
                        'is_support_media': True if post.get('is_support_media') == 'on' else False,
                    }
                )
                task_id = task.id
            elif post.get('initiative', False) == 'icesco_plan':
                task_id = int(post.get('task', False))
                req.env['project.task'].search([('id', '=', task_id)]).write({
                    'translation': True if post.get('translation') == 'on' else False,
                    'is_support_designing': True if post.get('is_support_designing') == 'on' else False,
                    'is_support_legal': True if post.get('is_support_legal') == 'on' else False,
                    'is_support_logistics': True if post.get('is_support_logistics') == 'on' else False,
                    'is_support_protocol': True if post.get('is_support_protocol') == 'on' else False,
                    'is_support_finance': True if post.get('is_support_finance') == 'on' else False,
                    'is_support_admin': True if post.get('is_support_admin') == 'on' else False,
                    'is_support_it': True if post.get('is_support_it') == 'on' else False,
                    'is_support_media': True if post.get('is_support_media') == 'on' else False,
                    'list_translation_service': int(post.get('service_translation')) if int(
                        post.get('service_translation', False)) != 0 and post.get('translation') == 'on' else False,
                    'list_designing_service': int(post.get('service_designing')) if int(
                        post.get('service_designing', False)) != 0 and post.get(
                        'is_support_designing') == 'on' else False,
                    'list_legal_service': int(post.get('service_legal')) if int(
                        post.get('service_legal', False)) != 0 and post.get('is_support_legal') == 'on' else False,
                    'list_finance_service': int(post.get('service_finance')) if int(
                        post.get('service_finance', False)) != 0 and post.get('is_support_finance') == 'on' else False,
                    'list_logistics_service': int(post.get('service_logistics')) if int(
                        post.get('service_logistics', False)) != 0 and post.get(
                        'is_support_logistics') == 'on' else False,
                    'list_admin_service': int(post.get('service_procurement')) if int(
                        post.get('service_procurement', False)) != 0 and post.get(
                        'is_support_admin') == 'on' else False,
                    'list_it_service': int(post.get('service_it')) if int(
                        post.get('service_it', False)) != 0 and post.get('is_support_it') == 'on' else False,
                    'list_media_service': int(post.get('service_media')) if int(
                        post.get('service_media', False)) != 0 and post.get('is_support_media') == 'on' else False,
                    'list_protocol_service': int(post.get('service_protocol')) if int(
                        post.get('service_protocol', False)) != 0 and post.get(
                        'is_support_protocol') == 'on' else False,
                })
            else:
                task_id = False

            data = {
                # 'user_id': req.env.user.id,
                'name': post.get('event_related', False) if post.get('event_related', False) else False,
                'date_begin': post.get('date_begin', False).replace('T', ' ') if post.get('date_begin',
                                                                                          False) else False,
                'date_end': post.get('date_end', False).replace('T', ' ') if post.get('date_end', False) else False,
                # 'date_tz': post.get('date_tz', False),
                # 'seat_min': post.get('seat_min', False),
                # 'seats_availability': post.get('seats_availability', False),
                # 'seats_max': post.get('seats_max', False),
                'deptartment_id': int(post.get('deptartment_id')) if int(
                    post.get('deptartment_id', False)) != 0 else False,
                'event_related': post.get('event_related', False) if post.get('event_related', False) else False,
                'conference_link': post.get('conference_link', False) if post.get('conference_link', False) else False,
                'deadline_delivery': post.get('deadline_delivery', False).replace('T', ' ') if post.get(
                    'deadline_delivery', False) else False,
                'location': post.get('location', False) if post.get('location', False) else False,
                'room_id': int(post.get('room_id')) if int(post.get('room_id', False)) != 0 and post.get('location',
                                                                                                         False) == 'icesco' else False,
                'project_id': project_id if project_id else False,
                'task_id': task_id if task_id else False,
                'country': int(post.get('country')) if int(post.get('country', False)) != 0 and post.get('location',
                                                                                                         False) == 'external' else False,
                'external_member_state': int(post.get('external_member_state')) if int(
                    post.get('external_member_state', False)) != 0 and post.get('location',
                                                                                False) == 'external' else False,
                'external_non_member_state': int(post.get('external_non_member_state')) if int(
                    post.get('external_non_member_state', False)) != 0 and post.get('location',
                                                                                    False) == 'external' else False,
                'city': post.get('city', False) if post.get('city', False) and post.get('location',
                                                                                        False) == 'external' else False,
                'location_name': post.get('location_name', False) if post.get('location_name', False) and post.get(
                    'location', False) == 'external' else False,
                'initiative': post.get('initiative', False) if post.get('initiative', False) else False,
                # 'initiative_required': post.get('initiative_required', False),
                'frequency': post.get('frequency', False) if post.get('frequency', False) else False,
                'provider': post.get('provider', False) if post.get('provider', False) else False,
                'others_organization': post.get('others_organization', False) if post.get('others_organization',
                                                                                          False) else False,
                'member_state_id': int(post.get('member_state_id')) if int(
                    post.get('member_state_id', False)) != 0 else False,
                'non_member_state_id': int(post.get('non_member_state_id', False)) if int(
                    post.get('non_member_state_id', False)) != 0 else False,
                'partners': post.get('partners', False) if post.get('partners', False) else False,
                'dg_approval': True if post.get('dg_approval') == 'on' else False,
                'is_many_presidents': True if post.get('is_many_presidents') == 'on' else False,
                'is_one_president': True if post.get('is_one_president') == 'on' else False,
                'is_many_ministers': True if post.get('is_many_ministers') == 'on' else False,
                'is_one_minister': True if post.get('is_one_minister') == 'on' else False,
                'is_dg_participation': True if post.get('is_dg_participation') == 'on' else False,
                'is_dpt_participation': True if post.get('is_dpt_participation') == 'on' else False,
                'is_external_expert': True if post.get('is_external_expert') == 'on' else False,
                'dg_initiative_required': True if post.get('dg_initiative_required') == 'on' else False,
                'is_sponsorship_available': True if post.get('is_sponsorship_available') == 'on' else False,
                'is_estimated_budget': True if post.get('is_estimated_budget') == 'on' else False,
                'budget': float(post.get('budget').replace(' ', '')) if post.get('budget') else 0,
                'dg_participation': post.get('dg_participation', False) if post.get('dg_participation',
                                                                                    False) else False,
                'speech_topic': post.get('speech_topic', False) if post.get('speech_topic', False) else False,
                'key_people_meet': post.get('key_people_meet', False) if post.get('key_people_meet', False) else False,
                'agenda_topics': post.get('agenda_topics', False) if post.get('agenda_topics', False) else False,
                'speech_points': post.get('speech_points', False) if post.get('speech_points', False) else False,
                'speech_duration': int(post.get('speech_duration')) if post.get('speech_duration') else 0,
                'duration_video': int(post.get('duration_video')) if post.get('duration_video') else 0,
                'date_speech': post.get('date_speech', False).replace('T', ' ') if post.get('date_speech',
                                                                                            False) else False,
                'participation_level': post.get('participation_level', False) if post.get('participation_level',
                                                                                          False) else False,
                'is_ioc_organization': True if post.get('is_ioc_organization') == 'on' else False,
                'list_oic_organization': int(post.get('partner_ioc')) if int(
                    post.get('partner_ioc', False)) != 0 and post.get('is_ioc_organization') == 'on' else False,
                'is_un_organization': True if post.get('is_un_organization') == 'on' else False,
                'list_un_organization': int(post.get('partner_un')) if int(
                    post.get('partner_un', False)) != 0 and post.get('is_un_organization') == 'on' else False,
                'is_au_organization': True if post.get('is_au_organization') == 'on' else False,
                'list_au_organization': int(post.get('partners_au')) if int(
                    post.get('partners_au', False)) != 0 and post.get('is_au_organization') == 'on' else False,
                'is_al_organization': True if post.get('is_al_organization') == 'on' else False,
                'list_al_organization': int(post.get('partners_al')) if int(
                    post.get('partners_al', False)) != 0 and post.get('is_al_organization') == 'on' else False,
                'is_partnership_govenmental': True if post.get('is_partnership_govenmental') == 'on' else False,
                'is_partnership_international': True if post.get('is_partnership_international') == 'on' else False,
                'is_partnership_nonorganization': True if post.get('is_partnership_nonorganization') == 'on' else False,
                'is_partnership_others': True if post.get('is_partnership_others') == 'on' else False,
                'state_engagement': post.get('state_engagement', False) if post.get('state_engagement',
                                                                                    False) else False,
                'is_dg_participation_required': True if post.get('is_dg_participation_required') == 'on' else False,
                'is_dg_visit': True if post.get('is_dg_visit') == 'on' else False,
                'is_dg_event': True if post.get('is_dg_event') == 'on' else False,
                'is_dg_recorded': True if post.get('is_dg_recorded') == 'on' else False,
                'is_dg_video': True if post.get('is_dg_video') == 'on' else False,
                'is_opening': True if post.get('is_opening') == 'on' else False,
                'is_closing': True if post.get('is_closing') == 'on' else False,
                'is_panel': True if post.get('is_panel') == 'on' else False,
                'is_coverage_airflight': True if post.get('is_coverage_airflight') == 'on' else False,
                'is_coverage_diem': True if post.get('is_coverage_diem') == 'on' else False,
                'is_coverage_accomodation': True if post.get('is_coverage_accomodation') == 'on' else False,
                'is_coverage_localtransport': True if post.get('is_coverage_localtransport') == 'on' else False,
                'coverage_persons': post.get('coverage_persons', False) if post.get('coverage_persons',
                                                                                    False) else False,
                'coverage_persons_airflight': post.get('coverage_persons_airflight', False) if post.get(
                    'coverage_persons_airflight', False) else False,
                'coverage_persons_por_diem': post.get('coverage_persons_por_diem', False) if post.get(
                    'coverage_persons_por_diem', False) else False,
                'coverage_persons_accomodation': post.get('coverage_persons_accomodation', False) if post.get(
                    'coverage_persons_accomodation', False) else False,
                'coverage_persons_local_transportation': post.get('coverage_persons_local_transportation',
                                                                  False) if post.get(
                    'coverage_persons_local_transportation', False) else False,
                'is_increase_competitiveness': True if post.get('is_increase_competitiveness') == 'on' else False,
                'is_increase_fundraising': True if post.get('is_increase_fundraising') == 'on' else False,
                'is_increase_partnership': True if post.get('is_increase_partnership') == 'on' else False,
                'is_increase_services': True if post.get('is_increase_services') == 'on' else False,
                'is_increase_services_expertise': True if post.get('is_increase_services_expertise') == 'on' else False,
                'is_increase_services_capacity': True if post.get('is_increase_services_capacity') == 'on' else False,
                'is_increase_services_practice': True if post.get('is_increase_services_practice') == 'on' else False,
                'is_increase_services_collaboration': True if post.get(
                    'is_increase_services_collaboration') == 'on' else False,
                'is_support_translation': True if post.get('is_support_translation') == 'on' else False,
                'translation': True if post.get('translation') == 'on' else False,
                'is_support_designing': True if post.get('is_support_designing') == 'on' else False,
                'is_support_legal': True if post.get('is_support_legal') == 'on' else False,
                'is_support_logistics': True if post.get('is_support_logistics') == 'on' else False,
                'is_support_protocol': True if post.get('is_support_protocol') == 'on' else False,
                'is_support_finance': True if post.get('is_support_finance') == 'on' else False,
                'is_support_admin': True if post.get('is_support_admin') == 'on' else False,
                'is_support_it': True if post.get('is_support_it') == 'on' else False,
                'is_support_media': True if post.get('is_support_media') == 'on' else False,
                'is_support_other': True if post.get('is_support_other') == 'on' else False,
                'list_translation_service': int(post.get('service_translation')) if int(
                    post.get('service_translation', False)) != 0 and post.get('translation') == 'on' else False,
                'list_designing_service': int(post.get('service_designing')) if int(
                    post.get('service_designing', False)) != 0 and post.get('is_support_designing') == 'on' else False,
                'list_legal_service': int(post.get('service_legal')) if int(
                    post.get('service_legal', False)) != 0 and post.get('is_support_legal') == 'on' else False,
                'list_finance_service': int(post.get('service_finance')) if int(
                    post.get('service_finance', False)) != 0 and post.get('is_support_finance') == 'on' else False,
                'list_logistics_service': int(post.get('service_logistics')) if int(
                    post.get('service_logistics', False)) != 0 and post.get('is_support_logistics') == 'on' else False,
                'list_admin_service': int(post.get('service_procurement')) if int(
                    post.get('service_procurement', False)) != 0 and post.get('is_support_admin') == 'on' else False,
                'list_it_service': int(post.get('service_it')) if int(
                    post.get('service_it', False)) != 0 and post.get('is_support_it') == 'on' else False,
                'list_media_service': int(post.get('service_media')) if int(
                    post.get('service_media', False)) != 0 and post.get('is_support_media') == 'on' else False,
                'list_protocol_service': int(post.get('service_protocol')) if int(
                    post.get('service_protocol', False)) != 0 and post.get('is_support_protocol') == 'on' else False,
                'list_others_service': int(post.get('service_others')) if int(
                    post.get('service_others', False)) != 0 and post.get('is_support_other') == 'on' else False,
                'services_other': post.get('services_other', False) if post.get('services_other', False) else False,
                'suppliers_for': post.get('suppliers_for', False) if post.get('suppliers_for', False) else False,
                'sponsors_for': post.get('sponsors_for', False) if post.get('sponsors_for', False) else False,
                'attach_invitation_id': [(6, 0, [attachment_invitation.id])] if attachment_invitation else False,
                'attach_note_id': [(6, 0, [attachment_note.id])] if attachment_note else False,
                'attach_participants_id': [(6, 0, [attachment_participants.id])] if attachment_participants else False,
                'attach_external_export': [(6, 0, [attach_external_exports.id])] if attach_external_exports else False,
                'initiative_required': 'OK',
                'frequency_required': 'OK',
                'dg_initiative_required': 'OK',
                'dg_participation_required': 'OK',
                'participation_level_required': 'OK',
                'state_engagement_required': 'OK',
                'state': 'draft',
            }
            if post.get('create_event') == 'on':
                request = req.env['event.event'].sudo().create(data)

                if request.task_id.id != False:
                    request.task_id.event_id = request.id

                # dg_contact = req.env['res.partner'].search([('email', '=', 'it@icesco.org')])
                # registration = req.env['event.registration'].create(
                #     {'partner_id': dg_contact.id, 'name': dg_contact.name, 'email': dg_contact.email, 'event_id': request.id})
                # registration.confirm_registration()
                # registration.action_send_badge_email()

                return local_redirect("/my/event/%d" % request.id)
                # else:
                #     raise Exception("You can't create a request with empty lines")
                # return local_redirect("/my/event")
            else:
                return local_redirect("/my/event")

        except Exception as e:
            print(e)
            error = str(e)
            return self.view_event_form_create(error=error)
        # except:
        #     error = str("Something went wrong")
        #     return self.view_event_form_create(error=error)

    @http.route(["/event/delete/<int:event_id>", "/event/cancel<int:event_id>/<access_token>"], type='http',
                auth="public", website=True)
    def event_delete(self, event_id=None, access_token=None, **post):

        event = req.env['event.event'].sudo().search([('id', '=', event_id)])
        if event:
            event.unlink()
            return werkzeug.utils.redirect("/my/event")
        else:
            return werkzeug.utils.redirect("/my/event")

    @http.route(["/event/edit/<int:event_id>",
                 "/event/edit<int:event_id>/<access_token>"], type='http',
                auth="public", website=True)
    def event_edit(self, event_id=None, access_token=None, error=None, **kw):
        try:
            request_sudo = self._document_check_access('event.event',
                                                       event_id, access_token)
        except (AccessError, MissingError):
            return req.redirect('/my')
        # partner = req.env.user.partner_id.id
        # contracts = req.env['sochepress.contract'].sudo().search([
        #     ('stage_id', '=',
        #      req.env.ref('sochepress_base.sochepress_contract_stage_in_progress').id),
        #     ('partner_id', '=', partner)], limit=1)
        # child = ('id', 'in', req.env.user.partner_id.child_ids.ids if partner else [])
        # partners = req.env['res.partner'].sudo().search([('parent_id', '=', partner)])
        # expeditions = req.env['res.partner'].sudo().search([('parent_id', '=', partner), ('type', '=', 'other')])
        # expeditions = req.env['res.partner'].sudo().search([('parent_id', '=', partner), ('type', '=', 'other')])
        # destinators = req.env['res.partner'].sudo().search(
        #     [('parent_id', '=', partner), ('type', '=', 'delivery'), ('hidden', '=', False)])
        # destinations = req.env['sochepress.destination'].sudo().search([('id', 'in', contracts.destination_ids.ids)])
        #
        # countries = req.env['res.country'].sudo().search([])
        # types = [('normal', "Normal"), ('transport', "Dedicted transport"),
        #          ('course', "Urgent course")]
        # return_of_fund = [('simple', "Simple"), ('espece', "Especes"),
        #                   ('check', "Cheque"), ('trait', "Traite")]
        # products = req.env['sochepress.type.colis'].sudo().search([])
        # vehicules = req.env['fleet.vehicle'].sudo().search([])
        # demand_date = datetime.today().date()
        partner = req.env.user.partner_id.id
        categories = req.env['event.type'].sudo().search([])
        departments = req.env['hr.department'].sudo().search([])
        # child = ('id', 'in', req.env.user.partner_id.child_ids.ids if partner else [])
        users = req.env['res.users'].sudo().search([])
        states = [('draft', "Uncofirmed"), ('confirm', "Confirmed"),
                  ('cancel', "Cancelled"), ('done', "Done")]
        locations = [('icesco', "ICESCO"), ('external', "External")]
        values = self._event_get_page_view_values(request_sudo, access_token, **kw)
        values.update({
            'users': users,
            'categories': categories,
            'locations': locations,
            'departments': departments,
            'partner': req.env.user.partner_id
        })
        return req.render("icesco_portal.event_edit", values)

    @http.route(["/event/submit_edit/<int:request_id>", "/event/submit_edit<int:request_id>/<access_token>"],
                type='http', auth="user", website=True)
    def edit_request_record_request(self, request_id=None, access_token=None, **post):
        try:
            # id = request_id
            # responsible = int(post.get('responsible')) if int(post.get('responsible', False)) != 0 else False
            # category = int(post.get('category')) if int(post.get('category', False)) != 0 else False
            event = req.env['event.event'].search([('id', '=', request_id)])
            IrAttachment = req.env['ir.attachment']
            access_token = False

            attachment_invitation = False
            if post.get('attach_invitation_id', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                attachment_invitation = IrAttachment.create({
                    'name': post.get('attach_invitation_id', False).filename,
                    'datas': base64.b64encode(post.get('attach_invitation_id', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })
            attachment_note = False
            if post.get('attach_note_id', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                attachment_note = IrAttachment.create({
                    'name': post.get('attach_note_id', False).filename,
                    'datas': base64.b64encode(post.get('attach_note_id', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })
            attachment_participants = False
            if post.get('attach_participants_id', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                attachment_participants = IrAttachment.create({
                    'name': post.get('attach_participants_id', False).filename,
                    'datas': base64.b64encode(post.get('attach_participants_id', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })

            data = {
                # 'user_id': req.env.user.id,
                'name': post.get('event_related', False) if post.get('event_related', False) else event.name,
                'date_begin': post.get('date_begin', False) if post.get('date_begin', False) else event.date_begin,
                'date_end': post.get('date_end', False) if post.get('date_end', False) else event.date_end,
                # 'date_tz': post.get('date_tz', False),
                # 'seat_min': post.get('seat_min', False),
                # 'seats_availability': post.get('seats_availability', False),
                # 'seats_max': post.get('seats_max', False),
                'deptartment_id': int(post.get('deptartment_id')) if int(
                    post.get('deptartment_id', False)) != 0 else event.deptartment_id.id,
                'event_related': post.get('event_related', False) if post.get('event_related',
                                                                              False) else event.event_related,
                'location': post.get('location', False) if post.get('location', False) else event.location,
                'room_id': int(post.get('room_id')) if int(post.get('room_id', False)) != 0 else event.room_id.id,
                'country': int(post.get('country')) if int(post.get('country', False)) != 0 else event.country.id,
                'city': post.get('city', False) if post.get('city', False) else event.city,
                'location_name': post.get('location_name', False) if post.get('location_name',
                                                                              False) else event.location_name,
                'initiative': post.get('initiative', False) if post.get('initiative', False) else event.initiative,
                # 'initiative_required': post.get('initiative_required', False),
                'frequency': post.get('frequency', False) if post.get('frequency', False) else event.frequency,
                'member_state_id': int(post.get('member_state_id')) if int(
                    post.get('member_state_id', False)) != 0 else event.member_state_id.id,
                'non_member_state_id': post.get('non_member_state_id', False) if post.get('non_member_state_id',
                                                                                          False) else event.non_member_state_id.id,
                'partners': post.get('partners', False) if post.get('partners', False) else event.partners,
                'dg_approval': True if post.get('dg_approval') == 'on' else event.dg_approval,
                'is_dg_participation': True if post.get('is_dg_participation') == 'on' else event.is_dg_participation,
                'dg_initiative_required': True if post.get(
                    'dg_initiative_required') == 'on' else event.dg_initiative_required,
                'is_estimated_budget': True if post.get('is_estimated_budget') == 'on' else event.is_estimated_budget,
                'budget': float(post.get('budget').replace(' ', '')) if post.get('budget') else event.budget,
                'dg_participation': post.get('dg_participation', False) if post.get('dg_participation',
                                                                                    False) else event.dg_participation,
                'speech_topic': post.get('speech_topic', False) if post.get('speech_topic',
                                                                            False) else event.speech_topic,
                'speech_points': post.get('speech_points', False) if post.get('speech_points',
                                                                              False) else event.speech_points,
                'speech_duration': int(post.get('speech_duration')) if post.get(
                    'speech_duration') else event.speech_duration,
                'duration_video': int(post.get('duration_video')) if post.get(
                    'duration_video') else event.duration_video,
                'date_speech': post.get('date_speech', False) if post.get('date_speech', False) else event.date_speech,
                'participation_level': post.get('participation_level', False) if post.get('participation_level',
                                                                                          False) else event.participation_level,
                'is_partnership_govenmental': True if post.get(
                    'is_partnership_govenmental') == 'on' else event.is_partnership_govenmental,
                'is_partnership_international': True if post.get(
                    'is_partnership_international') == 'on' else event.is_partnership_international,
                'is_partnership_nonorganization': True if post.get(
                    'is_partnership_nonorganization') == 'on' else event.is_partnership_nonorganization,
                'is_partnership_others': True if post.get(
                    'is_partnership_others') == 'on' else event.is_partnership_others,
                'is_dg_participation_required': True if post.get(
                    'is_dg_participation_required') == 'on' else event.is_dg_participation_required,
                'state_engagement': post.get('state_engagement', False) if post.get('state_engagement',
                                                                                    False) else event.state_engagement,
                'is_coverage_airflight': True if post.get(
                    'is_coverage_airflight') == 'on' else event.is_coverage_airflight,
                'is_coverage_diem': True if post.get('is_coverage_diem') == 'on' else event.is_coverage_diem,
                'is_coverage_accomodation': True if post.get(
                    'is_coverage_accomodation') == 'on' else event.is_coverage_accomodation,
                'is_coverage_localtransport': True if post.get(
                    'is_coverage_localtransport') == 'on' else event.is_coverage_localtransport,
                'coverage_persons': post.get('coverage_persons', False) if post.get('coverage_persons',
                                                                                    False) else event.coverage_persons,
                'is_increase_competitiveness': True if post.get(
                    'is_increase_competitiveness') == 'on' else event.is_increase_competitiveness,
                'is_increase_fundraising': True if post.get(
                    'is_increase_fundraising') == 'on' else event.is_increase_fundraising,
                'is_increase_partnership': True if post.get(
                    'is_increase_partnership') == 'on' else event.is_increase_partnership,
                'is_increase_services': True if post.get(
                    'is_increase_services') == 'on' else event.is_increase_services,
                'is_increase_services_expertise': True if post.get(
                    'is_increase_services_expertise') == 'on' else event.is_increase_services_expertise,
                'is_increase_services_capacity': True if post.get(
                    'is_increase_services_capacity') == 'on' else event.is_increase_services_capacity,
                'is_increase_services_practice': True if post.get(
                    'is_increase_services_practice') == 'on' else event.is_increase_services_practice,
                'is_increase_services_collaboration': True if post.get(
                    'is_increase_services_collaboration') == 'on' else event.is_increase_services_collaboration,
                'is_support_translation': True if post.get(
                    'is_support_translation') == 'on' else event.is_support_translation,
                'translation': True if post.get('translation') == 'on' else event.translation,
                'is_support_designing': True if post.get(
                    'is_support_designing') == 'on' else event.is_support_designing,
                'is_support_legal': True if post.get('is_support_legal') == 'on' else event.is_support_legal,
                'is_support_finance': True if post.get('is_support_finance') == 'on' else event.is_support_finance,
                'is_support_admin': True if post.get('is_support_admin') == 'on' else event.is_support_admin,
                'is_support_it': True if post.get('is_support_it') == 'on' else event.is_support_it,
                'is_support_media': True if post.get('is_support_media') == 'on' else event.is_support_media,
                'is_support_other': True if post.get('is_support_other') == 'on' else event.is_support_other,
                'services_other': post.get('services_other', False) if post.get('services_other',
                                                                                False) else event.services_other,
                'suppliers_for': post.get('suppliers_for', False) if post.get('suppliers_for',
                                                                              False) else event.suppliers_for,
                'sponsors_for': post.get('sponsors_for', False) if post.get('sponsors_for',
                                                                            False) else event.sponsors_for,
                'attach_invitation_id': [(6, 0, [attachment_invitation.id])] if attachment_invitation else [
                    (6, 0, event.attach_invitation_id.ids)],
                'attach_note_id': [(6, 0, [attachment_note.id])] if attachment_note else [
                    (6, 0, event.attach_note_id.ids)],
                'attach_participants_id': [(6, 0, [attachment_participants.id])] if attachment_participants else [
                    (6, 0, event.attach_participants_id.ids)],
                'state': 'draft',
            }
            event.write(data)
            return local_redirect("/my/event/%d" % event.id)
            # if post.get('url_param'):
            #     print("bloqued here")
            #     # return werkzeug.utils.redirect("/my/event/%d?%s" % (
            #     request.id, post['url_param']))
            #     return local_redirect("/my/event/%d?%s" % (request.id,
            #     post['url_param']))
            # else:
            #     print('-----------------')
            #     return local_redirect("/my/event/%d" % request.id)
            #     # return werkzeug.utils.redirect("/my/event/%d" % request.id)

        except Exception as e:
            error = str(e)
            return self.event_edit(request_id=request_id, access_token=None,
                                   error=error, **post)


from odoo.addons.website_form.controllers.main import WebsiteForm


class WebsiteForm(WebsiteForm):

    @http.route('''/helpdesk/<model("helpdesk.team", "[('use_website_helpdesk_form','=',True)]"):team>/submit''',
                type='http', auth="public", website=True)
    def website_helpdesk_form(self, error=None, **kwargs):
        default_values = {}
        if req.env.user.partner_id != req.env.ref('base.public_partner'):
            default_values['name'] = req.env.user.partner_id.name
            default_values['email'] = req.env.user.partner_id.email
            default_values['events'] = req.env['event.event'].sudo().search([])
            default_values['coordinateurs'] = req.env['res.partner'].sudo().search([])
            default_values['departments'] = req.env['hr.department'].sudo().search([])
            default_values['list_it_services'] = req.env['dh.service.department'].sudo().search(
                [("type_department", "=", 'translation')])
            default_values['rooms'] = req.env['cps.event.room'].sudo().search([])
            default_values['error'] = error
        return req.render("website_helpdesk_form.ticket_submit", default_values)

    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        if req.params.get('partner_email'):
            Partner = req.env['res.partner'].sudo().search([('email', '=', kwargs.get('partner_email'))], limit=1)
            if Partner:
                req.params['partner_id'] = Partner.id

        return super(WebsiteForm, self).website_form(model_name, **kwargs)

    @http.route('/website_form/submit', type='http', auth="public", methods=['POST'], csrf=False, website=True)
    def create_ticket_record_request(self, **post):
        try:
            name = ''
            # if int(post.get('event_id', False)) not in ['', False]:
            # name = req.env['event.event'].search([('id', '=', int(post.get('event_id')))]).name
            data = {
                # 'user_id': req.env.user.id,
                'name': post.get('event_id') + ' ' + req.env.user.partner_id.name + ' request' if post.get('event_id',
                                                                                                           False) else False,
                'event_id': post.get('event_id') if post.get('event_id', False) else False,
                'date_start': post.get('date_start', False).replace('T', ' ') if post.get('date_start',
                                                                                          False) else False,
                'partner_email': req.env.user.partner_id.email,
                'company': post.get('company') if post.get('company', False) else False,
                'meeting_link': post.get('meeting_link') if post.get('meeting_link', False) else False,
                'partner_id': int(post.get('partner_id')) if int(
                    post.get('partner_id', False)) != 0 else False,
                'deptartment_id': int(post.get('deptartment_id')) if int(
                    post.get('deptartment_id', False)) != 0 else False,
                'room_id': int(post.get('room_id')) if int(post.get('room_id', False)) != 0 else False,
                'duration': int(post.get('duration')) if post.get('duration') else 0,
                'webinar_attendees': int(post.get('webinar_attendees')) if post.get('webinar_attendees') else 0,
                'data_uploading': True if post.get('data_uploading') == 'on' else False,
                'meeting_zoom_link': True if post.get('meeting_zoom_link') == 'on' else False,
                'registration_link': True if post.get('registration_link') == 'on' else False,
                'video_recording': True if post.get('video_recording') == 'on' else False,
                'video_conference_management': True if post.get('video_conference_management') == 'on' else False,
                'webinar_link': True if post.get('webinar_link') == 'on' else False,
                'website_edition': True if post.get('website_edition') == 'on' else False,
                'waiting_room': True if post.get('waiting_room') == 'on' else False,
                # 'is_translation': True if post.get('is_translation') == 'on' else False,
                'is_translation_arabic': True if post.get('is_translation_arabic') == 'on' else False,
                'is_translation_english': True if post.get('is_translation_english') == 'on' else False,
                'is_translation_french': True if post.get('is_translation_french') == 'on' else False,
                'list_it_service': int(post.get('list_it_service')) if post.get('list_it_service') else 0,
                # 'team_id': req.env['helpdesk.team'].search([], order="id desc", limit=1).id
            }

            request = req.env['helpdesk.ticket'].sudo().create(data)

            # dg_contact = req.env['res.partner'].search([('email', '=', 'it@icesco.org')])
            # registration = req.env['event.registration'].create(
            #     {'partner_id': dg_contact.id, 'name': dg_contact.name, 'email': dg_contact.email, 'event_id': request.id})
            # registration.confirm_registration()
            # registration.action_send_badge_email()

            return local_redirect("/helpdesk/ticket/%d" % request.id)
            # else:
            #     raise Exception("You can't create a request with empty lines")
            # return local_redirect("/my/event")
        except Exception as e:
            print(e)
            error = str(e)
            return req.website_helpdesk_form(error=error)
        # except:
        #     error = str("Something went wrong")
        #     return self.view_event_form_create(error=error)

    @http.route([
        "/my/event/<int:event_id>",
        "/my/event<int:event_id>/<access_token>"
    ], type='http', auth="public", website=True)
    def event_followup(self, event_id=None, access_token=None, **kw):
        try:
            event_sudo = self._document_check_access('event.event',
                                                     event_id, access_token)

        except (AccessError, MissingError):
            return req.redirect('/my')

        values = self._event_get_page_view_values(event_sudo, access_token, **kw)
        return req.render("icesco_portal.portal_event_page", values)


class PortalGoal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalGoal, self)._prepare_portal_layout_values()
        domain = []
        orders_count = req.env['dh.strategic.objectives'].sudo().search_count(
            domain)
        values['goals_count'] = orders_count
        return values

    def _goal_get_page_view_values(self, goal, access_token, **kwargs):
        values = {
            'page_name': 'goal',
            'goal': goal,
        }
        return self._get_page_view_values(goal, access_token, values,
                                          'my_goals_history', False, **kwargs)

    @http.route(['/my/choice', '/my/choice/page/<int:page>'], type='http', auth="user",
                website=True)
    def portal_my_choice(self, page=1, date_begin=None, date_end=None, search=None,
                       search_in='all',
                       groupby='user_id', sortby=None, **kw):

        values = self._prepare_portal_layout_values()
        values.update({
            'page_name': 'Choice',
            # 'searchbar_sortings': searchbar_sortings,
            # # 'searchbar_groupby': searchbar_groupby,
            # 'searchbar_inputs': searchbar_inputs,
            # 'search_in': search_in,
            # 'sortby': sortby,
            # 'groupby': groupby,
        })

        return req.render("icesco_portal.tasks_kanban_select", values)

    @http.route(['/my/goal', '/my/goal/page/<int:page>'], type='http', auth="user",
                website=True)
    def portal_my_goal(self, page=1, date_begin=None, date_end=None, search=None,
                       search_in='all',
                       groupby='user_id', sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        goal = req.env['dh.strategic.objectives'].sudo()
        # domain = [('create_uid', '=', req.env.uid)]
        domain = []
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('goal'), 'order': 'name'},
        }

        # default sort by order id = top_menu_collapse
        # searchbar_groupby = {
        #     'none': {'input': 'none', 'label': _('None')},
        #     'create_date': {'input': 'create_date', 'label': _('Create date')},
        # }

        searchbar_inputs = {
            'name': {'input': 'name', 'label': _('Search in name')},

            # 'create_date': {'input': 'create_date', 'label': _('Search in create date')},
            # 'all': {'input': 'all', 'label': _('Search in name')},
            # 'ref_ext': {'input': 'ref_ext', 'label': _('Search in External Reference')},
        }

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        if search and search_in:
            search_domain = []
            # if search_in in ('content', 'all'):
            #     search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            # if search_in in ('user_id', 'all'):
            #     search_domain = OR(
            #         [search_domain, [('user_id', 'ilike', search)]])

            # if search_in in ('create_date', 'all'):
            #     search_domain = OR(
            #         [search_domain, [('create_date', 'ilike', search)]])
            domain += search_domain

        # if search and search_in:
        #     domain = AND([domain, [('name', 'ilike', search)]])

        # count for pager
        goal_count = goal.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/goal",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby,
                      'search_in': search_in, 'groupby': groupby,
                      'search': search, },
            total=goal_count,
            page=page,
            step=self._items_per_page
        )

        archive_groups = self._get_archive_groups('dh.strategic.objectives',
                                                  domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin),
                       ('create_date', '<=', date_end)]

        # content according to pager and archive selected
        # if groupby == 'state':
        #     order = "state, %s" % order
        # if groupby == 'user_id':
        #     order = "user_id, %s" % order
        if groupby == 'create_date':
            order = "create_date, %s" % order

        goal = goal.search(domain, order=order, limit=self._items_per_page,
                           offset=pager['offset'])

        req.session['my_goals_history'] = goal.ids[:100]

        # if groupby == 'state':
        #     grouped_event = [req.env['event.event'].concat(*g) for
        #                      k, g in
        #                      groupbyelem(event, itemgetter('state'))]
        # elif groupby == 'user_id':
        #     grouped_event = [req.env['event.event'].concat(*g) for
        #                      k, g in
        #                      groupbyelem(event, itemgetter('user_id'))]
        if groupby == 'create_date':
            grouped_goal = [req.env['dh.strategic.objectives'].concat(*g) for k, g in
                            groupbyelem(goal, itemgetter('create_date'))]
        else:
            grouped_goal = [goal]

        values.update({
            'date': date_begin,
            'goal': goal,
            'grouped_goal': grouped_goal,
            'page_name': 'goal',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/goal',
            # 'searchbar_sortings': searchbar_sortings,
            # # 'searchbar_groupby': searchbar_groupby,
            # 'searchbar_inputs': searchbar_inputs,
            # 'search_in': search_in,
            # 'sortby': sortby,
            # 'groupby': groupby,
        })

        return req.render("icesco_portal.portal_my_goal", values)


    @http.route(['/my/kanban/goals', '/my/kanban/goals/page/<int:page>'], type='http', auth="user", website=True)
    def task_kanban_searchbar_goal(self, page=1, date_begin=None, date_end=None, sortby=None, groupby=None, filterby=None, search=None, search_in='name', **kw):

        # page_count  = request.env['ir.config_parameter'].sudo().get_param('website_project_kanbanview.tasks_page_count')
        page_count  = 0
        if int(page_count) > 0 :
            page_count_kanban  = int(page_count)
        else :
            page_count_kanban = 200

        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        searchbar_inputs = {
            'customer': {'input': 'name', 'label': _('Search in Name')},
        }
        searchbar_groupby = {
            'name': {'input': 'name', 'label': _('Name')},
        }

        # extends filterby criteria with project the customer has access to
        goals = request.env['dh.icesco.goal.strategies.kanban'].search([])

        # extends filterby criteria with goal (criteria name is the goal id)
        # Note: portal users can't view goals they don't follow
        # goal_groups = request.env['project.task'].read_group([('goal_id', 'not in', goals.ids)],
        #                                                         ['project_id'], ['project_id'])
        # for group in project_groups:
        #     proj_id = group['project_id'][0] if group['project_id'] else False
        #     proj_name = group['project_id'][1] if group['project_id'] else _('Others')
        #     searchbar_filters.update({
        #         str(proj_id): {'label': proj_name, 'domain': [('project_id', '=', proj_id)]}
        #     })

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']

        # archive groups - Default Group By 'create_date'
        # archive_groups = self._get_archive_groups('project.task', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])

            domain += search_domain

        # task count
        project_count = request.env['project.project'].sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/kanban/goals",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby, 'search_in': search_in, 'search': search},
            total=project_count,
            page=page,
            step=page_count_kanban
        )
        # content according to pager and archive selected
        if groupby == 'name':
            order = "name, %s" % order  # force sort on project first to group by project in view
        # projects = request.env['project.project'].search(domain, order=order, limit=page_count_kanban, offset=(page - 1) * page_count_kanban)
        # request.session['my_tasks_history'] = projects.ids[:100]
        # if groupby == 'name':
        #     grouped_projects_list = [request.env['project.project'].concat(*g) for k, g in groupbyelem(projects, itemgetter('name'))]
        # else:
        #     grouped_projects_list = [projects]
        # grouped_projects = [projects]

        values.update({
            'goals': goals,
            'date': date_begin,
            'date_end': date_end,
            # 'grouped_kanban_tasks': grouped_projects,
            # 'grouped_tasks': grouped_tasks_list,
            'page_name': 'goal',
            # 'archive_groups': archive_groups,
            'default_url': '/my/kanban/goals',
            'pager': pager,
            # 'searchbar_sortings': searchbar_sortings,
            # 'searchbar_groupby': searchbar_groupby,
            # 'searchbar_inputs': searchbar_inputs,
            # 'search_in': search_in,
            # 'sortby': sortby,
            # 'groupby': groupby,
            # 'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            # 'filterby': filterby,
        })
        return request.render("icesco_portal.goal_kanban_searchbar_goal", values)

    @http.route('/goal/create', type='http', auth="user", website=True)
    def view_goal_form_create(self, error=None, **kwargs):
        partner = req.env.user.partner_id.id

    @http.route(['/my/goal/<int:request_id>/pillars', '/my/goal/<int:request_id>/pillars/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_goal_pillars(self, page=1, date_begin=None, date_end=None, sortby=None, request_id=None, **kw):
        values = self._prepare_portal_layout_values()
        pilliers = request.env['dh.pilliar'].sudo()
        domain = [('orientation_id', '=', request_id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups('dh.pilliar', domain) if values.get('my_details') else []
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        # projects count
        pillier_count = pilliers.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/goal/" + str(request_id) + "/pillars",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=pillier_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        pillars = pilliers.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        # request.session['my_projects_history'] = prpillarsojects.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'pillars': pillars,
            'page_name': 'goal',
            'archive_groups': archive_groups,
            'default_url': "/my/goal/" + str(request_id) + "/pillars",
            'pager': pager,
            # 'searchbar_sortings': searchbar_sortings,
            # 'sortby': sortby
        })
        return request.render("icesco_portal.portal_my_pillars", values)

    @http.route(['/my/pillar/<int:request_id>/projects', '/my/pillar/<int:request_id>/projects/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_pillar_projects(self, page=1, date_begin=None, date_end=None, sortby=None, request_id=None, **kw):
        values = self._prepare_portal_layout_values()
        Project = request.env['project.project'].sudo()
        domain = [('pilliar_id', '=', request_id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups('project.project', domain) if values.get('my_details') else []
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        # projects count
        project_count = Project.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/pillar/"+str(request_id)+"/projects",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=project_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        projects = Project.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_projects_history'] = projects.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'projects': projects,
            'page_name': 'goal',
            'archive_groups': archive_groups,
            'default_url': "/my/pillar/"+str(request_id)+"/projects",
            'pager': pager,
            # 'searchbar_sortings': searchbar_sortings,
            # 'sortby': sortby
        })
        return request.render("icesco_portal.portal_my_projects", values)

    @http.route(['/my/tasks', '/my/tasks/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_tasks(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None,
                        search_in='content', groupby='project', **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Title'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        searchbar_inputs = {
            'content': {'input': 'content', 'label': _('Search <span class="nolabel"> (in Content)</span>')},
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'customer': {'input': 'customer', 'label': _('Search in Customer')},
            'stage': {'input': 'stage', 'label': _('Search in Stages')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'project': {'input': 'project', 'label': _('Project')},
        }

        # extends filterby criteria with project the customer has access to
        projects = request.env['project.project'].sudo().search([])
        for project in projects:
            searchbar_filters.update({
                str(project.id): {'label': project.name, 'domain': [('project_id', '=', project.id)]}
            })

        # extends filterby criteria with project (criteria name is the project id)
        # Note: portal users can't view projects they don't follow
        project_groups = request.env['project.task'].read_group([('project_id', 'not in', projects.ids)],
                                                                ['project_id'], ['project_id'])
        for group in project_groups:
            proj_id = group['project_id'][0] if group['project_id'] else False
            proj_name = group['project_id'][1] if group['project_id'] else _('Others')
            searchbar_filters.update({
                str(proj_id): {'label': proj_name, 'domain': [('project_id', '=', proj_id)]}
            })

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups('project.task', domain) if values.get('my_details') else []
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('content', 'all'):
                search_domain = OR([search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]])
            if search_in in ('customer', 'all'):
                search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
            if search_in in ('message', 'all'):
                search_domain = OR([search_domain, [('message_ids.body', 'ilike', search)]])
            if search_in in ('stage', 'all'):
                search_domain = OR([search_domain, [('stage_id', 'ilike', search)]])
            domain += search_domain

        # domain += AND([domain, [('create_uid', '=', req.env.uid)]])
        # task count
        task_count = request.env['project.task'].sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/tasks",
            # url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby,
            #           'search_in': search_in, 'search': search},
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=task_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        if groupby == 'project':
            order = "project_id, %s" % order  # force sort on project first to group by project in view
        tasks = request.env['project.task'].sudo().search(domain, order=order, limit=self._items_per_page,
                                                   offset=(page - 1) * self._items_per_page)
        request.session['my_tasks_history'] = tasks.ids[:100]
        if groupby == 'project':
            grouped_tasks = [request.env['project.task'].concat(*g) for k, g in
                             groupbyelem(tasks, itemgetter('project_id'))]
        else:
            grouped_tasks = [tasks]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_tasks': grouped_tasks,
            'page_name': 'project',
            'archive_groups': archive_groups,
            'default_url': '/my/tasks',
            'pager': pager,
            # 'searchbar_sortings': searchbar_sortings,
            # 'searchbar_groupby': searchbar_groupby,
            # 'searchbar_inputs': searchbar_inputs,
            # 'search_in': search_in,
            # 'sortby': sortby,
            # 'groupby': groupby,
            # 'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            # 'filterby': filterby,
        })
        return request.render("project.portal_my_tasks", values)

    @http.route(["/task/participate/<int:task_id>", "/task/participate<int:task_id>/<access_token>"], type='http',
                auth="public", website=True)
    def task_participate(self, task_id=None, access_token=None, **post):
        task = req.env['project.task'].sudo().search([('id', '=', task_id)])
        if task:
            task.write({'pays_members_cibles': [(4, req.env.user.partner_id.id)]})

            if task.project_id.id != False:
                return werkzeug.utils.redirect("/my/tasks?filterby=%s"  % (task.project_id.id))
            else:
                return werkzeug.utils.redirect("/my/tasks")
        else:
            if task.project_id.id != False:
                return werkzeug.utils.redirect("/my/tasks?filterby=%s" % (task.project_id.id))
            else:
                return werkzeug.utils.redirect("/my/tasks")

    @http.route(["/task/nonparticipate/<int:task_id>", "/task/nonparticipate<int:task_id>/<access_token>"], type='http',
                auth="public", website=True)
    def task_nonparticipate(self, task_id=None, access_token=None, **post):

        task = req.env['project.task'].sudo().search([('id', '=', task_id)])
        if task:
            task.write({'pays_members_cibles': [(3, req.env.user.partner_id.id)]})

            if task.project_id.id != False:
                return werkzeug.utils.redirect("/my/tasks?filterby=%s" % (task.project_id.id))
            else:
                return werkzeug.utils.redirect("/my/tasks")
        else:
            if task.roject_id.id != False:
                return werkzeug.utils.redirecpt("/my/tasks?filterby=%s" % (task.project_id.id))
            else:
                return werkzeug.utils.redirect("/my/tasks")

    @http.route('/task/create', type='http', auth="user", website=True)
    def view_task_form_createee(self, error=None, request_id=None, **kwargs):

        activities = req.env['dh.perf.type.activity'].sudo().search([])
        scopes = req.env['dh.scope.type'].sudo().search([])
        projects = req.env['project.project'].sudo().search([])

        # values = {
        #     'activities': activities,
        #     'scopes': scopes,
        #     'projects': projects,
        #     'project': False,
        # }
        # return req.render("icesco_portal.task_submit_projects", values)
        if req.context['lang'] in ['ar_AR', 'ar_SY']:
            types = [('local', 'محلي'), ('regional', 'إقليمي'), ('international', 'دولي')]
        else:
            types = [('local', 'Local'),('regional', 'Regional'),('international', 'International')]

        goals = req.env['dh.orientations'].sudo().search([])
        pillars = request.env['dh.pilliar'].sudo().search([])

        values = {
            'activities': activities,
            'scopes': scopes,
            'project': False,
            'types': types,
            'goals': goals,
            'pillars': pillars,
            'projects': projects,
            # 'project': False,
        }
        return req.render("icesco_portal.proposition_create", values)

    @http.route('/task/create/filterby=<int:request_id>', type='http', auth="user", website=True)
    def view_task_form_create(self, error=None, request_id=None, **kwargs):

        activities = req.env['dh.perf.type.activity'].sudo().search([])
        scopes = req.env['dh.scope.type'].sudo().search([])
        projects = req.env['project.project'].sudo().search([])
        name_project = req.env['project.project'].sudo().search([('id', '=', int(request_id))]).name
        if req.context['lang'] in ['ar_AR', 'ar_SY']:
            types = [('local', 'محلي'), ('regional', 'إقليمي'), ('international', 'دولي')]
        else:
            types = [('local', 'Local'),('regional', 'Regional'),('international', 'International')]
        goals = req.env['dh.orientations'].sudo().search([])
        pillars = request.env['dh.pilliar'].sudo().search([])

        values = {
            'activities': activities,
            'scopes': scopes,
            'projects': projects,
            'name_project': name_project,
            'project': request_id,
            'types': types,
            'goals': goals,
            'pillars': pillars,
        }
        return req.render("icesco_portal.task_submit", values)

    @http.route(["/task/add", "/task/add/<access_token>"],
                type='http', auth="user", website=True)
    def view_task_form_add(self, request_id=None, error=None, access_token=None, **post):
        try:
            proposal_note = False
            IrAttachment = req.env['ir.attachment']
            if post.get('concept_note', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                proposal_note = IrAttachment.create({
                    'name': post.get('concept_note', False).filename,
                    'datas': base64.b64encode(post.get('concept_note', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })
            data = {
                'name': post.get('name_task') if post.get('name_task', False) != 0 else False,
                'purpose': post.get('purpose_task') if post.get('purpose_task', False) != 0 else False,
                'activity_id': int(post.get('activity_id')) if int(
                    post.get('activity_id', False)) != 0 else False,
                'project_id': int(post.get('project_id')) if int(
                    post.get('project_id', False)) != 0 else False,
                'activity_scope': post.get('activity_scope') if post.get('activity_scope', False) else False,
                'remarks': post.get('remarks') if post.get('remarks', False) else False,
                'proposed_date': post.get('proposed_date').replace('T', ' ') if post.get('proposed_date', False) else False,
                'amount_usd': post.get('budget') if post.get('budget', False) else False,
                'is_budget_required': True if post.get('is_budget') == 'on' else False,
                'proposal_note': [(6, 0, [proposal_note.id])] if proposal_note else False,
            }

            task = req.env['project.task'].sudo().create(data)

            lines = []
            count = 0
            for key, value in post.items():  # iter on both keys and values
                if key.startswith('job_itle'):
                    count += 1

            if post.get('job_title'):
                attachment_ids = False
                IrAttachment = req.env['ir.attachment']
                if post.get('attachment_ids', False):
                    IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                    access_token = IrAttachment._generate_access_token()
                    attachment_ids = IrAttachment.create({
                        'name': post.get('attachment_ids', False).filename,
                        'datas': base64.b64encode(post.get('attachment_ids', False).read()),
                        # 'res_model': 'event.event',
                        # 'res_id': 0,
                        'access_token': access_token,
                    })
                lines.append({'name': post.get('invite_name') if post.get('invite_name', False) else False,
                              'job_title': post.get('job_title') if
                              post.get('job_title', False) else False,
                              'attachment_ids': [(6, 0, [attachment_ids.id])] if attachment_ids else False, })

            for i in range(count):
                if post.get('job_title_%s' % (i)):
                    attachment_ids = False
                    IrAttachment = req.env['ir.attachment']
                    if post.get('attachment_ids_%s' % (i), False):
                        IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                        access_token = IrAttachment._generate_access_token()
                        attachment_ids = IrAttachment.create({
                            'name': post.get('attachment_ids_%s' % (i), False).filename,
                            'datas': base64.b64encode(post.get('attachment_ids_%s' % (i), False).read()),
                            # 'res_model': 'event.event',
                            # 'res_id': 0,
                            'access_token': access_token,
                        })
                    lines.append(
                        {'name': post.get('invite_name_%s' % (i)) if post.get('invite_name_%s' % (i), False) else False,
                         'job_title': post.get('job_title_%s' % (i)) if post.get('job_title_%s' % (i),
                                                                                 False) else False,
                         'attachment_ids': [(6, 0, [attachment_ids.id])] if attachment_ids else False,
                         })

            data_proposition = {
                'name': post.get('name_task') if post.get('name_task', False) else False,
                'location': post.get('location') if post.get('location', False) else False,
                'city': post.get('city') if post.get('city', False) else False,
                'type': post.get('type') if post.get('type', False) else False,
                'is_sponsorise': post.get('is_sponsorise') if post.get('is_sponsorise', False) else False,
                'proposition_sponsor': post.get('proposition_sponsor') if post.get('proposition_sponsor',
                                                                                   False) else False,
                'number_participant_out_icesco': int(post.get('number_participant_out_icesco')) if int(
                    post.get('number_participant_out_icesco', False)) != False else 0,
                'number_billets': int(post.get('number_billets')) if int(
                    post.get('number_billets', False)) != False else 0,
                'number_residences': int(post.get('number_residences')) if int(
                    post.get('number_residences', False)) != False else 0,
                'task_id': task.id,
                'participant_ids': [(0, 0, line) for line in lines]
            }

            proposition = req.env['dh.icesco.proposition'].sudo().create(data_proposition)

            task.write({'proposition_id': proposition.id})

            return req.redirect("/my/tasks?filterby=%s" % (task.project_id.id))

        except Exception as e:
            error = str(e)
            return self.view_task_form_add(access_token=None, error=error, **post)

    @http.route('/proposition/create', type='http', auth="user", website=True)
    def view_proposition_form_createee(self, error=None, request_id=None, **kwargs):

        # activities = req.env['dh.perf.type.activity'].sudo().search([])
        # scopes = req.env['dh.scope.type'].sudo().search([])
        # projects = req.env['project.project'].sudo().search([])
        if req.context['lang'] in ['ar_AR', 'ar_SY']:
            types = [('local', 'محلي'), ('regional', 'إقليمي'), ('international', 'دولي')]
        else:
            types = [('local', 'Local'),('regional', 'Regional'),('international', 'International')]

        goals = req.env['dh.orientations'].sudo().search([])
        pillars = request.env['dh.pilliar'].sudo().search([])
        projects = req.env['project.project'].sudo().search([])
        activities = req.env['dh.perf.type.activity'].sudo().search([])
        scopes = req.env['dh.scope.type'].sudo().search([])

        values = {
            'types': types,
            'goals': goals,
            'pillars': pillars,
            'projects': projects,
            'activities': activities,
            'scopes': scopes,
            # 'project': False,
        }
        return req.render("icesco_portal.proposition_create", values)

    @http.route(["/proposition/add", "/proposition/add/<access_token>"],
                type='http', auth="user", website=True)
    def view_proposition_form_add(self, request_id=None, error=None, access_token=None, **post):
        try:
            proposal_note = False
            IrAttachment = req.env['ir.attachment']
            if post.get('concept_note', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                proposal_note = IrAttachment.create({
                    'name': post.get('concept_note', False).filename,
                    'datas': base64.b64encode(post.get('concept_note', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })
            data_task = {
                'name': post.get('name_task') if post.get('name_task', False) else False,
                'purpose': post.get('purpose_task') if post.get('purpose_task', False) else False,
                'activity_id': int(post.get('activity_id')) if int(
                    post.get('activity_id', False)) != 0 else False,
                'project_id': int(post.get('project_id')) if int(
                    post.get('project_id', False)) != 0 else False,
                'activity_scope': post.get('activity_scope') if post.get('activity_scope', False) else False,
                'remarks': post.get('remarks') if post.get('remarks', False) else False,
                'proposed_date': post.get('proposed_date').replace('T', ' ') if post.get('proposed_date',
                                                                                         False) else False,
                'amount_usd': post.get('budget') if post.get('budget', False) else False,
                'is_budget_required': True if post.get('is_budget') == 'on' else False,
                'proposal_note': [(6, 0, [proposal_note.id])] if proposal_note else False,
            }

            task = req.env['project.task'].sudo().create(data_task)

            lines = []
            count = 0
            for key, value in post.items():  # iter on both keys and values
                if key.startswith('job_itle'):
                    count += 1

            if post.get('job_title'):
                attachment_ids = False
                IrAttachment = req.env['ir.attachment']
                if post.get('attachment_ids', False):
                    IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                    access_token = IrAttachment._generate_access_token()
                    attachment_ids = IrAttachment.create({
                        'name': post.get('attachment_ids', False).filename,
                        'datas': base64.b64encode(post.get('attachment_ids', False).read()),
                        # 'res_model': 'event.event',
                        # 'res_id': 0,
                        'access_token': access_token,
                    })
                lines.append({'name': post.get('invite_name') if post.get('invite_name', False) else False,
                              'job_title': post.get('job_title') if
                                  post.get('job_title', False) else False,
                              'attachment_ids': [(6, 0, [attachment_ids.id])] if attachment_ids else False,})

            for i in range(count):
                if post.get('job_title_%s' %(i)):
                    attachment_ids = False
                    IrAttachment = req.env['ir.attachment']
                    if post.get('attachment_ids_%s' %(i), False):
                        IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                        access_token = IrAttachment._generate_access_token()
                        attachment_ids = IrAttachment.create({
                            'name': post.get('attachment_ids_%s' %(i), False).filename,
                            'datas': base64.b64encode(post.get('attachment_ids_%s' %(i), False).read()),
                            # 'res_model': 'event.event',
                            # 'res_id': 0,
                            'access_token': access_token,
                        })
                    lines.append({'name': post.get('invite_name_%s' %(i)) if post.get('invite_name_%s' %(i),False) else False,
                                  'job_title': post.get('job_title_%s' %(i)) if post.get('job_title_%s' %(i),False) else False,
                                  'attachment_ids': [(6, 0, [attachment_ids.id])] if attachment_ids else False,
                                  })

            data_proposition = {
                'name': post.get('name_task') if post.get('name_task', False) else False,
                'location': post.get('location') if post.get('location', False) else False,
                'city': post.get('city') if post.get('city', False) else False,
                'type': post.get('type') if post.get('type', False) else False,
                'is_sponsorise': post.get('is_sponsorise') if post.get('is_sponsorise', False) else False,
                'proposition_sponsor': post.get('proposition_sponsor') if post.get('proposition_sponsor', False) else False,
                'number_participant_out_icesco': int(post.get('number_participant_out_icesco')) if int(post.get('number_participant_out_icesco', False)) != False else 0,
                'number_billets': int(post.get('number_billets')) if int(post.get('number_billets', False)) != False else 0,
                'number_residences': int(post.get('number_residences')) if int(post.get('number_residences', False)) != False else 0,
                'task_id': task.id,
                'participant_ids': [(0, 0, line) for line in lines]

            }

            proposition = req.env['dh.icesco.proposition'].sudo().create(data_proposition)

            task.write({'proposition_id': proposition.id})

            return req.redirect("/proposition/create")

        except Exception as e:
            error = str(e)
            return self.view_proposition_form_add(access_token=None, error=error, **post)

    @http.route('/project/create', type='http', auth="user", website=True)
    def view_project_form_create(self, error=None, **kwargs):

        goals = req.env['dh.strategic.objectives'].sudo().search([])
        print('test', http.request.httprequest.full_path)
        values = {
            'goals': goals,
            'goal': 0,
        }
        return req.render("icesco_portal.project_submit", values)

    @http.route(["/project/add", "/project/add/<access_token>"],
                type='http', auth="user", website=True)
    def view_project_form_add(self, request_id=None, error=None, access_token=None, **post):
        try:

            data = {
                'name': post.get('name_project') if post.get('name_project', False) != 0 else False,
                'strategic_id': int(post.get('goal_id')) if int(
                    post.get('goal_id', False)) != 0 else False,
            }

            project = req.env['project.project'].create(data)

            return req.redirect("/my/goal/"+str(project.strategic_id.id)+"/projects")
            # return req.redirect("/my/projects")

        except Exception as e:
            error = str(e)
            return self.view_project_form_add(access_token=None, error=error, **post)

class PortalPartner(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalPartner, self)._prepare_portal_layout_values()
        domain = [('is_member_state', '=', True)]
        orders_count = req.env['res.partner'].sudo().search_count(
            domain)
        values['members_count'] = orders_count
        return values

    def _partner_get_page_view_values(self, partner, access_token, **kwargs):
        values = {
            'page_name': 'partner',
            'partner': partner,
        }
        return self._get_page_view_values(partner, access_token, values,
                                          'my_partners_history', False, **kwargs)

    @http.route(['/my/partner', '/my/partner/page/<int:page>'], type='http', auth="user",
                website=True)
    def portal_my_partner(self, page=1, date_begin=None, date_end=None, search=None,
                       search_in='all',
                       groupby='user_id', sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = req.env['res.partner'].sudo()
        domain = [('is_member_state', '=', True)]
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Member State'), 'order': 'name'},
        }

        # default sort by order id = top_menu_collapse
        # searchbar_groupby = {
        #     'none': {'input': 'none', 'label': _('None')},
        #     'create_date': {'input': 'create_date', 'label': _('Create date')},
        # }

        searchbar_inputs = {
            'name': {'input': 'name', 'label': _('Search in name')},

            # 'create_date': {'input': 'create_date', 'label': _('Search in create date')},
            # 'all': {'input': 'all', 'label': _('Search in name')},
            # 'ref_ext': {'input': 'ref_ext', 'label': _('Search in External Reference')},
        }

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        if search and search_in:
            search_domain = []
            # if search_in in ('content', 'all'):
            #     search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            # if search_in in ('user_id', 'all'):
            #     search_domain = OR(
            #         [search_domain, [('user_id', 'ilike', search)]])

            # if search_in in ('create_date', 'all'):
            #     search_domain = OR(
            #         [search_domain, [('create_date', 'ilike', search)]])
            domain += search_domain

        # if search and search_in:
        #     domain = AND([domain, [('name', 'ilike', search)]])

        # count for pager
        partner_count = partner.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/partner",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby,
                      'search_in': search_in, 'groupby': groupby,
                      'search': search, },
            total=partner_count,
            page=page,
            step=self._items_per_page
        )

        archive_groups = self._get_archive_groups('res.partner',
                                                  domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin),
                       ('create_date', '<=', date_end)]

        # content according to pager and archive selected
        # if groupby == 'state':
        #     order = "state, %s" % order
        # if groupby == 'user_id':
        #     order = "user_id, %s" % order
        if groupby == 'create_date':
            order = "create_date, %s" % order

        partner = partner.search(domain, order=order, limit=self._items_per_page,
                           offset=pager['offset'])

        req.session['my_partners_history'] = partner.ids[:100]

        # if groupby == 'state':
        #     grouped_event = [req.env['event.event'].concat(*g) for
        #                      k, g in
        #                      groupbyelem(event, itemgetter('state'))]
        # elif groupby == 'user_id':
        #     grouped_event = [req.env['event.event'].concat(*g) for
        #                      k, g in
        #                      groupbyelem(event, itemgetter('user_id'))]
        if groupby == 'create_date':
            grouped_partner = [req.env['res.partner'].concat(*g) for k, g in
                            groupbyelem(partner, itemgetter('create_date'))]
        else:
            grouped_partner = [partner]

        values.update({
            'date': date_begin,
            'partner': partner,
            'grouped_partner': grouped_partner,
            'page_name': 'partner',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/partner',
            # 'searchbar_sortings': searchbar_sortings,
            # 'searchbar_groupby': searchbar_groupby,
            # 'searchbar_inputs': searchbar_inputs,
            # 'search_in': search_in,
            # 'sortby': sortby,
            # 'groupby': groupby,
        })

        return req.render("icesco_portal.portal_my_partner", values)


    @http.route(['/my/kanban/partners', '/my/kanban/partners/page/<int:page>'], type='http', auth="user", website=True)
    def member_kanban_searchbar_partner(self, page=1, date_begin=None, date_end=None, sortby=None, groupby=None, filterby=None, search=None, search_in='name', **kw):

        # page_count  = request.env['ir.config_parameter'].sudo().get_param('website_project_kanbanview.tasks_page_count')
        page_count  = 0
        if int(page_count) > 0 :
            page_count_kanban  = int(page_count)
        else :
            page_count_kanban = 200

        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        searchbar_inputs = {
            'name': {'input': 'name', 'label': _('Search in Name')},
        }
        searchbar_groupby = {
            'name': {'input': 'name', 'label': _('Name')},
        }

        # extends filterby criteria with project the customer has access to
        partners = request.env['res.partner'].sudo().search([('is_member_state', '=', True)], order="dh_order asc")

        # extends filterby criteria with partner (criteria name is the partner id)
        # Note: portal users can't view partners they don't follow
        # partner_groups = request.env['project.member'].read_group([('partner_id', 'not in', partners.ids)],
        #                                                         ['project_id'], ['project_id'])
        # for group in project_groups:
        #     proj_id = group['project_id'][0] if group['project_id'] else False
        #     proj_name = group['project_id'][1] if group['project_id'] else _('Others')
        #     searchbar_filters.update({
        #         str(proj_id): {'label': proj_name, 'domain': [('project_id', '=', proj_id)]}
        #     })

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']

        # archive groups - Default Group By 'create_date'
        # archive_groups = self._get_archive_groups('project.member', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])

            domain += [('is_member_state', '=', True)]
            domain += search_domain
            partners = request.env['res.partner'].sudo().search(domain)

        # member count
        project_count = request.env['res.partner'].sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/kanban/partners",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby, 'search_in': search_in, 'search': search},
            total=project_count,
            page=page,
            step=page_count_kanban
        )
        # content according to pager and archive selected
        if groupby == 'name':
            order = "name, %s" % order  # force sort on project first to group by project in view
        # projects = request.env['project.project'].search(domain, order=order, limit=page_count_kanban, offset=(page - 1) * page_count_kanban)
        # request.session['my_members_history'] = projects.ids[:100]
        # if groupby == 'name':
        #     grouped_projects_list = [request.env['project.project'].concat(*g) for k, g in groupbyelem(projects, itemgetter('name'))]
        # else:
        #     grouped_projects_list = [projects]
        # grouped_projects = [projects]

        values.update({
            'partners': partners,
            'date': date_begin,
            'date_end': date_end,
            # 'grouped_kanban_members': grouped_projects,
            # 'grouped_members': grouped_members_list,
            'page_name': 'partners',
            # 'archive_groups': archive_groups,
            'default_url': '/my/kanban/partners',
            'pager': pager,
            # 'searchbar_sortings': searchbar_sortings,
            # 'searchbar_groupby': searchbar_groupby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            # 'sortby': sortby,
            # # 'groupby': groupby,
            # 'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            # 'filterby': filterby,
        })
        return request.render("icesco_portal.partner_kanban_searchbar_partner", values)

    @http.route(['/my/kanban/partners/<int:request_id>'], type='http', auth="user", website=True)
    def member_state_partner(self, page=1, request_id=None ,date_begin=None, date_end=None, sortby=None, groupby=None,
                                        filterby=None, search=None, search_in='name', **kw):
        values = []
        partner = req.env['res.partner'].sudo().search([('id', '=', request_id)])
        countries = req.env['res.country'].sudo().search([])
        capital_countries = req.env['res.city'].sudo().search([])
        states = req.env['res.country.state'].sudo().search([])
        langagues = req.env['dh.lang'].sudo().search([])

        values = {
            'partner': partner,
            'countries': countries,
            'capital_countries': capital_countries,
            'official_languages': langagues,
            'used_languages': langagues,
            'page_name': 'partner',
            'states': states,
        }
        return request.render("icesco_portal.portal_partner_details", values)

    @http.route('/contact_us', type='http', auth="public", website=True)
    def view_contactus(self, error=None, request_id=None, **kwargs):

        department = req.env['dh.perf.sector'].sudo().search([])
        amana = req.env['res.partner'].sudo().search([('is_amana', '=', True)], limit=1)
        commission = req.env['res.partner'].sudo().search([('is_commission', '=', True)])

        values = {
            'departments': department,
            'commissions': commission,
            'amana_name': amana.display_name,
            'error': error,
        }
        return req.render("icesco_portal.contact_us", values)

    @http.route('/contactus/sent', type='http', auth="user", website=True)
    def submit_contact_us(self, error=None, access_token=None, **post):
        try:
            manager_department = req.env['hr.department'].sudo().search([('id', '=', int(post.get('department_id')))]).manager_id
            support_docs = False
            IrAttachment = req.env['ir.attachment']
            if post.get('support_docs', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                support = IrAttachment.create({
                    'name': post.get('support_docs', False).filename,
                    'datas': base64.b64encode(post.get('support_docs', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })
                support_docs = support.id

            official_request = False
            IrAttachment = req.env['ir.attachment']
            if post.get('official_request', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                request = IrAttachment.create({
                    'name': post.get('official_request', False).filename,
                    'datas': base64.b64encode(post.get('official_request', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })
                official_request = request.id

            email_amana = False
            email_amana = req.env['res.partner'].sudo().search([('is_amana', '=', True)], limit=1).email

            mail = req.env['mail.mail'].sudo().create({'email_from': 'it@icesco.org', 'email_to': manager_department.work_email, 'email_cc': email_amana, 'subject': post.get('subject'), 'body_html': '<p>- %s</p><br/><p>- %s</p><br/>Cordialement' % (post.get('resume'), post.get('required'))})
            if support_docs != False:
                mail.write({'attachment_ids': [(4, support_docs)]})

            if official_request != False:
                mail.write({'attachment_ids': [(4, official_request)]})

            mail.send()

            return local_redirect("/contact_us")

        except Exception as e:
            print(e)
            error = str(e)
            return self.view_contactus(error=error)
        # except:
        #     error = str("Something went wrong")
        #     return self.view_event_form_create(error=error)

    @http.route('/contactcommission/sent', type='http', auth="user", website=True)
    def submit_contact_commission(self, error=None, access_token=None, **post):
        try:
            commission = req.env['hr.department'].sudo().search(
                [('id', '=', int(post.get('commission_id')))])
            support_docs = False
            IrAttachment = req.env['ir.attachment']
            if post.get('com_support_docs', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                support = IrAttachment.create({
                    'name': post.get('com_support_docs', False).filename,
                    'datas': base64.b64encode(post.get('com_support_docs', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })
                support_docs = support.id

            com_official_request = False
            IrAttachment = req.env['ir.attachment']
            if post.get('com_official_request', False):
                IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
                access_token = IrAttachment._generate_access_token()
                request = IrAttachment.create({
                    'name': post.get('com_official_request', False).filename,
                    'datas': base64.b64encode(post.get('com_official_request', False).read()),
                    # 'res_model': 'event.event',
                    # 'res_id': 0,
                    'access_token': access_token,
                })
                com_official_request = request.id

            email_amana = False
            email_amana = req.env['res.partner'].sudo().search([('is_amana', '=', True)], limit=1).email
            if post.get('copy_aussi_to') != False and email_amana:
                email_cc = email_amana + ', ' + post.get('copy_aussi_to')
            elif post.get('copy_aussi_to') == False and email_amana:
                email_cc = email_amana
            elif post.get('copy_aussi_to') != False and email_amana == False:
                email_cc = post.get('copy_aussi_to')
            else:
                email_cc = False

            mail = req.env['mail.mail'].sudo().create({'email_from': 'it@icesco.org', 'email_to': manager_department.work_email,
                                         'email_cc': email_cc, 'subject': post.get('com_subject'),
                                         'body_html': '<p>%s</p><br/><p>%s</p><br/>Cordialement' % (post.get('com_resume'), post.get('com_required')),
                                         })
            if support_docs != False:
                mail.write({'attachment_ids': [(4, support_docs)]})

            if com_official_request != False:
                mail.write({'attachment_ids': [(4, com_official_request)]})

            mail.send()

            return local_redirect("/contact_us")

        except Exception as e:
            print(e)
            error = str(e)
            return self.view_contactus(error=error)
        # except:
        #     error = str("Something went wrong")
        #     return self.view_event_form_create(error=error)