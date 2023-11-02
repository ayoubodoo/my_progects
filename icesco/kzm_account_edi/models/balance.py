# -*- encoding: utf-8 -*-
import base64
import datetime as dt
from lxml import etree
from pprint import pprint

from odoo import models, fields, api
from odoo.exceptions import ValidationError
# from openerp.osv import fields, osv
from odoo import tools

# from .report.common_balance_reports import CommonBalanceReportHeaderWebkit

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


class liasse_balance_line(models.Model):

    @api.depends('init_balance', 'debit', 'credit')
    def _solde_fin_debit(self):

        for record in self:
            # if record.compte[:1] in ['2','3','5','6']:
            solde = record.init_balance + record.debit - record.credit
            record.sf_debit = solde if solde > 0 else 0

    @api.depends('init_balance', 'debit', 'credit')
    def _solde_fin_credit(self):
        for record in self:
            # if record.compte[:1] in ['2','3','5','6']:
            solde = record.init_balance + record.debit - record.credit
            if solde < 0:
                record.sf_credit = -solde
            else:
                record.sf_credit = 0

    @api.depends('debit', 'credit')
    def _solde_fin(self):
        for record in self:
            solde = record.sf_debit - record.sf_credit
            record.solde = solde
            if record.compte:
                if record.compte.startswith('4') or record.compte.startswith('1') or record.compte.startswith(
                        '55') or record.compte.startswith('59') or record.compte.startswith('7'):
                    record.solde = -solde
                if record.compte.startswith('28') or record.compte.startswith('29') or record.compte.startswith('39'):
                    record.solde = -solde

    _name = "liasse.balance.line"
    _description = "liasse.balance.line"

    exercice = fields.Many2one('date.range', 'Exercice', domain=[('kzm_is_fiscalyear', '=', True)],
                               related="balance_id.name")
    compte = fields.Char('Compte ', required=True)
    lib = fields.Char('Libelle ')
    init_balance = fields.Float('Solde debut')
    debit = fields.Float('Mouvement debit')
    credit = fields.Float('Mouvement credit')
    sf_debit = fields.Float(compute=_solde_fin_debit, string='Solde fin debit')
    sf_credit = fields.Float(compute=_solde_fin_credit, string='Solde fin credit')
    solde = fields.Float(compute=_solde_fin, string='Solde fin')
    balance_id = fields.Many2one('liasse.balance.erp', 'Balance ID', ondelete='cascade', index=True)

    _rec_name = 'compte'


class liasse_balance(models.Model):
    _name = "liasse.balance.erp"
    _description = "liasse.balance.erp"

    def see_balances(self):
        action = self.env.ref('kzm_account_edi.liasse_balance_action').read()[0]
        action['domain'] = [('balance_id', '=', self.id)]
        action['context'] =  {'default_balance_id': self.id}
        action['views'] = [(self.env.ref('kzm_account_edi.liasse_balance_line_view_tree').id, 'tree'),
                           (self.env.ref('kzm_account_edi.liasse_balance_line_view_form').id, 'form')]
        return action

    def _get_pm_cp(self):
        # pm_table = self.env['pm.value.erp']
        total = 0
        for r in self:
            for pm_obj in r.pm_value:
                # pm_obj = pm_table.browse(pm)
                total += pm_obj.compte_princ
            r.pm_compte_princ = total
        print(total)

    def _get_pm_mb(self):
        # pm_table = self.env['pm.value.erp']
        total = 0
        for r in self:
            for pm_obj in r.pm_value:
                # pm_obj = pm_table.browse(pm)
                total += pm_obj.montant_brut
            r.pm_montant_brut = total

    def _get_pm_ac(self):
        pm_table = self.env['pm.value.erp']
        res = {}
        total = 0
        for r in self:
            for pm_obj in r.pm_value:
                # pm_obj = pm_table.browse(pm)
                total += pm_obj.amort_cumul
            r.pm_amort_cumul = total

    def _get_pm_vna(self):
        # pm_table = self.env['pm.value.erp']

        total = 0
        for r in self:
            for pm_obj in r.pm_value:
                # pm_obj = pm_table.browse(pm)
                total += pm_obj.val_net_amort
            r.pm_val_net_amort = total

    def _get_pm_pc(self):
        # pm_table = self.env['pm.value.erp']
        total = 0
        for r in self:
            for pm_obj in r.pm_value:
                # pm_obj = pm_table.browse(cr,uid,pm)
                total += pm_obj.prod_cess
            r.pm_prod_cess = total

    def _get_pm_pv(self):
        # pm_table = self.env['pm.value.erp']
        total = 0
        for r in self:
            for pm_obj in r.pm_value:
                # pm_obj = pm_table.browse(cr,uid,pm)
                total += pm_obj.plus_value
            r.pm_plus_value = total

    def _get_pm_mv(self):
        # pm_table = self.env['pm.value.erp']
        total = 0
        for r in self:
            for pm_obj in r.pm_value:
                # pm_obj = pm_table.browse(cr,uid,pm)
                total += pm_obj.moins_value
            r.pm_moins_value = total

    def _get_tp_cp(self):
        # tp_table = self.env['titre.particip.erp']

        total = 0
        for r in self:
            for tp_obj in r.titre_particip:
                # tp_obj = tp_table.browse(cr,uid,tp)
                total += tp_obj.capit_social
            r.tp_capit_social = total

    def _get_tp_pc(self):
        # tp_table = self.env['titre.particip.erp']
        total = 0
        for r in self:
            for tp_obj in r.titre_particip:
                # tp_obj = tp_table.browse(cr,uid,tp)
                total += tp_obj.particip_cap
            r.tp_particip_cap = total

    def _get_tp_pg(self):
        # tp_table = self.env['titre.particip.erp']

        total = 0
        for r in self:
            for tp_obj in r.titre_particip:
                # tp_obj = tp_table.browse(cr,uid,tp)
                total += tp_obj.prix_global
            r.tp_prix_global = total

    def _get_tp_vc(self):
        # tp_table = self.env['titre.particip.erp']
        total = 0
        for r in self:
            for tp_obj in r.titre_particip:
                # tp_obj = tp_table.browse(cr,uid,tp)
                total += tp_obj.val_compt
            r.tp_val_compt = total

    def _get_tp_es(self):
        # tp_table = self.env['titre.particip.erp']
        total = 0
        for r in self:
            for tp_obj in r.titre_particip:
                # tp_obj = tp_table.browse(cr,uid,tp)
                total += tp_obj.extr_situation
            r.tp_extr_situation = total

    def _get_tp_er(self):
        # tp_table = self.env['titre.particip.erp']

        total = 0
        for r in self:
            for tp_obj in r.titre_particip:
                # tp_obj = tp_table.browse(cr,uid,tp)
                total += tp_obj.extr_resultat
            r.tp_extr_resultat = total

    def _get_tp_pi(self):
        # tp_table = self.env['titre.particip.erp']

        total = 0
        for r in self:
            for tp_obj in r.titre_particip:
                # tp_obj = tp_table.browse(cr,uid,tp)
                total += tp_obj.prod_inscrit
            r.tp_prod_inscrit = total

    def _get_in_mt(self):
        # in_table = self.env['interets.erp']
        total = 0
        for r in self:
            for int_obj in r.interets_associe:
                # int_obj = in_table.browse(cr,uid,int)
                total += int_obj.mont_pretl
            for int in r.interets_tier:
                # int_obj = in_table.browse(cr,uid,int)
                total += int.mont_pretl
            r.in_mont_pretl = total

    def _get_in_cg(self):
        # in_table = self.env['interets.erp']

        total = 0
        for r in self:
            for int_obj in r.interets_associe:
                # int_obj = in_table.browse(cr,uid,int)
                total += int_obj.charge_global
            for int in r.interets_tier:
                # int_obj = in_table.browse(cr,uid,int)
                total += int.charge_global
            r.in_charge_global = total

    def _get_in_rp(self):
        # in_table = self.env['interets.erp']

        total = 0
        for r in self:
            for int_obj in r.interets_associe:
                # int_obj = in_table.browse(cr,uid,int)
                total += int_obj.remb_princ
            for int in r.interets_tier:
                # int_obj = in_table.browse(cr,uid,int)
                total += int.remb_princ
            r.in_remb_princ = total

    def _get_in_ri(self):
        # in_table = self.env['interets.erp']
        total = 0
        for r in self:
            for int_obj in r.interets_associe:
                # int_obj = in_table.browse(cr,uid,int)
                total += int_obj.remb_inter
            for int in r.interets_tier:
                # int_obj = in_table.browse(cr,uid,int)
                total += int.remb_inter
            r.in_remb_inter = total

    def _get_in_rap(self):
        # in_table = self.env['interets.erp']
        total = 0
        for r in self:
            for int_obj in r.interets_associe:
                # int_obj = in_table.browse(cr,uid,int)
                total += int_obj.remb_actual_princ
            for int in r.interets_tier:
                # int_obj = in_table.browse(cr,uid,int)
                total += int.remb_actual_princ
            r.in_remb_actual_princ = total

    def _get_in_rai(self):
        # in_table = self.env['interets.erp']

        total = 0
        for r in self:
            for int_obj in r.interets_associe:
                # int_obj = in_table.browse(cr,uid,int)
                total += int_obj.remb_actual_inter
            for int in r.interets_tier:
                # int_obj = in_table.browse(cr,uid,int)
                total += int.remb_actual_inter
            r.in_remb_actual_inter = total

    def _get_bx_ml(self):
        # beaux_table = self.env['beaux.erp']

        total = 0
        for r in self:
            for bx_obj in r.beaux:
                # bx_obj = beaux_table.browse(cr,uid,bx)
                total += bx_obj.mont_annuel
            r.bx_mont_pretl = total

    def _get_bx_mc(self):
        # beaux_table = self.env['beaux.erp']

        total = 0
        for r in self:
            for bx_obj in r.beaux:
                # bx_obj = beaux_table.browse(cr,uid,bx)
                total += bx_obj.mont_loyer
            r.bx_charge_global = total

    def _get_p_mp(self):
        # passage_table = self.env['passage.erp']

        total = 0
        for r in self:
            for tp_obj in r.passages_rfc:
                # tp_obj = passage_table.browse(cr,uid,tp)
                total += tp_obj.montant1
            for tp_obj in r.passages_rfnc:
                # tp_obj = passage_table.browse(cr,uid,tp)
                total += tp_obj.montant1
            total += r.p_benifice_p
            r.p_total_montantp = total

    def _get_p_mm(self):
        # passage_table = self.env['passage.erp']

        total = 0
        for r in self:
            for tp_obj in r.passages_dfc:
                # tp_obj = passage_table.browse(cr,uid,tp)
                total += tp_obj.montant2
            for tp_obj in r.passages_dfnc:
                # tp_obj = passage_table.browse(cr,uid,tp)
                total += tp_obj.montant2
            total += r.p_perte_m
            r.p_total_montantm = total

    def _get_p_bbf(self):

        total = 0
        for r in self:
            if r.p_total_montantp > r.p_total_montantm:
                total = r.p_total_montantp - r.p_total_montantm
            r.p_benificebm = total

    def _get_p_dbf(self):
        res = {}
        total = 0
        for r in self:
            if r.p_total_montantp < r.p_total_montantm:
                total = r.p_total_montantm - r.p_total_montantp
            r.p_deficitfm = total

    def _get_p_dnf(self):
        for r in self:
            total = r.p_deficitfm
            r.p_deficitnfm = total

    def _get_aff_ta(self):

        for r in self:
            total = r.aff_rep_n + r.aff_res_n_in + r.aff_res_n_ex + r.aff_prev + r.aff_autre_prev
            r.aff_totala = total

    def _get_aff_tb(self):

        for r in self:
            total = r.aff_rl + r.aff_autre_r + r.aff_tant + r.aff_div + r.aff_autre_aff + r.aff_rep_n2
            r.aff_totalb = total

    def _get_encp_ep(self):

        for r in self:
            total = (r.vente_imp_ep + r.vente_ex100_ep + r.vente_ex50_ep + r.vente_li_ep + r.vente_lex100_ep +
                     r.vente_lex50_ep + r.pres_imp_ep + r.pres_ex100_ep + r.pres_ex50_ep + r.prod_acc_ep +
                     r.prod_sub_ep + r.sub_eq_ep + r.sub_imp_ep + r.sub_ex100_ep + r.sub_ex50_ep)
            r.taux_part_ep = total

    def _get_encp_epi(self):
        res = {}
        total = 0
        for r in self:
            total = (r.vente_imp_epi + r.vente_ex100_epi + r.vente_ex50_epi + r.vente_li_epi + r.vente_lex100_epi +
                     r.vente_lex50_epi + r.pres_imp_epi + r.pres_ex100_epi + r.pres_ex50_epi + r.prod_acc_epi +
                     r.prod_sub_epi + r.sub_eq_epi + r.sub_imp_epi + r.sub_ex100_epi + r.sub_ex50_epi)
            r.taux_part_epi = total
        return res

    def _get_encp_ept(self):

        for r in self:
            total = (r.vente_imp_ept + r.vente_ex100_ept + r.vente_ex50_ept + r.vente_li_ept + r.vente_lex100_ept +
                     r.vente_lex50_ept + r.pres_imp_ept + r.pres_ex100_ept + r.pres_ex50_ept + r.prod_acc_ept +
                     r.prod_sub_ept + r.sub_eq_ept + r.sub_imp_ept + r.sub_ex100_ept + r.sub_ex50_ept)
            r.taux_part_ept = total

    def _get_encg_ep(self):
        res = {}
        total = 0
        for r in self:
            total = (r.vente_imp_ep + r.vente_ex100_ep + r.vente_ex50_ep + r.vente_li_ep + r.vente_lex100_ep +
                     r.vente_lex50_ep + r.pres_imp_ep + r.pres_ex100_ep + r.pres_ex50_ep + r.prod_acc_ep +
                     r.prod_sub_ep + r.sub_eq_ep + r.sub_imp_ep + r.sub_ex100_ep + r.sub_ex50_ep +
                     r.profit_g_ep + r.profit_ex_ep)
            r.total_g_ep = total

    def _get_encg_epi(self):

        for r in self:
            total = (r.vente_imp_epi + r.vente_ex100_epi + r.vente_ex50_epi + r.vente_li_epi + r.vente_lex100_epi +
                     r.vente_lex50_epi + r.pres_imp_epi + r.pres_ex100_epi + r.pres_ex50_epi + r.prod_acc_epi +
                     r.prod_sub_epi + r.sub_eq_epi + r.sub_imp_epi + r.sub_ex100_epi + r.sub_ex50_epi +
                     r.profit_g_epi + r.profit_ex_epi)
            r.total_g_epi = total

    def _get_encg_ept(self):
        res = {}
        total = 0
        for r in self:
            total = (r.vente_imp_ept + r.vente_ex100_ept + r.vente_ex50_ept + r.vente_li_ept + r.vente_lex100_ept +
                     r.vente_lex50_ept + r.pres_imp_ept + r.pres_ex100_ept + r.pres_ex50_ept + r.prod_acc_ept +
                     r.prod_sub_ept + r.sub_eq_ept + r.sub_imp_ept + r.sub_ex100_ept + r.sub_ex50_ept +
                     r.profit_g_ept + r.profit_ex_ept)
            r.total_g_ept = total

    # immo

    def _get_immonv_mbi(self):
        res = {}
        total = 0
        for r in self:
            total = (r.fp_mb + r.charge_mb + r.prime_mb)
            r.immonv_mb = total

    def _get_immonv_aug_acq(self):
        res = {}
        total = 0
        for r in self:
            total = (r.fp_aug_acq + r.charge_aug_acq + r.prime_aug_acq)
            r.immonv_aug_acq = total

    def _get_immonv_aug_pd(self):
        res = {}
        total = 0
        for r in self:
            total = (r.fp_aug_pd + r.charge_aug_pd + r.prime_aug_pd)
            r.immonv_aug_pd = total

    def _get_immonv_aug_vir(self):
        res = {}
        total = 0
        for r in self:
            total = (r.fp_aug_vir + r.charge_aug_vir + r.prime_aug_vir)
            r.immonv_aug_vir = total

    def _get_immonv_dim_cess(self):
        res = {}
        total = 0
        for r in self:
            total = (r.fp_dim_cess + r.charge_dim_cess + r.prime_dim_cess)
            r.immonv_dim_cess = total

    def _get_immonv_dim_ret(self):
        res = {}
        total = 0
        for r in self:
            total = (r.fp_dim_ret + r.charge_dim_ret + r.prime_dim_ret)
            r.immonv_dim_ret = total

    def _get_immonv_dim_vir(self):
        res = {}
        total = 0
        for r in self:
            total = (r.fp_dim_vir + r.charge_dim_vir + r.prime_dim_vir)
            r.immonv_dim_vir = total

    def _get_immonv_mbf(self):
        res = {}
        total = 0
        for r in self:
            total = (r.fp_mbf + r.charge_mbf + r.prime_mbf)
            r.immonv_mbf = total

    def _get_immoi_mbi(self):
        res = {}
        total = 0
        for r in self:
            total = (r.immord_mb + r.brevet_mb + r.fond_mb + r.autre_incorp_mb)
            r.immoi_mb = total

    def _get_immoi_aug_acq(self):
        res = {}
        total = 0
        for r in self:
            total = (r.immord_aug_acq + r.brevet_aug_acq + r.fond_aug_acq + r.autre_incorp_aug_acq)
            r.immoi_aug_acq = total

    def _get_immoi_aug_pd(self):

        for r in self:
            total = (r.immord_aug_pd + r.brevet_aug_pd + r.fond_aug_pd + r.autre_incorp_aug_pd)
            r.immoi_aug_pd = total

    def _get_immoi_aug_vir(self):

        for r in self:
            total = (r.immord_aug_vir + r.brevet_aug_vir + r.fond_aug_vir + r.autre_incorp_aug_vir)
            r.immoi_aug_vir = total

    def _get_immoi_dim_cess(self):
        res = {}
        total = 0
        for r in self:
            total = (r.immord_dim_cess + r.brevet_dim_cess + r.fond_dim_cess + r.autre_incorp_dim_cess)
            r.immoi_dim_cess = total

    def _get_immoi_dim_ret(self):
        res = {}
        total = 0
        for r in self:
            total = (r.immord_dim_ret + r.brevet_dim_ret + r.fond_dim_ret + r.autre_incorp_dim_ret)
            r.immoi_dim_ret = total

    def _get_immoi_dim_vir(self):

        for r in self:
            total = (r.immord_dim_vir + r.brevet_dim_vir + r.fond_dim_vir + r.autre_incorp_dim_vir)
            r.immoi_dim_vir = total

    def _get_immoi_mbf(self):

        for r in self:
            total = (r.immord_mbf + r.brevet_mbf + r.fond_mbf + r.autre_incorp_mbf)
            r.immoi_mbf = total

    def _get_immoc_mbi(self):

        for r in self:
            total = (r.terrain_mb + r.constructions_mb + r.inst_mb + r.mat_mb + r.mob_mb + r.autre_corp_mb
                     + r.immocc_mb + r.mati_mb)
            r.immonc_mb = total

    def _get_immoc_aug_acq(self):
        res = {}
        total = 0
        for r in self:
            total = (r.terrain_aug_acq + r.constructions_aug_acq + r.inst_aug_acq + r.mat_aug_acq +
                     r.mob_aug_acq + r.autre_corp_aug_acq + r.immocc_aug_acq + r.mati_aug_acq)
            r.immonc_aug_acq = total

    def _get_immoc_aug_pd(self):

        for r in self:
            total = (r.terrain_aug_pd + r.constructions_aug_pd + r.inst_aug_pd + r.mat_aug_pd + r.mob_aug_pd +
                     r.autre_corp_aug_pd + r.immocc_aug_pd + r.mati_aug_pd)
            r.immonc_aug_pd = total

    def _get_immoc_aug_vir(self):

        for r in self:
            total = (r.terrain_aug_vir + r.constructions_aug_vir + r.inst_aug_vir + r.mat_aug_vir + r.mob_aug_vir +
                     r.autre_corp_aug_vir + r.immocc_aug_vir + r.mati_aug_vir)
            r.immonc_aug_vir = total

    def _get_immoc_dim_cess(self):
        res = {}
        total = 0
        for r in self:
            total = (r.terrain_dim_cess + r.constructions_dim_cess + r.inst_dim_cess + r.mat_dim_cess + r.mob_dim_cess +
                     r.autre_corp_dim_cess + r.immocc_dim_cess + r.mati_dim_cess)
            r.immonc_dim_cess = total

    def _get_immoc_dim_ret(self):

        for r in self:
            total = (r.terrain_dim_ret + r.constructions_dim_ret + r.inst_dim_ret + r.mat_dim_ret + r.mob_dim_ret +
                     r.autre_corp_dim_ret + r.immocc_dim_ret + r.mati_dim_ret)
            r.immonc_dim_ret = total

    def _get_immoc_dim_vir(self):

        for r in self:
            total = (r.terrain_dim_vir + r.constructions_dim_vir + r.inst_dim_vir + r.mat_dim_vir + r.mob_dim_vir +
                     r.autre_corp_dim_vir + r.immocc_dim_vir + r.mati_dim_vir)
            r.immonc_dim_vir = total

    def _get_immoc_mbf(self):

        for r in self:
            total = (r.terrain_mbf + r.constructions_mbf + r.inst_mbf + r.mat_mbf + r.mob_mbf +
                     r.autre_corp_mbf + r.immocc_mbf + r.mati_mbf)
            r.immonc_mbf = total

    def _get_fp_mbf(self):

        for r in self:
            total = (r.fp_mb + r.fp_aug_acq + r.fp_aug_pd + r.fp_aug_vir - r.fp_dim_cess -
                     r.fp_dim_ret - r.fp_dim_vir)
            r.fp_mbf = total

    def _get_charge_mbf(self):
        for r in self:
            total = (r.charge_mb + r.charge_aug_acq + r.charge_aug_pd + r.charge_aug_vir - r.charge_dim_cess -
                     r.charge_dim_ret - r.charge_dim_vir)
            r.charge_mbf = total

    def _get_prime_mbf(self):

        for r in self:
            total = (r.prime_mb + r.prime_aug_acq + r.prime_aug_pd + r.prime_aug_vir - r.prime_dim_cess -
                     r.prime_dim_ret - r.prime_dim_vir)
            r.prime_mbf = total

    def _get_immord_mbf(self):
        res = {}
        total = 0
        for r in self:
            total = (r.immord_mb + r.immord_aug_acq + r.immord_aug_pd + r.immord_aug_vir - r.immord_dim_cess -
                     r.immord_dim_ret - r.immord_dim_vir)
            r.immord_mbf = total

    def _get_brevet_mbf(self):
        res = {}
        total = 0
        for r in self:
            total = (r.brevet_mb + r.brevet_aug_acq + r.brevet_aug_pd + r.brevet_aug_vir - r.brevet_dim_cess -
                     r.brevet_dim_ret - r.brevet_dim_vir)
            r.brevet_mbf = total

    def _get_fond_mbf(self):
        res = {}
        total = 0
        for r in self:
            total = (r.fond_mb + r.fond_aug_acq + r.fond_aug_pd + r.fond_aug_vir - r.fond_dim_cess -
                     r.fond_dim_ret - r.fond_dim_vir)
            r.fond_mbf = total

    def _get_autre_incorp_mbf(self):
        res = {}
        total = 0
        for r in self:
            total = (
                    r.autre_incorp_mb + r.autre_incorp_aug_acq + r.autre_incorp_aug_pd + r.autre_incorp_aug_vir - r.autre_incorp_dim_cess -
                    r.autre_incorp_dim_ret - r.autre_incorp_dim_vir)
            r.autre_incorp_mbf = total

    def _get_terrain_mbf(self):

        for r in self:
            total = (r.terrain_mb + r.terrain_aug_acq + r.terrain_aug_pd + r.terrain_aug_vir - r.terrain_dim_cess -
                     r.terrain_dim_ret - r.terrain_dim_vir)
            r.terrain_mbf = total

    def _get_constructions_mbf(self):
        res = {}
        total = 0
        for r in self:
            total = (
                    r.constructions_mb + r.constructions_aug_acq + r.constructions_aug_pd + r.constructions_aug_vir - r.constructions_dim_cess -
                    r.constructions_dim_ret - r.constructions_dim_vir)
            r.constructions_mbf = total

    def _get_inst_mbf(self):

        for r in self:
            total = (r.inst_mb + r.inst_aug_acq + r.inst_aug_pd + r.inst_aug_vir - r.inst_dim_cess -
                     r.inst_dim_ret - r.inst_dim_vir)
            r.inst_mbf = total

    def _get_mat_mbf(self):
        res = {}
        total = 0
        for r in self:
            total = (r.mat_mb + r.mat_aug_acq + r.mat_aug_pd + r.mat_aug_vir - r.mat_dim_cess -
                     r.mat_dim_ret - r.mat_dim_vir)
            r.mat_mbf = total

    def _get_mob_mbf(self):
        res = {}
        total = 0
        for r in self:
            total = (r.mob_mb + r.mob_aug_acq + r.mob_aug_pd + r.mob_aug_vir - r.mob_dim_cess -
                     r.mob_dim_ret - r.mob_dim_vir)
            r.mob_mbf = total

    def _get_autre_corp_mbf(self):
        res = {}
        total = 0
        for r in self:
            total = (
                    r.autre_corp_mb + r.autre_corp_aug_acq + r.autre_corp_aug_pd + r.autre_corp_aug_vir - r.autre_corp_dim_cess -
                    r.autre_corp_dim_ret - r.autre_corp_dim_vir)
            r.autre_corp_mbf = total

    def _get_immocc_mbf(self):
        res = {}
        total = 0
        for r in self:
            total = (r.immocc_mb + r.immocc_aug_acq + r.immocc_aug_pd + r.immocc_aug_vir - r.immocc_dim_cess -
                     r.immocc_dim_ret - r.immocc_dim_vir)
            r.immocc_mbf = total

    def _get_mati_mbf(self):
        res = {}
        total = 0
        for r in self:
            total = (r.mati_mb + r.mati_aug_acq + r.mati_aug_pd + r.mati_aug_vir - r.mati_dim_cess -
                     r.mati_dim_ret - r.mati_dim_vir)
            r.mati_mbf = total

    def _get_tva_recsd(self):
        res = {}
        total = 0
        for r in self:
            total = (r.tva_charsd + r.tva_immosd)
            r.tva_recsd = total

    def _get_tva_reco(self):
        res = {}
        total = 0
        for r in self:
            total = (r.tva_charo + r.tva_immoo)
            r.tva_reco = total

    def _get_tva_recd(self):
        res = {}
        total = 0
        for r in self:
            total = (r.tva_chard + r.tva_immod)
            r.tva_recd = total

    def _get_tva_recsf(self):
        res = {}
        total = 0
        for r in self:
            total = (r.tva_charsf + r.tva_immosf)
            r.tva_recsf = total

    def _get_totalsd(self):
        res = {}
        total = 0
        for r in self:
            total = (r.tva_facsd - r.tva_recsd)
            r.tva_totalsd = total

    def _get_totald(self):
        res = {}
        total = 0
        for r in self:
            total = (r.tva_facd - r.tva_recd)
            r.tva_totald = total

    def _get_totalo(self):
        res = {}
        total = 0
        for r in self:
            total = (r.tva_faco - r.tva_reco)
            r.tva_totalo = total

    def _get_totalsf(self):

        for r in self:
            total = (r.tva_facsf - r.tva_recsf)
            r.tva_totalsf = total

    date_start = fields.Date('Date d\'ouverture', required=True)
    date_end = fields.Date('Date de cloture', required=True)
    output2 = fields.Binary('Data XML', readonly=True)
    actif = fields.One2many('bilan.actif.fiscale.erp', 'balance_id', 'Actif')
    passif = fields.One2many('bilan.passif.fiscale.erp', 'balance_id', 'Passif')
    cpc = fields.One2many('cpc.fiscale.erp', 'balance_id', 'CPC')
    det_cpc = fields.One2many('det.cpc.fiscale.erp', 'balance_id', 'Det CPC')
    tfr = fields.One2many('tfr.fiscale.erp', 'balance_id', 'TFR')
    caf = fields.One2many('caf.fiscale.erp', 'balance_id', 'CAF')
    amort = fields.One2many('amort.fiscale.erp', 'balance_id', 'Amort')
    provision = fields.One2many('provision.fiscale.erp', 'balance_id', 'Prov')
    stock = fields.One2many('stock.fiscale.erp', 'balance_id', 'Stock')
    fusion = fields.One2many('fusion.fiscale.erp', 'balance_id', 'Fusion')
    exercice_prec = fields.Many2one('liasse.balance.erp', 'Exercice precedent')
    output = fields.Binary('Declaration EDI', readonly=True)
    output_name = fields.Char('File name', default='edi.xml')
    date_cloture = fields.Date('Date', required=True, default=fields.Date.context_today)
    name = fields.Many2one("date.range", string="Exercice", required=True, domain=[('kzm_is_fiscalyear', '=', True)])
    file_data = fields.Binary('Fichier CSV')
    file_name = fields.Char('File name')
    balance_line = fields.One2many('liasse.balance.line', 'balance_id', 'Balance Generale')
    credit_bail = fields.One2many('credi.bail.erp', 'balance_id', 'Credit Bail')
    pm_value = fields.One2many('pm.value.erp', 'balance_id', '+- Valeur ')
    dotation_amort = fields.One2many('dotation.amort.erp', 'balance_id', 'Dotation')
    titre_particip = fields.One2many('titre.particip.erp', 'balance_id', 'Titre Participation ')
    repart_cs = fields.One2many('repart.cs.erp', 'balance_id', 'ETAT DE REPARTITION DU CAPITAL SOCIAL ')
    interets_associe = fields.One2many('interets.erp', 'balance_id', 'Interets Associe ', domain=[('type', '=', '0')],
                                       context={'default_type': '0'})
    interets_tier = fields.One2many('interets.erp', 'balance_id', 'Interets tiers ', domain=[('type', '=', '1')],
                                    context={'default_type': '1'})
    beaux = fields.One2many('beaux.erp', 'balance_id', 'BEAUX ')
    extra_tab = fields.Boolean('Afficher la liasse')
    bal_view = fields.Boolean('Afficher la balance')
    fiche = fields.Many2one('liasse.fiche.signalitique.erp', u'Fiche signalitique', required=True)
    passages_rfc = fields.One2many('passage.erp', 'balance_id', 'Reintegrations fiscales courantes',
                                   domain=[('type', '=', '0')], context={'default_type': '0'})
    passages_rfnc = fields.One2many('passage.erp', 'balance_id', 'Reintegrations fiscales non courantes',
                                    domain=[('type', '=', '1')], context={'default_type': '1'})
    passages_dfc = fields.One2many('passage.erp', 'balance_id', 'Déductions fiscales courantes',
                                   domain=[('type', '=', '2')], context={'default_type': '2'})
    passages_dfnc = fields.One2many('passage.erp', 'balance_id', 'Déductions fiscales non courantes',
                                    domain=[('type', '=', '3')], context={'default_type': '3'})
    # pm total
    pm_compte_princ = fields.Float(compute=_get_pm_cp, string='Compte principal')
    pm_montant_brut = fields.Float(compute=_get_pm_mb, string='Montant brut')
    pm_amort_cumul = fields.Float(compute=_get_pm_ac, string='Amortissements cumulés')
    pm_val_net_amort = fields.Float(compute=_get_pm_vna, string='Valeur nette d\'amortissements')
    pm_prod_cess = fields.Float(compute=_get_pm_pc, string='Produit de cession')
    pm_plus_value = fields.Float(compute=_get_pm_pv, string='Plus values')
    pm_moins_value = fields.Float(compute=_get_pm_mv, string='Moins values')

    # titre_particip
    tp_sect_activity = fields.Char('Secteur d\'activité')
    tp_capit_social = fields.Float(compute=_get_tp_cp, string='Capital social')
    tp_particip_cap = fields.Float(compute=_get_tp_pc, string='Participation au capital %')
    tp_prix_global = fields.Float(compute=_get_tp_pg, string='Prix d\'acquisition global')
    tp_val_compt = fields.Float(compute=_get_tp_vc, string='Valeur comptable nette')
    tp_extr_date = fields.Date('Extrait(Date de clôture)')
    tp_extr_situation = fields.Float(compute=_get_tp_es, string='Extrait(Situation nette)')
    tp_extr_resultat = fields.Float(compute=_get_tp_er, string='Extrait(résultat net)')
    tp_prod_inscrit = fields.Float(compute=_get_tp_pi, string='Produits inscrits au C.P.C de l\'exercice')
    # repartition du cs
    montant_rcs = fields.Float('Montant du capital')
    # interets
    in_mont_pretl = fields.Float(compute=_get_in_mt, string='Montant du prêt')
    in_charge_global = fields.Float(compute=_get_in_cg, string='Charge financière globale')
    in_remb_princ = fields.Float(compute=_get_in_rp, string='Remboursement exercices antérieurs(Principal)')
    in_remb_inter = fields.Float(compute=_get_in_ri, string='Remboursement exercices antérieurs(Intérêt)')
    in_remb_actual_princ = fields.Float(compute=_get_in_rap, string='Remboursement exercice actuel(Principal)')
    in_remb_actual_inter = fields.Float(compute=_get_in_rai, string='Remboursement exercice actuel(Intérêt)')
    # beaux
    bx_mont_pretl = fields.Float(compute=_get_bx_ml, string='Montant annuel de location')
    bx_charge_global = fields.Float(compute=_get_bx_mc,
                                    string='Montant du loyer compris dans les charges de l\'exercice')
    # passage
    p_benifice_p = fields.Float('Bénéfice net (+)')
    p_benifice_m = fields.Float('Bénéfice net (-)')
    p_perte_p = fields.Float('Perte nette (+)')
    p_perte_m = fields.Float('Perte nette (-)')
    p_total_montantp = fields.Float(compute=_get_p_mp, string='Total mantant(+)')
    p_total_montantm = fields.Float(compute=_get_p_mm, string='Total mantant(-)')
    p_benificebp = fields.Float('Bénéfice brut si T1> T2 (+)')
    p_benificebm = fields.Float(compute=_get_p_bbf, string='Bénéfice brut si T1> T2 (-)')
    p_deficitfp = fields.Float('Déficit brut fiscal si T2> T1 (+)')
    p_deficitfm = fields.Float(compute=_get_p_dbf, string='Déficit brut fiscal si T2> T1 (-)')
    p_exo4p = fields.Float('Exercice n-4 (+)')
    # 'p_exo4m = fields.Float('Exercice n-4 (-)'),
    p_exo3p = fields.Float('Exercice n-3 (+)')
    # 'p_exo3m = fields.Float('Exercice n-3 (-)'),
    p_exo2p = fields.Float('Exercice n-2 (+)')
    # 'p_exo2m = fields.Float('Exercice n-2 (-)'),
    p_exo1p = fields.Float('Exercice n-1 (+)')
    # 'p_exo1m = fields.Float('Exercice n-1 (-)'),
    p_benificenfp = fields.Float(u'Bénéfice net fiscal(+)')
    p_benificenfm = fields.Float(u'Bénéfice net fiscal(-)')
    p_deficitnfp = fields.Float(u'déficit net fiscal(+)')
    p_deficitnfm = fields.Float(compute=_get_p_dnf, string=u'déficit net fiscal(-)')
    p_cumulafdm = fields.Float(u'CUMUL DES AMORTISSEMENTS FISCALEMENT DIFFERES(-)')
    p_exo4cumulp = fields.Float('Exercice n-4 (+)')
    p_exo3cumulp = fields.Float('Exercice n-3 (+)')
    p_exo2cumulp = fields.Float('Exercice n-2 (+)')
    p_exo1cumulp = fields.Float('Exercice n-1 (+)')
    # affect
    aff_rep_n = fields.Float(u'Report à nouveau')
    aff_res_n_in = fields.Float(u'Résultats nets en instance d\'affectation ')
    aff_res_n_ex = fields.Float(u'Résultat net de l\'exercice')
    aff_prev = fields.Float(u'Prélèvements sur les réserves')
    # aff_autre_prev = fields.Float()
    aff_autre_prev = fields.Float(u'Autres prélèvements')
    aff_totala = fields.Float(compute=_get_aff_ta, string='Total A')

    aff_rl = fields.Float(u'Réserve légale')
    aff_autre_r = fields.Float(u'Autres réserves')
    aff_tant = fields.Float(u'Tantièmes')
    aff_div = fields.Float(u'Dividendes')
    aff_autre_aff = fields.Float(u'Autres affectations')
    aff_rep_n2 = fields.Float(u'Report à nouveau ')
    aff_totalb = fields.Float(compute=_get_aff_tb, string='Total B')

    # encouragement
    vente_imp_ep = fields.Float('Vente imposable', help="Ensemble des produits")
    vente_imp_epi = fields.Float('Vente imposable', help="Ensemble des produits correspondant à la base imposable")
    vente_imp_ept = fields.Float('Vente imposable', help="Ensemble des produits correspondant au numérateur taxable")
    vente_ex100_ep = fields.Float('Ventes exonérées à 100% ', help="Ensemble des produits")
    vente_ex100_epi = fields.Float('Ventes exonérées à 100% ',
                                   help="Ensemble des produits correspondant à la base imposable")
    vente_ex100_ept = fields.Float('Ventes exonérées à 100% ',
                                   help="Ensemble des produits correspondant au numérateur taxable")
    vente_ex50_ep = fields.Float('Ventes exonérées à 50% ', help="Ensemble des produits")
    vente_ex50_epi = fields.Float('Ventes exonérées à 50% ',
                                  help="Ensemble des produits correspondant à la base imposable")
    vente_ex50_ept = fields.Float('Ventes exonérées à 50% ',
                                  help="Ensemble des produits correspondant au numérateur taxable")

    vente_li_ep = fields.Float('Ventes et locations imposables', help="Ensemble des produits")
    vente_li_epi = fields.Float('Ventes et locations imposables',
                                help="Ensemble des produits correspondant à la base imposable")
    vente_li_ept = fields.Float('Ventes et locations imposables',
                                help="Ensemble des produits correspondant au numérateur taxable")
    vente_lex100_ep = fields.Float('Ventes et locations exclues à 100% ', help="Ensemble des produits")
    vente_lex100_epi = fields.Float('Ventes et locations exclues à 100%  ',
                                    help="Ensemble des produits correspondant à la base imposable")
    vente_lex100_ept = fields.Float('Ventes et locations exclues à 100%  ',
                                    help="Ensemble des produits correspondant au numérateur taxable")
    vente_lex50_ep = fields.Float('Ventes et locations exclues à 50%  ', help="Ensemble des produits")
    vente_lex50_epi = fields.Float('Ventes et locations exclues à 50%  ',
                                   help="Ensemble des produits correspondant à la base imposable")
    vente_lex50_ept = fields.Float('Ventes et locations exclues à 50% ',
                                   help="Ensemble des produits correspondant au numérateur taxable")

    pres_imp_ep = fields.Float('Imposables', help="Ensemble des produits")
    pres_imp_epi = fields.Float('Imposables', help="Ensemble des produits correspondant à la base imposable")
    pres_imp_ept = fields.Float('Imposables', help="Ensemble des produits correspondant au numérateur taxable")
    pres_ex100_ep = fields.Float('Exonérées à 100% ', help="Ensemble des produits")
    pres_ex100_epi = fields.Float('Exonérées à 100% ', help="Ensemble des produits correspondant à la base imposable")
    pres_ex100_ept = fields.Float('Exonérées à 100% ',
                                  help="Ensemble des produits correspondant au numérateur taxable")
    pres_ex50_ep = fields.Float('Exonérées à 50% ', help="Ensemble des produits")
    pres_ex50_epi = fields.Float('Exonérées à 50% ', help="Ensemble des produits correspondant à la base imposable")
    pres_ex50_ept = fields.Float('Exonérées à 50% ', help="Ensemble des produits correspondant au numérateur taxable")

    prod_acc_ep = fields.Float(u'Produits accessoires. Produits financiers, dons et libéralités',
                               help="Ensemble des produits")
    prod_acc_epi = fields.Float(u'Produits accessoires. Produits financiers, dons et libéralités ',
                                help="Ensemble des produits correspondant à la base imposable")
    prod_acc_ept = fields.Float(u'Produits accessoires. Produits financiers, dons et libéralités ',
                                help="Ensemble des produits correspondant au numérateur taxable")
    prod_sub_ep = fields.Float('Subventions d\'équipement', help="Ensemble des produits")
    prod_sub_epi = fields.Float('Subventions d\'équipement ',
                                help="Ensemble des produits correspondant à la base imposable")
    prod_sub_ept = fields.Float('Subventions d\'équipement ',
                                help="Ensemble des produits correspondant au numérateur taxable")

    sub_eq_ep = fields.Float(u'Subventions d\'équilibre', help="Ensemble des produits")
    sub_eq_epi = fields.Float(u'Subventions d\'équilibre ',
                              help="Ensemble des produits correspondant à la base imposable")
    sub_eq_ept = fields.Float(u'Subventions d\'équilibre',
                              help="Ensemble des produits correspondant au numérateur taxable")
    sub_imp_ep = fields.Float('Imposables', help="Ensemble des produits")
    sub_imp_epi = fields.Float('Imposables', help="Ensemble des produits correspondant à la base imposable")
    sub_imp_ept = fields.Float('Imposables', help="Ensemble des produits correspondant au numérateur taxable")
    sub_ex100_ep = fields.Float(u'Exonérées à 100%', help="Ensemble des produits")
    sub_ex100_epi = fields.Float(u'Exonérées à 100%', help="Ensemble des produits correspondant à la base imposable")
    sub_ex100_ept = fields.Float(u'Exonérées à 100%', help="Ensemble des produits correspondant au numérateur taxable")
    sub_ex50_ep = fields.Float(u'Exonérées à 50%', help="Ensemble des produits")
    sub_ex50_epi = fields.Float(u'Exonérées à 50%', help="Ensemble des produits correspondant à la base imposable")
    sub_ex50_ept = fields.Float(u'Exonérées à 50%', help="Ensemble des produits correspondant au numérateur taxable")

    taux_part_ep = fields.Float(compute=_get_encp_ep, string='partiels', help="Ensemble des produits")
    taux_part_epi = fields.Float(compute=_get_encp_epi, string='Totaux partiels',
                                 help="Ensemble des produits correspondant à la base imposable")
    taux_part_ept = fields.Float(compute=_get_encp_ept, string='Totaux partiels',
                                 help="Ensemble des produits correspondant au numérateur taxable")

    profit_g_ep = fields.Float(u'Profit net global des cessions après abattement pondéré',
                               help="Ensemble des produits")
    profit_g_epi = fields.Float(u'Profit net global des cessions après abattement pondéré',
                                help="Ensemble des produits correspondant à la base imposable")
    profit_g_ept = fields.Float(u'Profit net global des cessions après abattement pondéré',
                                help="Ensemble des produits correspondant au numérateur taxable")
    profit_ex_ep = fields.Float(u'Autres profils exceptionnels', help="Ensemble des produits")
    profit_ex_epi = fields.Float(u'Autres profils exceptionnels',
                                 help="Ensemble des produits correspondant à la base imposable")
    profit_ex_ept = fields.Float(u'Autres profils exceptionnels',
                                 help="Ensemble des produits correspondant au numérateur taxable")

    total_g_ep = fields.Float(compute=_get_encg_ep, string='Total général', help="Ensemble des produits")
    total_g_epi = fields.Float(compute=_get_encg_epi, string='Total général',
                               help="Ensemble des produits correspondant à la base imposable")
    total_g_ept = fields.Float(compute=_get_encg_ept, string='Total général',
                               help="Ensemble des produits correspondant au numérateur taxable")

    # immo
    immonv_mb = fields.Float(compute=_get_immonv_mbi, string='IMMOBILISATION EN NON-VALEURS',
                             help="Montant brut debut exercice")
    immonv_aug_acq = fields.Float(compute=_get_immonv_aug_acq, string='Immo non valeurs',
                                  help="Augmentation: acquisition")
    immonv_aug_pd = fields.Float(compute=_get_immonv_aug_pd, string='Immo non valeurs',
                                 help="Augmentation: Production par l'entreprise pour elle-même")
    immonv_aug_vir = fields.Float(compute=_get_immonv_aug_vir, string='Immo non valeurs',
                                  help="Augmentation: Virement")
    immonv_dim_cess = fields.Float(compute=_get_immonv_dim_cess, string='Immo non valeurs',
                                   help="Diminution: cession")
    immonv_dim_ret = fields.Float(compute=_get_immonv_dim_ret, string='Immo non valeurs',
                                  help="Diminution: retrait")
    immonv_dim_vir = fields.Float(compute=_get_immonv_dim_vir, string='Immo non valeurs',
                                  help="Diminution: virement")
    immonv_mbf = fields.Float(compute=_get_immonv_mbf, string='Immo non valeurs',
                              help="Montant brut fin exercice")

    fp_mb = fields.Float('Frais preliminaires', help="Montant brut debut exercice")
    fp_aug_acq = fields.Float('Frais preliminaires', help="Augmentation: acquisition")
    fp_aug_pd = fields.Float('Frais preliminaires', help="Augmentation: Production par l'entreprise pour elle-même")
    fp_aug_vir = fields.Float('Frais preliminaires', help="Augmentation: Virement")
    fp_dim_cess = fields.Float('Frais preliminaires', help="Diminution: cession")
    fp_dim_ret = fields.Float('Frais preliminaires', help="Diminution: retrait")
    fp_dim_vir = fields.Float('Frais preliminaires', help="Diminution: virement")
    fp_mbf = fields.Float(compute=_get_fp_mbf, string='Frais preliminaires', help="Montant brut fin exercice")

    charge_mb = fields.Float('Charges a repartir sur plusieurs exercices', help="Montant brut debut exercice")
    charge_aug_acq = fields.Float('Charges a repartir sur plusieurs exercices', help="Augmentation: acquisition")
    charge_aug_pd = fields.Float('Charges a repartir sur plusieurs exercices',
                                 help="Augmentation: Production par l'entreprise pour elle-même")
    charge_aug_vir = fields.Float('Charges a repartir sur plusieurs exercices', help="Augmentation: Virement")
    charge_dim_cess = fields.Float('Charges a repartir sur plusieurs exercices', help="Diminution: cession")
    charge_dim_ret = fields.Float('Charges a repartir sur plusieurs exercices', help="Diminution: retrait")
    charge_dim_vir = fields.Float('Charges a repartir sur plusieurs exercices', help="Diminution: virement")
    charge_mbf = fields.Float(compute=_get_charge_mbf, string='Charges a repartir sur plusieurs exercices',
                              help="Montant brut fin exercice")

    prime_mb = fields.Float('Primes de remboursement obligations', help="Montant brut debut exercice")
    prime_aug_acq = fields.Float('Primes de remboursement obligations', help="Augmentation: acquisition")
    prime_aug_pd = fields.Float('Primes de remboursement obligations',
                                help="Augmentation: Production par l'entreprise pour elle-même")
    prime_aug_vir = fields.Float('Primes de remboursement obligations', help="Augmentation: Virement")
    prime_dim_cess = fields.Float('Primes de remboursement obligations', help="Diminution: cession")
    prime_dim_ret = fields.Float('Primes de remboursement obligations', help="Diminution: retrait")
    prime_dim_vir = fields.Float('Primes de remboursement obligations', help="Diminution: virement")
    prime_mbf = fields.Float(compute=_get_prime_mbf, string='Primes de remboursement obligations', type="float",
                             help="Montant brut fin exercice")

    immoi_mb = fields.Float(compute=_get_immoi_mbi, string='IMMOBILISATIONS INCORPORELLES',
                            help="Montant brut debut exercice")
    immoi_aug_acq = fields.Float(compute=_get_immoi_aug_acq, string='IMMOBILISATIONS INCORPORELLES',
                                 help="Augmentation: acquisition")
    immoi_aug_pd = fields.Float(compute=_get_immoi_aug_pd, string='IMMOBILISATIONS INCORPORELLES',
                                help="Augmentation: Production par l'entreprise pour elle-même")
    immoi_aug_vir = fields.Float(compute=_get_immoi_aug_vir, string='IMMOBILISATIONS INCORPORELLES',
                                 help="Augmentation: Virement")
    immoi_dim_cess = fields.Float(compute=_get_immoi_dim_cess, string='IMMOBILISATIONS INCORPORELLES',
                                  help="Diminution: cession")
    immoi_dim_ret = fields.Float(compute=_get_immoi_dim_ret, string='IMMOBILISATIONS INCORPORELLES',
                                 help="Diminution: retrait")
    immoi_dim_vir = fields.Float(compute=_get_immoi_dim_vir, string='IMMOBILISATIONS INCORPORELLES',
                                 help="Diminution: virement")
    immoi_mbf = fields.Float(compute=_get_immoi_mbf, string='IMMOBILISATIONS INCORPORELLES',
                             help="Montant brut fin exercice")

    immord_mb = fields.Float('Immobilisation en recherche et developpement', help="Montant brut debut exercice")
    immord_aug_acq = fields.Float('Immobilisation en recherche et developpement', help="Augmentation: acquisition")
    immord_aug_pd = fields.Float('Immobilisation en recherche et developpement',
                                 help="Augmentation: Production par l'entreprise pour elle-même")
    immord_aug_vir = fields.Float('Immobilisation en recherche et developpement', help="Augmentation: Virement")
    immord_dim_cess = fields.Float('Immobilisation en recherche et developpement', help="Diminution: cession")
    immord_dim_ret = fields.Float('Immobilisation en recherche et developpement', help="Diminution: retrait")
    immord_dim_vir = fields.Float('Immobilisation en recherche et developpement', help="Diminution: virement")
    immord_mbf = fields.Float(compute=_get_immord_mbf, string='Immobilisation en recherche et developpement',
                              help="Montant brut fin exercice")

    brevet_mb = fields.Float('Brevets, marques, droits et valeurs similaires', help="Montant brut debut exercice")
    brevet_aug_acq = fields.Float('Brevets, marques, droits et valeurs similaires', help="Augmentation: acquisition")
    brevet_aug_pd = fields.Float('Brevets, marques, droits et valeurs similaires',
                                 help="Augmentation: Production par l'entreprise pour elle-même")
    brevet_aug_vir = fields.Float('Brevets, marques, droits et valeurs similaires', help="Augmentation: Virement")
    brevet_dim_cess = fields.Float('Brevets, marques, droits et valeurs similaires', help="Diminution: cession")
    brevet_dim_ret = fields.Float('Brevets, marques, droits et valeurs similaires', help="Diminution: retrait")
    brevet_dim_vir = fields.Float('Brevets, marques, droits et valeurs similaires', help="Diminution: virement")
    brevet_mbf = fields.Float(compute=_get_brevet_mbf, string='Brevets, marques, droits et valeurs similaires',
                              help="Montant brut fin exercice")

    fond_mb = fields.Float('Fonds commercial', help="Montant brut debut exercice")
    fond_aug_acq = fields.Float('Fonds commercial', help="Augmentation: acquisition")
    fond_aug_pd = fields.Float('Fonds commercial', help="Augmentation: Production par l'entreprise pour elle-même")
    fond_aug_vir = fields.Float('Fonds commercial', help="Augmentation: Virement")
    fond_dim_cess = fields.Float('Fonds commercial', help="Diminution: cession")
    fond_dim_ret = fields.Float('Fonds commercial', help="Diminution: retrait")
    fond_dim_vir = fields.Float('Fonds commercial', help="Diminution: virement")
    fond_mbf = fields.Float(compute=_get_fond_mbf, string='Fonds commercial',
                            help="Montant brut fin exercice")

    autre_incorp_mb = fields.Float('Autres immobilisations incorporelles', help="Montant brut debut exercice")
    autre_incorp_aug_acq = fields.Float('Autres immobilisations incorporelles', help="Augmentation: acquisition")
    autre_incorp_aug_pd = fields.Float('Autres immobilisations incorporelles',
                                       help="Augmentation: Production par l'entreprise pour elle-même")
    autre_incorp_aug_vir = fields.Float('Autres immobilisations incorporelles', help="Augmentation: Virement")
    autre_incorp_dim_cess = fields.Float('Autres immobilisations incorporelles', help="Diminution: cession")
    autre_incorp_dim_ret = fields.Float('Autres immobilisations incorporelles', help="Diminution: retrait")
    autre_incorp_dim_vir = fields.Float('Autres immobilisations incorporelles', help="Diminution: virement")
    autre_incorp_mbf = fields.Float(compute=_get_autre_incorp_mbf, string='Autres immobilisations incorporelles',
                                    help="Montant brut fin exercice")

    immonc_mb = fields.Float(compute=_get_immoc_mbi, string='IMMOBILISATIONS CORPORELLES', type="float",
                             help="Montant brut debut exercice")
    immonc_aug_acq = fields.Float(compute=_get_immoc_aug_acq, string='IMMOBILISATIONS CORPORELLES', type="float",
                                  help="Augmentation: acquisition")
    immonc_aug_pd = fields.Float(compute=_get_immoc_aug_pd, string='IMMOBILISATIONS CORPORELLES', type="float",
                                 help="Augmentation: Production par l'entreprise pour elle-même")
    immonc_aug_vir = fields.Float(compute=_get_immoc_aug_vir, string='IMMOBILISATIONS CORPORELLES', type="float",
                                  help="Augmentation: Virement")
    immonc_dim_cess = fields.Float(compute=_get_immoc_dim_cess, string='IMMOBILISATIONS CORPORELLES', type="float",
                                   help="Diminution: cession")
    immonc_dim_ret = fields.Float(compute=_get_immoc_dim_ret, string='IMMOBILISATIONS CORPORELLES', type="float",
                                  help="Diminution: retrait")
    immonc_dim_vir = fields.Float(compute=_get_immoc_dim_vir, string='IMMOBILISATIONS CORPORELLES', type="float",
                                  help="Diminution: virement")
    immonc_mbf = fields.Float(compute=_get_immoc_mbf, string='IMMOBILISATIONS CORPORELLES',
                              help="Montant brut fin exercice")

    terrain_mb = fields.Float('Terrains', help="Montant brut debut exercice")
    terrain_aug_acq = fields.Float('Terrains', help="Augmentation: acquisition")
    terrain_aug_pd = fields.Float('Terrains', help="Augmentation: Production par l'entreprise pour elle-même")
    terrain_aug_vir = fields.Float('Terrains', help="Augmentation: Virement")
    terrain_dim_cess = fields.Float('Terrains', help="Diminution: cession")
    terrain_dim_ret = fields.Float('Terrains', help="Diminution: retrait")
    terrain_dim_vir = fields.Float('Terrains', help="Diminution: virement")
    terrain_mbf = fields.Float(compute=_get_terrain_mbf, string='Terrains', help="Montant brut fin exercice")

    constructions_mb = fields.Float('Constructions', help="Montant brut debut exercice")
    constructions_aug_acq = fields.Float('Constructions', help="Augmentation: acquisition")
    constructions_aug_pd = fields.Float('Constructions',
                                        help="Augmentation: Production par l'entreprise pour elle-même")
    constructions_aug_vir = fields.Float('Constructions', help="Augmentation: Virement")
    constructions_dim_cess = fields.Float('Constructions', help="Diminution: cession")
    constructions_dim_ret = fields.Float('Constructions', help="Diminution: retrait")
    constructions_dim_vir = fields.Float('Constructions', help="Diminution: virement")
    constructions_mbf = fields.Float(compute=_get_constructions_mbf, string='Constructionsins',
                                     help="Montant brut fin exercice")

    inst_mb = fields.Float('Installat. techniques,materiel et outillage', help="Montant brut debut exercice")
    inst_aug_acq = fields.Float('Installat. techniques,materiel et outillage', help="Augmentation: acquisition")
    inst_aug_pd = fields.Float('Installat. techniques,materiel et outillage',
                               help="Augmentation: Production par l'entreprise pour elle-même")
    inst_aug_vir = fields.Float('Installat. techniques,materiel et outillage', help="Augmentation: Virement")
    inst_dim_cess = fields.Float('Installat. techniques,materiel et outillage', help="Diminution: cession")
    inst_dim_ret = fields.Float('Installat. techniques,materiel et outillage', help="Diminution: retrait")
    inst_dim_vir = fields.Float('Installat. techniques,materiel et outillage', help="Diminution: virement")
    inst_mbf = fields.Float(compute=_get_inst_mbf, string='Installat. techniques,materiel et outillage',
                            help="Montant brut fin exercice")

    mat_mb = fields.Float('Materiel de transport', help="Montant brut debut exercice")
    mat_aug_acq = fields.Float('Materiel de transport', help="Augmentation: acquisition")
    mat_aug_pd = fields.Float('Materiel de transport', help="Augmentation: Production par l'entreprise pour elle-même")
    mat_aug_vir = fields.Float('Materiel de transport', help="Augmentation: Virement")
    mat_dim_cess = fields.Float('Materiel de transport', help="Diminution: cession")
    mat_dim_ret = fields.Float('Materiel de transport', help="Diminution: retrait")
    mat_dim_vir = fields.Float('Materiel de transport', help="Diminution: virement")
    mat_mbf = fields.Float(compute=_get_mat_mbf, string='Materiel de transport',
                           help="Montant brut fin exercice")

    mob_mb = fields.Float('Mobilier, materiel bureau et amenagements', help="Montant brut debut exercice")
    mob_aug_acq = fields.Float('Mobilier, materiel bureau et amenagements', help="Augmentation: acquisition")
    mob_aug_pd = fields.Float('Mobilier, materiel bureau et amenagements',
                              help="Augmentation: Production par l'entreprise pour elle-même")
    mob_aug_vir = fields.Float('Mobilier, materiel bureau et amenagements', help="Augmentation: Virement")
    mob_dim_cess = fields.Float('Mobilier, materiel bureau et amenagements', help="Diminution: cession")
    mob_dim_ret = fields.Float('Mobilier, materiel bureau et amenagements', help="Diminution: retrait")
    mob_dim_vir = fields.Float('Mobilier, materiel bureau et amenagements', help="Diminution: virement")
    mob_mbf = fields.Float(compute=_get_mob_mbf, string='Mobilier, materiel bureau et amenagements',
                           help="Montant brut fin exercice")

    autre_corp_mb = fields.Float('Immobilisations corporelles diverses', help="Montant brut debut exercice")
    autre_corp_aug_acq = fields.Float('Immobilisations corporelles diverses', help="Augmentation: acquisition")
    autre_corp_aug_pd = fields.Float('Immobilisations corporelles diverses',
                                     help="Augmentation: Production par l'entreprise pour elle-même")
    autre_corp_aug_vir = fields.Float('Immobilisations corporelles diverses', help="Augmentation: Virement")
    autre_corp_dim_cess = fields.Float('Immobilisations corporelles diverses', help="Diminution: cession")
    autre_corp_dim_ret = fields.Float('Immobilisations corporelles diverses', help="Diminution: retrait")
    autre_corp_dim_vir = fields.Float('Immobilisations corporelles diverses', help="Diminution: virement")
    autre_corp_mbf = fields.Float(compute=_get_autre_corp_mbf, string='Immobilisations corporelles diverses',
                                  help="Montant brut fin exercice")

    immocc_mb = fields.Float('Immobilisations corporelles en cours', help="Montant brut debut exercice")
    immocc_aug_acq = fields.Float('Immobilisations corporelles en cours', help="Augmentation: acquisition")
    immocc_aug_pd = fields.Float('Immobilisations corporelles en cours',
                                 help="Augmentation: Production par l'entreprise pour elle-même")
    immocc_aug_vir = fields.Float('Immobilisations corporelles en cours', help="Augmentation: Virement")
    immocc_dim_cess = fields.Float('Immobilisations corporelles en cours', help="Diminution: cession")
    immocc_dim_ret = fields.Float('Immobilisations corporelles en cours', help="Diminution: retrait")
    immocc_dim_vir = fields.Float('Immobilisations corporelles en cours', help="Diminution: virement")
    immocc_mbf = fields.Float(compute=_get_immocc_mbf, string='Immobilisations corporelles en cours',
                              help="Montant brut fin exercice")

    mati_mb = fields.Float('Matériel informatique', help="Montant brut debut exercice")
    mati_aug_acq = fields.Float('Matériel informatique', help="Augmentation: acquisition")
    mati_aug_pd = fields.Float('Matériel informatique',
                               help="Augmentation: Production par l'entreprise pour elle-même")
    mati_aug_vir = fields.Float('Matériel informatique', help="Augmentation: Virement")
    mati_dim_cess = fields.Float('Matériel informatique', help="Diminution: cession")
    mati_dim_ret = fields.Float('Matériel informatique', help="Diminution: retrait")
    mati_dim_vir = fields.Float('Matériel informatique', help="Diminution: virement")
    mati_mbf = fields.Float(compute=_get_mati_mbf, string='Matériel informatique', help="Montant brut fin exercice")

    # dotation
    val_acq = fields.Float('Valeur a amortir (Prix d acquisition)')
    val_compt = fields.Float('Valeur a amortir - Valeur comptable apres reevaluation')
    amort_ant = fields.Float('Amortissements anterieurs')
    amort_ded_et = fields.Float('Amortissements deduits du Benefice brut de l exercice (Taux)')
    amort_ded_e = fields.Float(
        'Amortissements deduits du Benefice brut de l exercice Amortissements normaux ou acceleres de l exercice')
    amort_fe = fields.Float('Total des amortissements a la fin de l exercice')
    montant_dot = fields.Float('Montant global')

    # tva
    tva_facsd = fields.Float('tva', help="solde au début de l\'exercice")
    tva_faco = fields.Float('tva', help="Opérations comptables de l\'exercice")
    tva_facd = fields.Float('tva', help="Déclarations T.V.A de l\'exercice")
    tva_facsf = fields.Float('tva', help="Solde fin d\'exercice")

    tva_recsd = fields.Float(compute=_get_tva_recsd, string='tva', help="solde au début de l\'exercice")
    tva_reco = fields.Float(compute=_get_tva_reco, string='tva', help="Opérations comptables de l\'exercice")
    tva_recd = fields.Float(compute=_get_tva_recd, string='tva', help="Déclarations T.V.A de l\'exercice")
    tva_recsf = fields.Float(compute=_get_tva_recsf, string='tva', help="Solde fin d\'exercice")

    tva_charsd = fields.Float('tva', help="solde au début de l\'exercice")
    tva_charo = fields.Float('tva', help="Opérations comptables de l\'exercice")
    tva_chard = fields.Float('tva', help="Déclarations T.V.A de l\'exercice")
    tva_charsf = fields.Float('tva', help="Solde fin d\'exercice")

    tva_immosd = fields.Float('tva', help="solde au début de l\'exercice")
    tva_immoo = fields.Float('tva', help="Opérations comptables de l\'exercice")
    tva_immod = fields.Float('tva', help="Déclarations T.V.A de l\'exercice")
    tva_immosf = fields.Float('tva', help="Solde fin d\'exercice")

    tva_totalsd = fields.Float(compute=_get_totalsd, string='tva', help="solde au début de l\'exercice")
    tva_totalo = fields.Float(compute=_get_totalo, string='tva', help="Opérations comptables de l\'exercice")
    tva_totald = fields.Float(compute=_get_totald, string='tva', help="Déclarations T.V.A de l\'exercice")
    tva_totalsf = fields.Float(compute=_get_totalsf, string='tva', help="Solde fin d\'exercice")

    company_id = fields.Many2one(comodel_name="res.company", related='fiche.company_id', store=True)

    # line_ids = fields.One2many('account.move.line', 'move_id2')

    """
    _constraints = [
        (osv.osv._check_recursion, 'Error ! You cannot create recursive categories.', ['exercice_prec'])
    ]
    """

    @api.onchange('name', 'date_start', 'date_end')
    def onchange_fiscalyer(self):
        if self.name:
            self.date_start = self.name.date_start
            self.date_end = self.name.date_end
            # return {'value': {'date_start': date_start, 'date_end': date_end}}

    def update_data_passage(self):
        pasage_edi = self.env['liasse.passage.erp']
        passage_data = self.env['passage.erp']
        # liasse_conf = self.pool.get('liasse.configuration')
        # balance = self.pool.get('liasse.balance.line')
        liasse_conf = self.env['liasse.configuration.erp']
        balance = self.env['liasse.balance.line']
        pasage_edi_ids = pasage_edi.search([], limit=1)
        pasage_edi_obj = pasage_edi_ids
        total = 0

        for rec in self:
            compte_bal_ids = balance.search([('compte', '=like', '7' + "%"), ('balance_id', '=', rec.id)])
            compte_bal_obj = compte_bal_ids
            for compte_bal in compte_bal_obj:
                total += compte_bal.solde
            compte_bal_ids = balance.search([('compte', '=like', '6' + "%"), ('balance_id', '=', rec.id)])
            compte_bal_obj = compte_bal_ids
            for compte_bal in compte_bal_obj:
                total -= compte_bal.solde

        if total >= 0:
            self.write({'p_benifice_p': total})
        else:
            self.write({'p_perte_m': abs(total)})
        # reintegration courante
        total = 0
        for rec in self:
            rec.env.cr.execute("delete from passage_erp where balance_id=%s and name=%s",
                               (rec.id, "Ecart de conversion passif",))
            compte_bal_ids = balance.search([('compte', '=like', '47' + "%"), ('balance_id', '=', rec.id)])
            compte_bal_obj = compte_bal_ids
            for compte_bal in compte_bal_obj:
                total += compte_bal.solde
            if total != 0:
                passage_data.create({"name": "Ecart de conversion passif", "montant1": total, "type": "0",
                                     "balance_id": rec.id})

        list_compte = ['6128', '6148', '6168', '6178', '6188', '6198', '6388', '6398']
        total = 0
        for rec in self:
            rec.env.cr.execute("delete from passage_erp where balance_id=%s and name=%s",
                               (rec.id, "Charge sur exercice anterieur",))
            for com in list_compte:
                compte_bal_ids = balance.search([('compte', '=like', com + "%"), ('balance_id', '=', rec.id)])
                compte_bal_obj = compte_bal_ids
                for compte_bal in compte_bal_obj:
                    total += compte_bal.solde
            if total != 0:
                passage_data.create({"name": "Charge sur exercice anterieur", "montant1": total, "type": "0",
                                     "balance_id": rec.id})

        # reintegration non courante
        total = 0
        for rec in self:
            rec.env.cr.execute("delete from passage_erp where balance_id=%s and name=%s",
                               (rec.id, "Impôt sur societé",))
            compte_bal_ids = balance.search([('compte', '=like', '67' + "%"), ('balance_id', '=', rec.id)])
            compte_bal_obj = compte_bal_ids
            for compte_bal in compte_bal_obj:
                total += compte_bal.solde
            if total != 0:
                passage_data.create(
                    {"name": "Impôt sur societé", "montant1": total, "type": "1", "balance_id": rec.id})

        total = 0
        for rec in self:
            rec.env.cr.execute("delete from passage_erp where balance_id=%s and name=%s",
                               (rec.id, "Penalité et amande fiscal",))
            compte_bal_ids = balance.search([('compte', '=like', '6581' + "%"), ('balance_id', '=', rec.id)])
            compte_bal_obj = compte_bal_ids
            for compte_bal in compte_bal_obj:
                total += compte_bal.solde
            if total != 0:
                passage_data.create({"name": "Penalité et amande fiscal", "montant1": total, "type": "1",
                                     "balance_id": rec.id})

        total = 0
        for rec in self:
            rec.env.cr.execute("delete from passage_erp where balance_id=%s and name=%s",
                               (rec.id, "Dons et liberalité",))
            compte_bal_ids = balance.search([('compte', '=like', '6586' + "%"), ('balance_id', '=', rec.id)])
            compte_bal_obj = compte_bal_ids
            for compte_bal in compte_bal_obj:
                total += compte_bal.solde
            if total != 0:
                passage_data.create({"name": "Dons et liberalité", "montant1": total, "type": "1",
                                     "balance_id": rec.id})

        # deduction non courante
        total = 0
        for rec in self:
            rec.env.cr.execute("delete from passage_erp where balance_id=%s and name=%s",
                               (rec.id, "Ecarts de conversion",))
            compte_bal_ids = balance.search([('compte', '=like', '47' + "%"), ('balance_id', '=', rec.id)])
            compte_bal_obj = compte_bal_ids
            for compte_bal in compte_bal_obj:
                total += compte_bal.init_balance
            if total != 0:
                passage_data.create({"name": "Ecarts de conversion", "montant2": total, "type": "2",
                                     "balance_id": rec.id})

        return True

    def update_tva(self):
        liasse_conf = self.env['liasse.configuration.erp']
        balance = self.env['liasse.balance.line']
        tva = self.env['liasse.tva.erp']
        tva_ids = tva.search([], limit=1)
        tva_obj = tva_ids
        balance = self.env['liasse.balance.line']
        for rec in self:
            total1 = 0
            total2 = 0
            total3 = 0
            total4 = 0
            total5 = 0
            total6 = 0
            total7 = 0
            total8 = 0
            total9 = 0
            for line in tva_obj:
                compte_conf_ids = liasse_conf.search([('code', '=', line.tva_facsd.id)])
                compte_conf_obj = compte_conf_ids
                for compte_conf in compte_conf_obj:
                    for compte_id in compte_conf.compte:
                        compte_bal_ids = balance.search([('compte', '=like', compte_id.compte + "%"),
                                                         ('balance_id', '=', rec.id)])
                        compte_bal_obj = compte_bal_ids
                        for compte_bal in compte_bal_obj:
                            total1 += abs(compte_bal.init_balance)

                compte_conf_ids = liasse_conf.search([('code', '=', line.tva_charsd.id)])
                compte_conf_obj = compte_conf_ids
                for compte_conf in compte_conf_obj:
                    for compte_id in compte_conf.compte:
                        compte_bal_ids = balance.search([('compte', '=like', compte_id.compte + "%"),
                                                         ('balance_id', '=', rec.id)])
                        compte_bal_obj = compte_bal_ids
                        for compte_bal in compte_bal_obj:
                            total2 += abs(compte_bal.init_balance)

                compte_conf_ids = liasse_conf.search([('code', '=', line.tva_immosd.id)])
                compte_conf_obj = compte_conf_ids
                for compte_conf in compte_conf_obj:
                    for compte_id in compte_conf.compte:
                        compte_bal_ids = balance.search([('compte', '=like', compte_id.compte + "%"),
                                                         ('balance_id', '=', rec.id)])
                        compte_bal_obj = compte_bal_ids
                        for compte_bal in compte_bal_obj:
                            total3 += abs(compte_bal.init_balance)

                compte_conf_ids = liasse_conf.search([('code', '=', line.tva_facsf.id)])
                compte_conf_obj = compte_conf_ids
                for compte_conf in compte_conf_obj:
                    for compte_id in compte_conf.compte:
                        compte_bal_ids = balance.search([('compte', '=like', compte_id.compte + "%"),
                                                         ('balance_id', '=', rec.id)])
                        compte_bal_obj = compte_bal_ids
                        for compte_bal in compte_bal_obj:
                            total1 += compte_bal.solde

                compte_conf_ids = liasse_conf.search([('code', '=', line.tva_charsf.id)])
                compte_conf_obj = compte_conf_ids
                for compte_conf in compte_conf_obj:
                    for compte_id in compte_conf.compte:
                        compte_bal_ids = balance.search([('compte', '=like', compte_id.compte + "%"),
                                                         ('balance_id', '=', rec.id)])
                        compte_bal_obj = compte_bal_ids
                        for compte_bal in compte_bal_obj:
                            total2 += compte_bal.solde

                compte_conf_ids = liasse_conf.search([('code', '=', line.tva_immosf.id)])
                compte_conf_obj = compte_conf_ids
                for compte_conf in compte_conf_obj:
                    for compte_id in compte_conf.compte:
                        compte_bal_ids = balance.search([('compte', '=like', compte_id.compte + "%"),
                                                         ('balance_id', '=', rec.id)])
                        compte_bal_obj = compte_bal_ids
                        for compte_bal in compte_bal_obj:
                            total3 += compte_bal.solde

                ####
                compte_conf_ids = liasse_conf.search([('code', '=', line.tva_facd.id)])
                compte_conf_obj = compte_conf_ids
                for compte_conf in compte_conf_obj:
                    for compte_id in compte_conf.compte:
                        compte_bal_ids = balance.search([('compte', '=like', compte_id.compte + "%"),
                                                         ('balance_id', '=', rec.id)])
                        compte_bal_obj = compte_bal_ids
                        for compte_bal in compte_bal_obj:
                            total7 += compte_bal.debit

                compte_conf_ids = liasse_conf.search([('code', '=', line.tva_chard.id)])
                compte_conf_obj = compte_conf_ids
                for compte_conf in compte_conf_obj:
                    for compte_id in compte_conf.compte:
                        compte_bal_ids = balance.search([('compte', '=like', compte_id.compte + "%"),
                                                         ('balance_id', '=', rec.id)])
                        compte_bal_obj = compte_bal_ids
                        for compte_bal in compte_bal_obj:
                            total8 += compte_bal.credit

                compte_conf_ids = liasse_conf.search([('code', '=', line.tva_immod.id)])
                compte_conf_obj = compte_conf_ids
                for compte_conf in compte_conf_obj:
                    for compte_id in compte_conf.compte:
                        compte_bal_ids = balance.search([('compte', '=like', compte_id.compte + "%"),
                                                         ('balance_id', '=', rec.id)])
                        compte_bal_obj = compte_bal_ids
                        for compte_bal in compte_bal_obj:
                            total9 += compte_bal.credit
            total10 = total4 + total7 - total1
            total11 = total6 + total9 - total3
            total12 = total5 + total8 - total2
            self.write({
                'tva_facsd': total1, 'tva_charsd': total2, 'tva_immosd': total3, 'tva_facsf': total4,
                'tva_charsf': total5,
                'tva_immosf': total6, 'tva_facd': total7, 'tva_chard': total8, 'tva_immod': total9,
                'tva_faco': total10, 'tva_faco': total11, 'tva_charo': total12
            })
        return True

    def update_data(self):
        immo = self.env['liasse.immo.erp']
        immo_ids = immo.search([], limit=1)
        immo_obj = immo_ids
        liasse_conf = self.env['liasse.configuration.erp']
        balance = self.env['liasse.balance.line']
        # acquisition
        for rec in self:
            for line in immo_obj:
                frais, frais1 = self.get_acq(rec.id, line.fp_aug_acq.id)
                charge, charge1 = self.get_acq(rec.id, line.charge_aug_acq.id)
                prime, prime1 = self.get_acq(rec.id, line.prime_aug_acq.id)
                immord, immord1 = self.get_acq(rec.id, line.immord_aug_acq.id)
                brevet, brevet1 = self.get_acq(rec.id, line.brevet_aug_acq.id)
                fond, fond1 = self.get_acq(rec.id, line.fond_aug_acq.id)
                autre_incorp, autre_incorp1 = self.get_acq(rec.id, line.autre_incorp_aug_acq.id)
                terrain, terrain1 = self.get_acq(rec.id, line.terrain_aug_acq.id)
                constructions, constructions1 = self.get_acq(rec.id, line.constructions_aug_acq.id)
                inst, inst1 = self.get_acq(rec.id, line.inst_aug_acq.id)
                mat, mat1 = self.get_acq(rec.id, line.mat_aug_acq.id)
                mob, mob1 = self.get_acq(rec.id, line.mob_aug_acq.id)
                autre, autre1 = self.get_acq(rec.id, line.autre_corp_aug_acq.id)
                immocc, immocc1 = self.get_acq(rec.id, line.immocc_aug_acq.id)
                mati, mati1 = self.get_acq(rec.id, line.mati_aug_acq.id)
                self.write({
                    'fp_aug_acq': frais, 'charge_aug_acq': charge, 'prime_aug_acq': prime, 'immord_aug_acq': immord,
                    'brevet_aug_acq': brevet,
                    'fond_aug_acq': fond, 'autre_incorp_aug_acq': autre_incorp, 'terrain_aug_acq': terrain,
                    'constructions_aug_acq': constructions,
                    'inst_aug_acq': inst, 'mat_aug_acq': mat, 'mob_aug_acq': mob, 'autre_corp_aug_acq': autre,
                    'immocc_aug_acq': immocc,
                    'mati_aug_acq': mati,
                    'fp_mb': frais1, 'charge_mb': charge1, 'prime_mb': prime1, 'immord_mb': immord1,
                    'brevet_mb': brevet1,
                    'fond_mb': fond1, 'autre_incorp_mb': autre_incorp1, 'terrain_mb': terrain1,
                    'constructions_mb': constructions1,
                    'inst_mb': inst1, 'mat_mb': mat1, 'mob_mb': mob1, 'autre_corp_mb': autre1, 'immocc_mb': immocc1,
                    'mati_mb': mati1
                })
                frais = self.get_cess(rec.id, line.fp_dim_cess.id)
                charge = self.get_cess(rec.id, line.charge_dim_cess.id)
                prime = self.get_cess(rec.id, line.prime_dim_cess.id)
                immord = self.get_cess(rec.id, line.immord_dim_cess.id)
                brevet = self.get_cess(rec.id, line.brevet_dim_cess.id)
                fond = self.get_cess(rec.id, line.fond_dim_cess.id)
                autre_incorp = self.get_cess(rec.id, line.autre_incorp_dim_cess.id)
                terrain = self.get_cess(rec.id, line.terrain_dim_cess.id)
                constructions = self.get_cess(rec.id, line.constructions_dim_cess.id)
                inst = self.get_cess(rec.id, line.inst_dim_cess.id)
                mat = self.get_cess(rec.id, line.mat_dim_cess.id)
                mob = self.get_cess(rec.id, line.mob_dim_cess.id)
                autre = self.get_cess(rec.id, line.autre_corp_dim_cess.id)
                immocc = self.get_cess(rec.id, line.immocc_dim_cess.id)
                mati = self.get_cess(rec.id, line.mati_dim_cess.id)
                self.write({
                    'fp_dim_cess': frais, 'charge_dim_cess': charge, 'prime_dim_cess': prime, 'immord_dim_cess': immord,
                    'brevet_dim_cess': brevet,
                    'fond_dim_cess': fond, 'autre_incorp_dim_cess': autre_incorp, 'terrain_dim_cess': terrain,
                    'constructions_dim_cess': constructions,
                    'inst_dim_cess': inst, 'mat_dim_cess': mat, 'mob_dim_cess': mob, 'autre_corp_dim_cess': autre,
                    'immocc_dim_vir': immocc,
                    'mati_dim_cess': mati
                })

        return True

    def get_acq(self, bal_id, code):
        liasse_conf = self.env['liasse.configuration.erp']
        balance = self.env['liasse.balance.line']
        total = 0
        total1 = 0
        compte_conf_ids = liasse_conf.search([('code', '=', code)])
        compte_conf_obj = compte_conf_ids
        for compte_conf in compte_conf_obj:
            for compte_id in compte_conf.compte:
                compte_bal_ids = balance.search([('compte', '=like', compte_id.compte + "%"),
                                                 ('balance_id', '=', bal_id)])
                compte_bal_obj = compte_bal_ids
                for compte_bal in compte_bal_obj:
                    total += compte_bal.debit
                    total1 += compte_bal.init_balance
        return total, total1

    def get_cess(self, bal_id, code):
        liasse_conf = self.env['liasse.configuration.erp']
        balance = self.env['liasse.balance.line']
        total = 0
        compte_conf_ids = liasse_conf.search([('code', '=', code)])
        compte_conf_obj = compte_conf_ids
        for compte_conf in compte_conf_obj:
            for compte_id in compte_conf.compte:
                compte_bal_ids = balance.search([('compte', '=like', compte_id.compte + "%"),
                                                 ('balance_id', '=', bal_id)])
                compte_bal_obj = compte_bal_ids
                for compte_bal in compte_bal_obj:
                    total += compte_bal.credit
        return total

    def edi_affectation(self):
        affect = self.env['liasse.affect.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            affect_edi_ids = affect.search([], limit=1)
            affect_edi_obj = affect_edi_ids
            if affect_edi_obj:
                affect_edi_obj[0].code0.write({'valeur': rec.aff_rep_n})
                affect_edi_obj[0].code1.write({'valeur': rec.aff_res_n_in})
                affect_edi_obj[0].code2.write({'valeur': rec.aff_res_n_ex})
                affect_edi_obj[0].code3.write({'valeur': rec.aff_prev})
                affect_edi_obj[0].code4.write({'valeur': rec.aff_autre_prev})
                affect_edi_obj[0].code5.write({'valeur': rec.aff_totala})
                affect_edi_obj[0].code6.write({'valeur': rec.aff_rl})
                affect_edi_obj[0].code7.write({'valeur': rec.aff_autre_r})
                affect_edi_obj[0].code8.write({'valeur': rec.aff_tant})
                affect_edi_obj[0].code9.write({'valeur': rec.aff_div})
                affect_edi_obj[0].code10.write({'valeur': rec.aff_autre_aff})
                affect_edi_obj[0].code11.write({'valeur': rec.aff_rep_n2})
                affect_edi_obj[0].code12.write({'valeur': rec.aff_totalb})
        return True

    def generate_report(self):

        data = {}

        for rec in self:
            data["company"] = rec.fiche.company_id.name
            data["if"] = rec.fiche.id_fiscal
            data["clos"] = rec.date_end
            data["from"] = rec.date_start
            data["montant_cs"] = rec.montant_rcs
            data["montant_dot"] = rec.montant_dot
            data["id"] = rec.id
        print(data)

        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'report_name': 'report_xlsx.report_xlsx',
            'report_file': 'liasse_balance_erp',
            'data': data,
        }

    def check_list_rub(self):
        check_data = self.env['check.rubrique.erp']
        self.env.cr.execute(""" delete from check_rubrique_erp""")
        check_config = self.env['liasse.check.rub.erp']
        check_config_ids = check_config.search([])
        check_config_obj = check_config_ids
        for record in self:

            for check_line in check_config_obj:
                data = {}
                data["name"] = check_line.rub
                data["compte"] = check_line.compte
                total = 0
                for bal_line in record.balance_line:
                    if bal_line.compte.startswith(check_line.compte):
                        total += bal_line.solde
                data["valeurbal"] = total
                total = 0
                for code_some in check_line.code_ids:
                    total += float(code_some.valeur)
                data["valeurres"] = total

                check_data.create(data)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Rubriques de controle',
            'view_mode': 'tree',
            'view_type': 'form',
            'res_model': 'check.rubrique.erp',
            'target': 'new',
        }

    #
    def check_list(self):
        check_data = self.env['check.list.erp']
        self.env.cr.execute(""" delete from check_list_erp""")
        check_config = self.env['liasse.check.erp']
        check_config_ids = check_config.search([])
        check_config_obj = check_config_ids
        for check_line in check_config_obj:
            data = {}
            data["etat"] = check_line.etat
            data["name"] = check_line.code
            total_exo = 0
            total_exop = 0
            for code_some in check_line.coden_ids:
                total_exo += float(code_some.valeur)
            for code_min in check_line.coden_min_ids:
                total_exo -= float(code_min.valeur)
            data["exercice"] = total_exo

            for code_some in check_line.codenp_ids:
                total_exop += float(code_some.valeur)
            for code_min in check_line.codenp_min_ids:
                total_exop -= float(code_min.valeur)
            data["exercicep"] = total_exop
            check_data.create(data)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Check list',
            'view_mode': 'tree',
            'view_type': 'form',
            'res_model': 'check.list.erp',
            'target': 'new',
        }

    def generate_head(self):
        for rec in self:
            model_id = 1
            id_fiscal = rec.fiche.id_fiscal
            year_deb = rec.date_start
            year_fin = rec.date_end
            doc = etree.Element("Liasse", nsmap={})
            model = etree.SubElement(doc, "modele")
            id = etree.SubElement(model, "id")
            id.text = str(model_id)
            fiscal_result = etree.SubElement(doc, "resultatFiscal")
            id_fiscale = etree.SubElement(fiscal_result, "identifiantFiscal")
            id_fiscale.text = str(id_fiscal)
            yearf = etree.SubElement(fiscal_result, "exerciceFiscalDu")
            yearf.text = str(year_deb)
            yearl = etree.SubElement(fiscal_result, "exerciceFiscalAu")
            yearl.text = str(year_fin)
        return doc

    def generate_table(self, group_val, code):
        if float(code.valeur) != 0:
            val_cell = etree.SubElement(group_val, "ValeurCellule")
            cellule = etree.SubElement(val_cell, "cellule")
            codeEdi = etree.SubElement(cellule, "codeEdi")
            codeEdi.text = str(code.code)
            valeur = etree.SubElement(val_cell, "valeur")
            valeur.text = str("{0:.2f}".format(float(code.valeur)))
        else:
            val_cell = etree.SubElement(group_val, "ValeurCellule")
            cellule = etree.SubElement(val_cell, "cellule")
            codeEdi = etree.SubElement(cellule, "codeEdi")
            codeEdi.text = str(code.code)
            valeur = etree.SubElement(val_cell, "valeur")
        return True

    def generate_table_text(self, group_val, code):
        if code.valeur:
            val_cell = etree.SubElement(group_val, "ValeurCellule")
            cellule = etree.SubElement(val_cell, "cellule")
            codeEdi = etree.SubElement(cellule, "codeEdi")
            codeEdi.text = str(code.code)
            valeur = etree.SubElement(val_cell, "valeur")
            valeur.text = str(code.valeur)
        else:
            val_cell = etree.SubElement(group_val, "ValeurCellule")
            cellule = etree.SubElement(val_cell, "cellule")
            codeEdi = etree.SubElement(cellule, "codeEdi")
            codeEdi.text = str(code.code)
            valeur = etree.SubElement(val_cell, "valeur")
        return True

    def generate_table_date(self, group_val, code):
        if code.valeur:
            val_cell = etree.SubElement(group_val, "ValeurCellule")
            cellule = etree.SubElement(val_cell, "cellule")
            codeEdi = etree.SubElement(cellule, "codeEdi")
            codeEdi.text = str(code.code)
            valeur = etree.SubElement(val_cell, "valeur")
            date_f = dt.datetime.strptime(code.valeur, "%Y-%m-%d")
            date = date_f.strftime('%d/%m/%Y')
            valeur.text = str(date)
        else:
            val_cell = etree.SubElement(group_val, "ValeurCellule")
            cellule = etree.SubElement(val_cell, "cellule")
            codeEdi = etree.SubElement(cellule, "codeEdi")
            codeEdi.text = str(code.code)
            valeur = etree.SubElement(val_cell, "valeur")
        return True

    def generate_table_date_ilimite(self, group_val, code):
        if not code.valeur_ids:
            val_cell = etree.SubElement(group_val, "ValeurCellule")
            cellule = etree.SubElement(val_cell, "cellule")
            codeEdi = etree.SubElement(cellule, "codeEdi")
            codeEdi.text = str(code.code)
            valeur = etree.SubElement(val_cell, "valeur")
            lignenum = etree.SubElement(val_cell, "numeroLigne")
            lignenum.text = str(1)
        else:
            for val in code.valeur_ids:
                if val.valeur:
                    val_cell = etree.SubElement(group_val, "ValeurCellule")
                    cellule = etree.SubElement(val_cell, "cellule")
                    codeEdi = etree.SubElement(cellule, "codeEdi")
                    codeEdi.text = str(code.code)
                    valeur = etree.SubElement(val_cell, "valeur")
                    if val.valeur:
                        date_f = dt.datetime.strptime(val.valeur, "%Y-%m-%d")
                        date = date_f.strftime('%d/%m/%Y')
                        valeur.text = str(date)
                    lignenum = etree.SubElement(val_cell, "numeroLigne")
                    lignenum.text = str(val.ligne)
        return True

    def generate_table_ilimite(self, group_val, code):
        if not code.valeur_ids:
            val_cell = etree.SubElement(group_val, "ValeurCellule")
            cellule = etree.SubElement(val_cell, "cellule")
            codeEdi = etree.SubElement(cellule, "codeEdi")
            codeEdi.text = str(code.code)
            valeur = etree.SubElement(val_cell, "valeur")
            lignenum = etree.SubElement(val_cell, "numeroLigne")
            lignenum.text = str(1)

        else:
            for val in code.valeur_ids:
                if float(val.valeur) != 0:
                    val_cell = etree.SubElement(group_val, "ValeurCellule")
                    cellule = etree.SubElement(val_cell, "cellule")
                    codeEdi = etree.SubElement(cellule, "codeEdi")
                    codeEdi.text = str(code.code)
                    valeur = etree.SubElement(val_cell, "valeur")
                    if val.valeur:
                        valeur.text = str("{0:.2f}".format(float(val.valeur)))
                    lignenum = etree.SubElement(val_cell, "numeroLigne")
                    lignenum.text = str(val.ligne)
        return True

    def generate_table_entier_ilimite(self, group_val, code):
        if not code.valeur_ids:
            val_cell = etree.SubElement(group_val, "ValeurCellule")
            cellule = etree.SubElement(val_cell, "cellule")
            codeEdi = etree.SubElement(cellule, "codeEdi")
            codeEdi.text = str(code.code)
            valeur = etree.SubElement(val_cell, "valeur")
            lignenum = etree.SubElement(val_cell, "numeroLigne")
            lignenum.text = str(1)
        else:
            for val in code.valeur_ids:
                if int(val.valeur) != 0:
                    val_cell = etree.SubElement(group_val, "ValeurCellule")
                    cellule = etree.SubElement(val_cell, "cellule")
                    codeEdi = etree.SubElement(cellule, "codeEdi")
                    codeEdi.text = str(code.code)
                    valeur = etree.SubElement(val_cell, "valeur")
                    if val.valeur:
                        valeur.text = str(val.valeur)
                    lignenum = etree.SubElement(val_cell, "numeroLigne")
                    lignenum.text = str(val.ligne)
        return True

    def generate_table_text_ilimite(self, group_val, code):
        if not code.valeur_ids:
            val_cell = etree.SubElement(group_val, "ValeurCellule")
            cellule = etree.SubElement(val_cell, "cellule")
            codeEdi = etree.SubElement(cellule, "codeEdi")
            codeEdi.text = str(code.code)
            valeur = etree.SubElement(val_cell, "valeur")
            lignenum = etree.SubElement(val_cell, "numeroLigne")
            lignenum.text = str(1)
        else:
            for val in code.valeur_ids:
                if val.valeur:
                    val_cell = etree.SubElement(group_val, "ValeurCellule")
                    cellule = etree.SubElement(val_cell, "cellule")
                    codeEdi = etree.SubElement(cellule, "codeEdi")
                    codeEdi.text = str(code.code)
                    valeur = etree.SubElement(val_cell, "valeur")
                    if val.valeur:
                        valeur.text = val.valeur
                    lignenum = etree.SubElement(val_cell, "numeroLigne")
                    lignenum.text = str(val.ligne)
        return True

    def generate_extra_field(self, extra_vals, code):
        if code.valeur:
            extra_val = etree.SubElement(extra_vals, "ExtraFieldValeur")
            extra_field = etree.SubElement(extra_val, "extraField")
            code_extra = etree.SubElement(extra_field, "code")
            code_extra.text = str(code.code)
            date_f = dt.datetime.strptime(code.valeur, "%Y-%m-%d")
            date = date_f.strftime('%d/%m/%Y')
            code_val = etree.SubElement(extra_val, "valeur")
            code_val.text = str(date)
        return True

    def generate_extra_double_field(self, extra_vals, code):
        if float(code.valeur) != 0:
            extra_val = etree.SubElement(extra_vals, "ExtraFieldValeur")
            extra_field = etree.SubElement(extra_val, "extraField")
            code_extra = etree.SubElement(extra_field, "code")
            code_extra.text = str(code.code)
            code_val = etree.SubElement(extra_val, "valeur")
            code_val.text = str("{0:.2f}".format(float(code.valeur)))
        return True

    def generate(self):
        # edi
        self.edi_actif()
        self.edi_affectation()
        self.edi_amort()
        self.edi_beaux()
        self.edi_caf()
        self.edi_cpc()
        self.edi_credit_bail()
        self.edi_det_cpc()
        self.edi_dotation()
        self.edi_encouragement()
        self.edi_fusion()
        self.edi_immo()
        self.edi_interets()
        self.edi_passage()
        self.edi_passif()
        self.edi_pm_value()
        self.edi_provision()
        self.edi_repart_cs()
        self.edi_stock()
        self.edi_tfr()
        self.edi_titre_particp()
        self.edi_tva()
        #############################
        doc = self.generate_head()
        group_val_tab = etree.SubElement(doc, "groupeValeursTableau")
        extra_tab = self.env["liasse.extra.field.erp"]
        extra_tab_ids = extra_tab.search([], limit=1)
        extra_tab_obj = extra_tab_ids

        # actif
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(2)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        actif_ids = self.env["liasse.bilan.actif.erp"].search([])
        actif_obj = actif_ids
        for line in actif_obj:
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)
            self.generate_table(group_val, line.code3)
            self.generate_table(group_val, line.code4)

        # passif
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(1)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        passif_ids = self.env["liasse.bilan.passif.erp"].search([])
        passif_obj = passif_ids
        for line in passif_obj:
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)

        # cpc
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(6)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        cpc_ids = self.env["liasse.cpc.erp"].search([])
        cpc_obj = cpc_ids
        for line in cpc_obj:
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)
            self.generate_table(group_val, line.code3)
            self.generate_table(group_val, line.code4)

        # esg
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(32)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        tfr_ids = self.env["liasse.tfr.erp"].search([])
        tfr_obj = tfr_ids
        for line in tfr_obj:
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)
        caf_ids = self.env["liasse.caf.erp"].search([])
        caf_obj = caf_ids
        for line in caf_obj:
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)

        # det cpc
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(34)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        det_cpc_ids = self.env["liasse.det.cpc.erp"].search([])
        det_cpc_obj = det_cpc_ids
        for line in det_cpc_obj:
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)
        for extra_line in extra_tab_obj:
            self.generate_extra_field(extra_vals, extra_line.code0cpc)

        # amort
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(24)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        amort_ids = self.env["liasse.amort.erp"].search([])
        amort_obj = amort_ids
        for line in amort_obj:
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)
            self.generate_table(group_val, line.code3)
            self.generate_table(group_val, line.code4)

        # prov
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(37)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        prov_ids = self.env["liasse.provision.erp"].search([])
        prov_obj = prov_ids
        for line in prov_obj:
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)
            self.generate_table(group_val, line.code3)
            self.generate_table(group_val, line.code4)
            self.generate_table(group_val, line.code5)
            self.generate_table(group_val, line.code6)
            self.generate_table(group_val, line.code7)
            self.generate_table(group_val, line.code8)
        for extra_line in extra_tab_obj:
            self.generate_extra_field(extra_vals, extra_line.code1prov)

        # stock
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(36)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        stock_ids = self.env["liasse.stock.erp"].search([])
        stock_obj = stock_ids
        for line in stock_obj:
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)
            self.generate_table(group_val, line.code3)
            self.generate_table(group_val, line.code4)
            self.generate_table(group_val, line.code5)
            self.generate_table(group_val, line.code6)
            self.generate_table(group_val, line.code7)

        # tva
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(40)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        tva_ids = self.env["liasse.tva.erp"].search([], limit=1)
        tva_obj = tva_ids
        for line in tva_obj:
            self.generate_table(group_val, line.tva_facsd)
            self.generate_table(group_val, line.tva_faco)
            self.generate_table(group_val, line.tva_facd)
            self.generate_table(group_val, line.tva_facsf)
            self.generate_table(group_val, line.tva_recsd)
            self.generate_table(group_val, line.tva_reco)
            self.generate_table(group_val, line.tva_recd)
            self.generate_table(group_val, line.tva_recsf)
            self.generate_table(group_val, line.tva_charsd)
            self.generate_table(group_val, line.tva_charo)
            self.generate_table(group_val, line.tva_chard)
            self.generate_table(group_val, line.tva_charsf)
            self.generate_table(group_val, line.tva_immosd)
            self.generate_table(group_val, line.tva_immoo)
            self.generate_table(group_val, line.tva_immod)
            self.generate_table(group_val, line.tva_immosf)
            self.generate_table(group_val, line.tva_totalsd)
            self.generate_table(group_val, line.tva_totalo)
            self.generate_table(group_val, line.tva_totald)
            self.generate_table(group_val, line.tva_totalsf)

        # immo
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(11)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        immo_ids = self.env["liasse.immo.erp"].search([], limit=1)
        immo_obj = immo_ids
        for line in immo_obj:
            self.generate_table(group_val, line.code0)
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)
            self.generate_table(group_val, line.code3)
            self.generate_table(group_val, line.code4)
            self.generate_table(group_val, line.code5)
            self.generate_table(group_val, line.code6)
            self.generate_table(group_val, line.code7)
            self.generate_table(group_val, line.fp_mb)
            self.generate_table(group_val, line.fp_aug_acq)
            self.generate_table(group_val, line.fp_aug_pd)
            self.generate_table(group_val, line.fp_aug_vir)
            self.generate_table(group_val, line.fp_dim_cess)
            self.generate_table(group_val, line.fp_dim_ret)
            self.generate_table(group_val, line.fp_dim_vir)
            self.generate_table(group_val, line.fp_mbf)
            self.generate_table(group_val, line.charge_mb)
            self.generate_table(group_val, line.charge_aug_acq)
            self.generate_table(group_val, line.charge_aug_pd)
            self.generate_table(group_val, line.charge_aug_vir)
            self.generate_table(group_val, line.charge_dim_cess)
            self.generate_table(group_val, line.charge_dim_ret)
            self.generate_table(group_val, line.charge_dim_vir)
            self.generate_table(group_val, line.charge_mbf)
            self.generate_table(group_val, line.prime_mb)
            self.generate_table(group_val, line.prime_aug_acq)
            self.generate_table(group_val, line.prime_aug_pd)
            self.generate_table(group_val, line.prime_aug_vir)
            self.generate_table(group_val, line.prime_dim_cess)
            self.generate_table(group_val, line.prime_dim_ret)
            self.generate_table(group_val, line.prime_dim_vir)
            self.generate_table(group_val, line.prime_mbf)
            self.generate_table(group_val, line.code8)
            self.generate_table(group_val, line.code9)
            self.generate_table(group_val, line.code10)
            self.generate_table(group_val, line.code11)
            self.generate_table(group_val, line.code12)
            self.generate_table(group_val, line.code13)
            self.generate_table(group_val, line.code14)
            self.generate_table(group_val, line.code15)
            self.generate_table(group_val, line.immord_mb)
            self.generate_table(group_val, line.immord_aug_acq)
            self.generate_table(group_val, line.immord_aug_pd)
            self.generate_table(group_val, line.immord_aug_vir)
            self.generate_table(group_val, line.immord_dim_cess)
            self.generate_table(group_val, line.immord_dim_ret)
            self.generate_table(group_val, line.immord_dim_vir)
            self.generate_table(group_val, line.immord_mbf)
            self.generate_table(group_val, line.brevet_mb)
            self.generate_table(group_val, line.brevet_aug_acq)
            self.generate_table(group_val, line.brevet_aug_pd)
            self.generate_table(group_val, line.brevet_aug_vir)
            self.generate_table(group_val, line.brevet_dim_cess)
            self.generate_table(group_val, line.brevet_dim_ret)
            self.generate_table(group_val, line.brevet_dim_vir)
            self.generate_table(group_val, line.brevet_mbf)

            self.generate_table(group_val, line.fond_mb)
            self.generate_table(group_val, line.fond_aug_acq)
            self.generate_table(group_val, line.fond_aug_pd)
            self.generate_table(group_val, line.fond_aug_vir)
            self.generate_table(group_val, line.fond_dim_cess)
            self.generate_table(group_val, line.fond_dim_ret)
            self.generate_table(group_val, line.fond_dim_vir)
            self.generate_table(group_val, line.fond_mbf)

            self.generate_table(group_val, line.autre_incorp_mb)
            self.generate_table(group_val, line.autre_incorp_aug_acq)
            self.generate_table(group_val, line.autre_incorp_aug_pd)
            self.generate_table(group_val, line.autre_incorp_aug_vir)
            self.generate_table(group_val, line.autre_incorp_dim_cess)
            self.generate_table(group_val, line.autre_incorp_dim_ret)
            self.generate_table(group_val, line.autre_incorp_dim_vir)
            self.generate_table(group_val, line.autre_incorp_mbf)

            self.generate_table(group_val, line.code16)
            self.generate_table(group_val, line.code17)
            self.generate_table(group_val, line.code18)
            self.generate_table(group_val, line.code19)
            self.generate_table(group_val, line.code20)
            self.generate_table(group_val, line.code21)
            self.generate_table(group_val, line.code22)
            self.generate_table(group_val, line.code23)

            self.generate_table(group_val, line.terrain_mb)
            self.generate_table(group_val, line.terrain_aug_acq)
            self.generate_table(group_val, line.terrain_aug_pd)
            self.generate_table(group_val, line.terrain_aug_vir)
            self.generate_table(group_val, line.terrain_dim_cess)
            self.generate_table(group_val, line.terrain_dim_ret)
            self.generate_table(group_val, line.terrain_dim_vir)
            self.generate_table(group_val, line.terrain_mbf)

            self.generate_table(group_val, line.constructions_mb)
            self.generate_table(group_val, line.constructions_aug_acq)
            self.generate_table(group_val, line.constructions_aug_pd)
            self.generate_table(group_val, line.constructions_aug_vir)
            self.generate_table(group_val, line.constructions_dim_cess)
            self.generate_table(group_val, line.constructions_dim_ret)
            self.generate_table(group_val, line.constructions_dim_vir)
            self.generate_table(group_val, line.constructions_mbf)

            self.generate_table(group_val, line.inst_mb)
            self.generate_table(group_val, line.inst_aug_acq)
            self.generate_table(group_val, line.inst_aug_pd)
            self.generate_table(group_val, line.inst_aug_vir)
            self.generate_table(group_val, line.inst_dim_cess)
            self.generate_table(group_val, line.inst_dim_ret)
            self.generate_table(group_val, line.inst_dim_vir)
            self.generate_table(group_val, line.inst_mbf)

            self.generate_table(group_val, line.mat_mb)
            self.generate_table(group_val, line.mat_aug_acq)
            self.generate_table(group_val, line.mat_aug_pd)
            self.generate_table(group_val, line.mat_aug_vir)
            self.generate_table(group_val, line.mat_dim_cess)
            self.generate_table(group_val, line.mat_dim_ret)
            self.generate_table(group_val, line.mat_dim_vir)
            self.generate_table(group_val, line.mat_mbf)

            self.generate_table(group_val, line.mob_mb)
            self.generate_table(group_val, line.mob_aug_acq)
            self.generate_table(group_val, line.mob_aug_pd)
            self.generate_table(group_val, line.mob_aug_vir)
            self.generate_table(group_val, line.mob_dim_cess)
            self.generate_table(group_val, line.mob_dim_ret)
            self.generate_table(group_val, line.mob_dim_vir)
            self.generate_table(group_val, line.mob_mbf)

            self.generate_table(group_val, line.autre_corp_mb)
            self.generate_table(group_val, line.autre_corp_aug_acq)
            self.generate_table(group_val, line.autre_corp_aug_pd)
            self.generate_table(group_val, line.autre_corp_aug_vir)
            self.generate_table(group_val, line.autre_corp_dim_cess)
            self.generate_table(group_val, line.autre_corp_dim_ret)
            self.generate_table(group_val, line.autre_corp_dim_vir)
            self.generate_table(group_val, line.autre_corp_mbf)

            self.generate_table(group_val, line.immocc_mb)
            self.generate_table(group_val, line.immocc_aug_acq)
            self.generate_table(group_val, line.immocc_aug_pd)
            self.generate_table(group_val, line.immocc_aug_vir)
            self.generate_table(group_val, line.immocc_dim_cess)
            self.generate_table(group_val, line.immocc_dim_ret)
            self.generate_table(group_val, line.immocc_dim_vir)
            self.generate_table(group_val, line.immocc_mbf)

            self.generate_table(group_val, line.mati_mb)
            self.generate_table(group_val, line.mati_aug_acq)
            self.generate_table(group_val, line.mati_aug_pd)
            self.generate_table(group_val, line.mati_aug_vir)
            self.generate_table(group_val, line.mati_dim_cess)
            self.generate_table(group_val, line.mati_dim_ret)
            self.generate_table(group_val, line.mati_dim_vir)
            self.generate_table(group_val, line.mati_mbf)

        # fusion
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(26)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        actif_ids = self.env["liasse.fusion.erp"].search([])
        actif_obj = actif_ids
        for line in actif_obj:
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)
            self.generate_table(group_val, line.code3)
            self.generate_table(group_val, line.code4)
            self.generate_table(group_val, line.code5)
            self.generate_table(group_val, line.code6)
            self.generate_table(group_val, line.code7)
            self.generate_table_text(group_val, line.code8)
        for extra_line in extra_tab_obj:
            self.generate_extra_field(extra_vals, extra_line.code2fusion)

        # encouragement
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(10)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        encourg_ids = self.env["liasse.encour.erp"].search([], limit=1)
        encourg_obj = encourg_ids
        for line in encourg_obj:
            self.generate_table(group_val, line.code0)
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)
            self.generate_table(group_val, line.code3)
            self.generate_table(group_val, line.code4)
            self.generate_table(group_val, line.code5)
            self.generate_table(group_val, line.code6)
            self.generate_table(group_val, line.code7)
            self.generate_table(group_val, line.code8)
            self.generate_table(group_val, line.code9)
            self.generate_table(group_val, line.code10)
            self.generate_table(group_val, line.code12)
            self.generate_table(group_val, line.code13)
            self.generate_table(group_val, line.code14)
            self.generate_table(group_val, line.code15)
            self.generate_table(group_val, line.code16)
            self.generate_table(group_val, line.code17)
            self.generate_table(group_val, line.code18)
            self.generate_table(group_val, line.code19)
            self.generate_table(group_val, line.code20)
            self.generate_table(group_val, line.code21)
            self.generate_table(group_val, line.code22)
            self.generate_table(group_val, line.code23)
            self.generate_table(group_val, line.code24)
            self.generate_table(group_val, line.code25)
            self.generate_table(group_val, line.code26)
            self.generate_table(group_val, line.code27)
            self.generate_table(group_val, line.code28)
            self.generate_table(group_val, line.code29)
            self.generate_table(group_val, line.code30)
            self.generate_table(group_val, line.code31)
            self.generate_table(group_val, line.code32)
            self.generate_table(group_val, line.code33)
            self.generate_table(group_val, line.code34)
            self.generate_table(group_val, line.code35)
            self.generate_table(group_val, line.code36)
            self.generate_table(group_val, line.code37)
            self.generate_table(group_val, line.code38)
            self.generate_table(group_val, line.code39)
            self.generate_table(group_val, line.code40)
            self.generate_table(group_val, line.code41)
            self.generate_table(group_val, line.code42)
            self.generate_table(group_val, line.code43)
            self.generate_table(group_val, line.code44)
            self.generate_table(group_val, line.code45)
            self.generate_table(group_val, line.code46)
            self.generate_table(group_val, line.code47)
            self.generate_table(group_val, line.code48)
            self.generate_table(group_val, line.code49)
            self.generate_table(group_val, line.code50)
            self.generate_table(group_val, line.code51)
            self.generate_table(group_val, line.code52)
            self.generate_table(group_val, line.code53)
            self.generate_table(group_val, line.code54)
            self.generate_table(group_val, line.code55)
            self.generate_table(group_val, line.code56)

        # affectation
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(5)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        affect_ids = self.env["liasse.affect.erp"].search([], limit=1)
        affect_obj = affect_ids
        for line in affect_obj:
            self.generate_table(group_val, line.code0)
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code2)
            self.generate_table(group_val, line.code3)
            self.generate_table(group_val, line.code4)
            self.generate_table(group_val, line.code5)
            self.generate_table(group_val, line.code6)
            self.generate_table(group_val, line.code7)
            self.generate_table(group_val, line.code8)
            self.generate_table(group_val, line.code9)
            self.generate_table(group_val, line.code10)
            self.generate_table(group_val, line.code12)

        # credit bail
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(23)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        credit_ids = self.env["liasse.credit.bail.erp"].search([], limit=1)
        credit_obj = credit_ids
        for line in credit_obj:
            for creditbail in line.credit_bail_ids:
                self.generate_table_text_ilimite(group_val, creditbail.code0)
                self.generate_table_date_ilimite(group_val, creditbail.code1)
                self.generate_table_entier_ilimite(group_val, creditbail.code2)
                self.generate_table_ilimite(group_val, creditbail.code3)
                self.generate_table_ilimite(group_val, creditbail.code4)
                self.generate_table_ilimite(group_val, creditbail.code5)
                self.generate_table_ilimite(group_val, creditbail.code6)
                self.generate_table_ilimite(group_val, creditbail.code7)
                self.generate_table_ilimite(group_val, creditbail.code8)
                self.generate_table_ilimite(group_val, creditbail.code9)
                self.generate_table_text_ilimite(group_val, creditbail.code10)
            self.generate_extra_field(extra_vals, line.extra_field_clos)

        # pm value
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(38)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        pm_ids = self.env["liasse.pm.value.erp"].search([], limit=1)
        pm_obj = pm_ids
        for line in pm_obj:
            for pmline in line.pm_val_ids:
                self.generate_table_date_ilimite(group_val, pmline.code0)
                self.generate_table_ilimite(group_val, pmline.code1)
                self.generate_table_ilimite(group_val, pmline.code2)
                self.generate_table_ilimite(group_val, pmline.code3)
                self.generate_table_ilimite(group_val, pmline.code4)
                self.generate_table_ilimite(group_val, pmline.code5)
                self.generate_table_ilimite(group_val, pmline.code6)
                self.generate_table_ilimite(group_val, pmline.code7)
            self.generate_extra_field(extra_vals, line.extra_field_clos)
            self.generate_table(group_val, line.compte_princ)
            self.generate_table(group_val, line.montant_brut)
            self.generate_table(group_val, line.amort_cumul)
            self.generate_table(group_val, line.val_net_amort)
            self.generate_table(group_val, line.prod_cess)
            self.generate_table(group_val, line.plus_value)
            self.generate_table(group_val, line.moins_value)

        # Titre de participation
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(39)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        titre_ids = self.env["liasse.titre.particip.erp"].search([], limit=1)
        titre_obj = titre_ids
        for line in titre_obj:
            for titreline in line.titre_particip_ids:
                self.generate_table_text_ilimite(group_val, titreline.code0)
                self.generate_table_text_ilimite(group_val, titreline.code1)
                self.generate_table_ilimite(group_val, titreline.code2)
                self.generate_table_ilimite(group_val, titreline.code3)
                self.generate_table_ilimite(group_val, titreline.code4)
                self.generate_table_ilimite(group_val, titreline.code5)
                self.generate_table_date_ilimite(group_val, titreline.code6)
                self.generate_table_ilimite(group_val, titreline.code7)
                self.generate_table_ilimite(group_val, titreline.code8)
                self.generate_table_ilimite(group_val, titreline.code8)
                self.generate_table_ilimite(group_val, titreline.code9)

            # self.generate_table_text( group_val, line.code1)
            self.generate_table(group_val, line.code2)
            self.generate_table(group_val, line.code3)
            self.generate_table(group_val, line.code4)
            self.generate_table(group_val, line.code5)
            self.generate_table_date(group_val, line.code6)
            self.generate_table(group_val, line.code7)
            self.generate_table(group_val, line.code8)
            self.generate_table(group_val, line.code9)

        # repartition capital social
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(41)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        rpcp_ids = self.env["liasse.repart.cs.erp"].search([], limit=1)
        rpcp_obj = rpcp_ids
        for line in rpcp_obj:
            for rpcpline in line.repart_cs_ids:
                self.generate_table_text_ilimite(group_val, rpcpline.code0)
                self.generate_table_entier_ilimite(group_val, rpcpline.code1)
                self.generate_table_text_ilimite(group_val, rpcpline.code2)
                self.generate_table_text_ilimite(group_val, rpcpline.code3)
                self.generate_table_entier_ilimite(group_val, rpcpline.code4)
                self.generate_table_entier_ilimite(group_val, rpcpline.code5)
                self.generate_table_ilimite(group_val, rpcpline.code6)
                self.generate_table_ilimite(group_val, rpcpline.code7)
                self.generate_table_ilimite(group_val, rpcpline.code8)
                self.generate_table_ilimite(group_val, rpcpline.code9)

            self.generate_extra_double_field(extra_vals, line.montant_capital)

        # Beaux
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(28)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        beaux_ids = self.env["liasse.beaux.erp"].search([], limit=1)
        beaux_obj = beaux_ids
        for line in beaux_obj:
            for beaux in line.beaux_ids:
                self.generate_table_text_ilimite(group_val, beaux.code0)
                self.generate_table_text_ilimite(group_val, beaux.code1)
                self.generate_table_text_ilimite(group_val, beaux.code2)
                self.generate_table_date_ilimite(group_val, beaux.code3)
                self.generate_table_ilimite(group_val, beaux.code4)
                self.generate_table_ilimite(group_val, beaux.code5)
                self.generate_table_text_ilimite(group_val, beaux.code6)
                self.generate_table_text_ilimite(group_val, beaux.code7)

            self.generate_table(group_val, line.code0)
            self.generate_table(group_val, line.code1)

        # passage
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(7)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        passage_ids = self.env["liasse.passage.erp"].search([], limit=1)
        passage_obj = passage_ids
        for line in passage_obj:
            for passage in line.passages_rfc:
                self.generate_table_text_ilimite(group_val, passage.code0)
                self.generate_table_ilimite(group_val, passage.code1)
                # self.generate_table_ilimite( group_val, passage.code2)
            for passage in line.passages_rfnc:
                self.generate_table_text_ilimite(group_val, passage.code0)
                self.generate_table_ilimite(group_val, passage.code1)
                # self.generate_table_ilimite( group_val, passage.code2)
            for passage in line.passages_dfc:
                self.generate_table_text_ilimite(group_val, passage.code0)
                # self.generate_table_ilimite( group_val, passage.code1)
                self.generate_table_ilimite(group_val, passage.code2)
            for passage in line.passages_dfnc:
                self.generate_table_text_ilimite(group_val, passage.code0)
                # self.generate_table_ilimite( group_val, passage.code1)
                self.generate_table_ilimite(group_val, passage.code2)

            self.generate_table(group_val, line.code0)
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code3)
            self.generate_table(group_val, line.code4)
            self.generate_table(group_val, line.code5)
            self.generate_table(group_val, line.code6)
            self.generate_table(group_val, line.code7)
            self.generate_table(group_val, line.code8)
            self.generate_table(group_val, line.code9)
            self.generate_table(group_val, line.code10)
            self.generate_table(group_val, line.code12)
            self.generate_table(group_val, line.code14)
            self.generate_table(group_val, line.code16)
            self.generate_table(group_val, line.code18)
            self.generate_table(group_val, line.code19)
            self.generate_table(group_val, line.code20)
            self.generate_table(group_val, line.code21)
            self.generate_table(group_val, line.code22)
            self.generate_table(group_val, line.code23)
            self.generate_table(group_val, line.code24)
            self.generate_table(group_val, line.code25)
            self.generate_table(group_val, line.code26)

        # Interets
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(27)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        interets_ids = self.env["liasse.interets.erp"].search([], limit=1)
        interets_obj = interets_ids
        for line in interets_obj:
            for interet in line.interets_associe:
                self.generate_table_text_ilimite(group_val, interet.code0)
                self.generate_table_text_ilimite(group_val, interet.code1)
                self.generate_table_text_ilimite(group_val, interet.code2)
                self.generate_table_ilimite(group_val, interet.code3)
                self.generate_table_date_ilimite(group_val, interet.code4)
                self.generate_table_entier_ilimite(group_val, interet.code5)
                self.generate_table_text_ilimite(group_val, interet.code6)
                self.generate_table_ilimite(group_val, interet.code7)
                self.generate_table_ilimite(group_val, interet.code8)
                self.generate_table_ilimite(group_val, interet.code9)
                self.generate_table_ilimite(group_val, interet.code10)
                self.generate_table_ilimite(group_val, interet.code11)
                self.generate_table_text_ilimite(group_val, interet.code12)

            for interet in line.interets_tier:
                self.generate_table_text_ilimite(group_val, interet.code0)
                self.generate_table_text_ilimite(group_val, interet.code1)
                self.generate_table_text_ilimite(group_val, interet.code2)
                self.generate_table_ilimite(group_val, interet.code3)
                self.generate_table_date_ilimite(group_val, interet.code4)
                self.generate_table_entier_ilimite(group_val, interet.code5)
                self.generate_table_text_ilimite(group_val, interet.code6)
                self.generate_table_ilimite(group_val, interet.code7)
                self.generate_table_ilimite(group_val, interet.code8)
                self.generate_table_ilimite(group_val, interet.code9)
                self.generate_table_ilimite(group_val, interet.code10)
                self.generate_table_ilimite(group_val, interet.code11)
                self.generate_table_text_ilimite(group_val, interet.code12)

            self.generate_extra_field(extra_vals, line.code0)
            self.generate_table(group_val, line.code1)
            self.generate_table(group_val, line.code3)
            self.generate_table(group_val, line.code4)
            self.generate_table(group_val, line.code5)
            self.generate_table(group_val, line.code6)

        # Dotation aux amortissement
        val_tab = etree.SubElement(group_val_tab, "ValeursTableau")
        tableau = etree.SubElement(val_tab, "tableau")
        id = etree.SubElement(tableau, "id")
        id.text = str(12)
        group_val = etree.SubElement(val_tab, "groupeValeurs")
        extra_vals = etree.SubElement(val_tab, "extraFieldvaleurs")
        dotation_ids = self.env["liasse.dotation.erp"].search([], limit=1)
        dotation_obj = dotation_ids
        for line in dotation_obj:
            for dot in line.dotation_line_ids:
                self.generate_table_text_ilimite(group_val, dot.code0)
                self.generate_table_date_ilimite(group_val, dot.code1)
                self.generate_table_ilimite(group_val, dot.code2)
                self.generate_table_ilimite(group_val, dot.code3)
                self.generate_table_ilimite(group_val, dot.code4)
                self.generate_table_ilimite(group_val, dot.code5)
                self.generate_table_entier_ilimite(group_val, dot.code6)
                self.generate_table_ilimite(group_val, dot.code7)
                self.generate_table_ilimite(group_val, dot.code8)
                self.generate_table_text_ilimite(group_val, dot.code9)

            self.generate_extra_double_field(extra_vals, line.montant_global)
            self.generate_extra_field(extra_vals, line.clos)
            self.generate_extra_field(extra_vals, line.date_from)
            self.generate_extra_field(extra_vals, line.date_end)
            self.generate_table(group_val, line.val_acq)
            self.generate_table(group_val, line.val_compt)
            self.generate_table(group_val, line.amort_ant)
            self.generate_table(group_val, line.amort_ded_e)
            self.generate_table(group_val, line.amort_fe)

        xml_data = "%s" % (
            etree.tostring(doc, pretty_print=True, xml_declaration=True,
                           encoding='UTF-8'
                           )
        )
        xml_data = xml_data[2:-1].replace("\\n", '\n')

        self.write({
            'output': base64.encodestring(xml_data.encode("utf-8"))
        })

        return True

    def generate_fiscale(self):
        print("call generate_fiscale")
        for field in self:
            if field.exercice_prec:
                print(field.exercice_prec)
                print(field.exercice_prec)
                print(field['exercice_prec'][0])
                self.report_nouveau(field['exercice_prec'][0])
            else:
                self.report_nouveau(field.exercice_prec)

        ###
        self.generate_actif()
        self.generate_passif()
        self.generate_cpc()
        self.update_data_passage()
        self.update_data()
        self.edi_affectation()
        self.generate_tfr()
        self.generate_caf()
        self.generate_det_cpc()
        self.generate_amort()
        self.generate_provision()
        self.generate_stock()
        self.generate_fusion()
        self.update_tva()
        return True

    def generate_actif(self):
        print("call generate_actif")
        code_conf = self.env['liasse.code.erp']
        actif = self.env['bilan.actif.fiscale.erp']
        bilan_actif = self.env['liasse.bilan.actif.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        for rec in self:
            rec.env.cr.execute("delete from bilan_actif_fiscale_erp where balance_id=" + str(rec.id))
        for code in bilan_actif_obj:
            total1 = self.count_cell(code.code1)
            total2 = self.count_cell(code.code2)
            total3 = total1 - total2
            total4 = self.count_cell(code.code4)
            print("generate_actif 111=====", code.code3.code, code.code3.valeur)
            code.code3.write({'valeur': total3})
            print("generate_actif 222=====", code.code3.code, code.code3.valeur)
            print("+++++++++++++++++++++++", code.code1, code.code2, code.code3, code.code4)
            data = {}
            data["lib"] = code.lib
            data["code1"] = total1
            data["code2"] = total2
            data["code3"] = total3
            data["code4"] = total4
            data["code0"] = code.id
            data["type"] = code.type
            data["sequence"] = code.sequence
            for rec in self:
                data["balance_id"] = rec.id
            actif.create(data)
            # print(code.z)
        return True

    #
    def generate_passif(self):
        actif = self.env['bilan.passif.fiscale.erp']
        bilan_actif = self.env['liasse.bilan.passif.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        for rec in self:
            rec.env.cr.execute("delete from bilan_passif_fiscale_erp where balance_id=" + str(rec.id))
        for code in bilan_actif_obj:
            total2 = self.count_cell(code.code2)
            print('passif: code2: ', total2, 'code: ', code.code2.code)
            total1 = self.count_cell(code.code1)
            print('passif: code1: ', total1)

            data = {}
            data["lib"] = code.lib
            data["code1"] = total1
            data["code2"] = total2
            data["code0"] = code.id
            data["type"] = code.type
            data["sequence"] = code.sequence
            for rec in self:
                data["balance_id"] = rec.id
            actif.create(data)
        return True

    def generate_cpc(self):
        code_conf = self.env['liasse.code.erp']
        actif = self.env['cpc.fiscale.erp']
        bilan_actif = self.env['liasse.cpc.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        for rec in self:
            rec.env.cr.execute("delete from cpc_fiscale_erp where balance_id=" + str(rec.id))
        for code in bilan_actif_obj:
            total1 = self.count_cell(code.code1)
            total2 = self.count_cell(code.code2)
            total4 = self.count_cell(code.code4)
            total3 = total1 + total2
            code.code3.write({'valeur': total3})

            data = {}
            data["lib"] = code.lib
            data["code1"] = total1
            data["code2"] = total2
            data["code3"] = total3
            data["code4"] = total4
            data["code0"] = code.id
            data["type"] = code.type
            data["sequence"] = code.sequence
            for rec in self:
                data["balance_id"] = rec.id
            actif.create(data)
        return True

    def generate_det_cpc(self):
        actif = self.env['det.cpc.fiscale.erp']
        bilan_actif = self.env['liasse.det.cpc.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        for rec in self:
            rec.env.cr.execute("delete from det_cpc_fiscale_erp where balance_id=" + str(rec.id))
        for code in bilan_actif_obj:
            total2 = self.count_cell(code.code2)
            total1 = self.count_cell(code.code1)

            data = {}
            data["poste"] = code.poste
            data["lib"] = code.lib
            data["code1"] = total1
            data["code2"] = total2
            data["code0"] = code.id
            data["type"] = code.type
            data["sequence"] = code.sequence
            for rec in self:
                data["balance_id"] = rec.id
            actif.create(data)
        return True

    def generate_tfr(self):
        actif = self.env['tfr.fiscale.erp']
        bilan_actif = self.env['liasse.tfr.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        for rec in self:
            rec.env.cr.execute("delete from tfr_fiscale_erp where balance_id=" + str(rec.id))
        for code in bilan_actif_obj:
            total2 = self.count_cell(code.code2)
            total1 = self.count_cell(code.code1)

            data = {}
            data["lettre"] = code.lettre
            data["num"] = code.num
            data["lib"] = code.lib
            data["op"] = code.op
            data["code1"] = total1
            data["code2"] = total2
            data["code0"] = code.id
            data["type"] = code.type
            data["sequence"] = code.sequence
            for rec in self:
                data["balance_id"] = rec.id
            actif.create(data)
        return True

    def generate_caf(self):
        actif = self.env['caf.fiscale.erp']
        bilan_actif = self.env['liasse.caf.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        for rec in self:
            rec.env.cr.execute("delete from caf_fiscale_erp where balance_id=" + str(rec.id))
        for code in bilan_actif_obj:
            total2 = self.count_cell(code.code2)
            total1 = self.count_cell(code.code1)

            data = {}
            data["lettre"] = code.lettre
            data["num"] = code.num
            data["op"] = code.op
            data["lib"] = code.lib
            data["code1"] = total1
            data["code2"] = total2
            data["code0"] = code.id
            data["type"] = code.type
            data["sequence"] = code.sequence
            for rec in self:
                data["balance_id"] = rec.id
            actif.create(data)
        return True

    def generate_amort(self):
        actif = self.env['amort.fiscale.erp']
        bilan_actif = self.env['liasse.amort.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        for rec in self:
            rec.env.cr.execute("delete from amort_fiscale_erp where balance_id=" + str(rec.id))
        for code in bilan_actif_obj:
            total1 = self.count_init(code.code1)
            total2 = self.count_cell(code.code2)
            total4 = self.count_cell(code.code4)
            total3 = total1 + total2 - total4

            data = {}
            data["lib"] = code.lib
            data["code1"] = total1
            data["code2"] = total2
            data["code3"] = total3
            data["code4"] = total4
            data["code0"] = code.id
            data["type"] = code.type
            data["sequence"] = code.sequence
            for rec in self:
                data["balance_id"] = rec.id
            actif.create(data)
        return True

    def generate_provision(self):
        actif = self.env['provision.fiscale.erp']
        bilan_actif = self.env['liasse.provision.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        for rec in self:
            rec.env.cr.execute("delete from provision_fiscale_erp where balance_id=" + str(rec.id))
        for code in bilan_actif_obj:
            total1 = self.count_init(code.code1)
            total2 = self.count_cell(code.code2)
            total3 = self.count_cell(code.code3)
            total4 = self.count_cell(code.code4)
            total5 = self.count_cell(code.code5)
            total6 = self.count_cell(code.code6)
            total7 = self.count_cell(code.code7)

            total8 = total1 + total2 + total3 + total4 - total5 - total6 - total7
            total8 = abs(total8)

            data = {}
            data["lib"] = code.lib
            data["code1"] = total1
            data["code2"] = total2
            data["code3"] = total3
            data["code4"] = total4
            data["code5"] = total5
            data["code6"] = total6
            data["code7"] = total7
            data["code8"] = total8
            data["code0"] = code.id
            data["type"] = code.type
            data["sequence"] = code.sequence
            for rec in self:
                data["balance_id"] = rec.id
            actif.create(data)
        return True

    def generate_stock(self):
        actif = self.env['stock.fiscale.erp']
        bilan_actif = self.env['liasse.stock.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        for rec in self:
            rec.env.cr.execute("delete from stock_fiscale_erp where balance_id=" + str(rec.id))
        for code in bilan_actif_obj:
            total4 = self.count_cell(code.code4)
            total5 = self.count_cell(code.code5)
            total1 = self.count_cell(code.code1)
            total2 = self.count_cell(code.code2)

            total3 = total1 - total2
            total6 = total4 - total5
            total7 = total3 - total6

            data = {}
            data["lib"] = code.lib
            data["code1"] = total1
            data["code2"] = total2
            data["code3"] = total3
            data["code4"] = total4
            data["code5"] = total5
            data["code6"] = total6
            data["code7"] = total7
            data["code0"] = code.id
            data["type"] = code.type
            data["sequence"] = code.sequence
            for rec in self:
                data["balance_id"] = rec.id
            actif.create(data)
        return True

    def generate_fusion(self):
        actif = self.env['fusion.fiscale.erp']
        bilan_actif = self.env['liasse.fusion.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        for rec in self:
            rec.env.cr.execute("delete from fusion_fiscale_erp where balance_id=" + str(rec.id))
        for code in bilan_actif_obj:
            total1 = 0
            total2 = 0
            total3 = 0
            total4 = 0
            total5 = 0
            total6 = 0
            total7 = 0
            total8 = ''

            data = {}
            data["lib"] = code.lib
            data["code1"] = total1
            data["code2"] = total2
            data["code3"] = total3
            data["code4"] = total4
            data["code5"] = total5
            data["code6"] = total6
            data["code7"] = total7
            data["code8"] = total8
            data["code0"] = code.id
            data["type"] = code.type
            data["sequence"] = code.sequence
            for rec in self:
                data["balance_id"] = rec.id
            actif.create(data)
        return True

    def edi_actif(self):
        actif = self.env['bilan.actif.fiscale.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            actif_ids = actif.search([('balance_id', '=', rec.id)])
            actif_obj = actif_ids
            for ac in actif_obj:
                ac.code0.code1.write({'valeur': ac.code1})
                ac.code0.code2.write({'valeur': ac.code2})
                ac.code0.code3.write({'valeur': ac.code3})
                ac.code0.code4.write({'valeur': ac.code4})
        return True

    def edi_passif(self):
        actif = self.env['bilan.passif.fiscale.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            actif_ids = actif.search([('balance_id', '=', rec.id)])
            actif_obj = actif_ids
            for ac in actif_obj:
                ac.code0.code1.write({'valeur': ac.code1})
                ac.code0.code2.write({'valeur': ac.code2})
        return True

    def edi_cpc(self):
        actif = self.env['cpc.fiscale.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            actif_ids = actif.search([('balance_id', '=', rec.id)])
            actif_obj = actif_ids
            for ac in actif_obj:
                ac.code0.code1.write({'valeur': ac.code1})
                ac.code0.code2.write({'valeur': ac.code2})
                ac.code0.code3.write({'valeur': ac.code3})
                ac.code0.code4.write({'valeur': ac.code4})
        return True

    def edi_det_cpc(self):
        extra_tab = self.env["liasse.extra.field.erp"]
        extra_tab_ids = extra_tab.search([], limit=1)
        extra_tab_obj = extra_tab_ids
        actif = self.env['det.cpc.fiscale.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            actif_ids = actif.search([('balance_id', '=', rec.id)])
            actif_obj = actif_ids
            for ex in extra_tab_obj:
                ex.code0cpc.write({'valeur': rec.date_end})
            for ac in actif_obj:
                ac.code0.code1.write({'valeur': ac.code1})
                ac.code0.code2.write({'valeur': ac.code2})
        return True

    def edi_tfr(self):
        actif = self.env['tfr.fiscale.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            actif_ids = actif.search([('balance_id', '=', rec.id)])
            actif_obj = actif_ids
            for ac in actif_obj:
                ac.code0.code1.write({'valeur': ac.code1})
                ac.code0.code2.write({'valeur': ac.code2})
        return True

    def edi_caf(self):
        actif = self.env['caf.fiscale.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            actif_ids = actif.search([('balance_id', '=', rec.id)])
            actif_obj = actif_ids
            for ac in actif_obj:
                ac.code0.code1.write({'valeur': ac.code1})
                ac.code0.code2.write({'valeur': ac.code2})
        return True

    def edi_amort(self):
        actif = self.env['amort.fiscale.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            actif_ids = actif.search([('balance_id', '=', rec.id)])
            actif_obj = actif_ids
            for ac in actif_obj:
                ac.code0.code1.write({'valeur': ac.code1})
                ac.code0.code2.write({'valeur': ac.code2})
                ac.code0.code3.write({'valeur': ac.code3})
                ac.code0.code4.write({'valeur': ac.code4})
        return True

    def edi_provision(self):
        extra_tab = self.env["liasse.extra.field.erp"]
        extra_tab_ids = extra_tab.search([], limit=1)
        extra_tab_obj = extra_tab_ids
        actif = self.env['provision.fiscale.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            actif_ids = actif.search([('balance_id', '=', rec.id)])
            actif_obj = actif_ids
            for ex in extra_tab_obj:
                ex.code1prov.write({'valeur': rec.date_end})
            for ac in actif_obj:
                ac.code0.code1.write({'valeur': ac.code1})
                ac.code0.code2.write({'valeur': ac.code2})
                ac.code0.code3.write({'valeur': ac.code3})
                ac.code0.code4.write({'valeur': ac.code4})
                ac.code0.code5.write({'valeur': ac.code5})
                ac.code0.code6.write({'valeur': ac.code6})
                ac.code0.code7.write({'valeur': ac.code7})
                ac.code0.code8.write({'valeur': ac.code8})
        return True

    def edi_stock(self):
        actif = self.env['stock.fiscale.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            actif_ids = actif.search([('balance_id', '=', rec.id)])
            actif_obj = actif_ids
            for ac in actif_obj:
                ac.code0.code1.write({'valeur': ac.code1})
                ac.code0.code2.write({'valeur': ac.code2})
                ac.code0.code3.write({'valeur': ac.code3})
                ac.code0.code4.write({'valeur': ac.code4})
                ac.code0.code5.write({'valeur': ac.code5})
                ac.code0.code6.write({'valeur': ac.code6})
                ac.code0.code7.write({'valeur': ac.code7})
        return True

    def edi_fusion(self):
        extra_tab = self.env["liasse.extra.field.erp"]
        extra_tab_ids = extra_tab.search([], limit=1)
        extra_tab_obj = extra_tab_ids
        actif = self.env['fusion.fiscale.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            actif_ids = actif.search([('balance_id', '=', rec.id)])
            actif_obj = actif_ids
            for ex in extra_tab_obj:
                ex.code2fusion.write({'valeur': rec.date_end})
            for ac in actif_obj:
                ac.code0.code1.write({'valeur': ac.code1})
                ac.code0.code2.write({'valeur': ac.code2})
                ac.code0.code3.write({'valeur': ac.code3})
                ac.code0.code4.write({'valeur': ac.code4})
                ac.code0.code5.write({'valeur': ac.code5})
                ac.code0.code6.write({'valeur': ac.code6})
                ac.code0.code7.write({'valeur': ac.code7})
                ac.code0.code8.write({'valeur': ac.code8})
        return True

    def edi_credit_bail(self):
        credit_bail_data = self.env['credi.bail.erp']
        credit_bail_edi = self.env['liasse.credit.bail.erp']
        code_conf = self.env['liasse.code.erp']
        code_conf_valeur = self.env['liasse.code.line.erp']
        for rec in self:
            credit_bail_data_ids = credit_bail_data.search([('balance_id', '=', rec.id)])
            credit_bail_edi_ids = credit_bail_edi.search([], limit=1)
            credit_bail_data_obj = credit_bail_data_ids
            credit_bail_edi_obj = credit_bail_edi_ids
            if credit_bail_edi_obj:
                credit_bail_edi_obj.extra_field_clos.write({'valeur': rec.date_end})
                if credit_bail_edi_obj.credit_bail_ids:
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.credit_bail_ids[0].code0.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.credit_bail_ids[0].code1.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.credit_bail_ids[0].code2.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.credit_bail_ids[0].code3.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.credit_bail_ids[0].code4.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.credit_bail_ids[0].code5.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.credit_bail_ids[0].code6.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.credit_bail_ids[0].code7.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.credit_bail_ids[0].code8.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.credit_bail_ids[0].code9.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.credit_bail_ids[0].code10.id))
            row = 1
            for data in credit_bail_data_obj:
                data1 = data.rubrique
                data2 = data.date_first_ech
                data3 = data.duree_contrat
                data4 = data.val_estime
                data5 = data.duree_theo
                data6 = data.cumul_prec
                data7 = data.montant_rev
                data8 = data.rev_moins
                data9 = data.rev_plus
                data10 = data.prix_achat
                data11 = data.observation
                if credit_bail_edi_obj:
                    if credit_bail_edi_obj.credit_bail_ids:
                        code_conf_valeur.create({'valeur': data1, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.credit_bail_ids[0].code0.id})
                        code_conf_valeur.create({'valeur': data2, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.credit_bail_ids[0].code1.id})
                        code_conf_valeur.create({'valeur': data3, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.credit_bail_ids[0].code2.id})
                        code_conf_valeur.create({'valeur': data4, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.credit_bail_ids[0].code3.id})
                        code_conf_valeur.create({'valeur': data5, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.credit_bail_ids[0].code4.id})
                        code_conf_valeur.create({'valeur': data6, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.credit_bail_ids[0].code5.id})
                        code_conf_valeur.create({'valeur': data7, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.credit_bail_ids[0].code6.id})
                        code_conf_valeur.create({'valeur': data8, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.credit_bail_ids[0].code7.id})
                        code_conf_valeur.create({'valeur': data9, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.credit_bail_ids[0].code8.id})
                        code_conf_valeur.create({'valeur': data10, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.credit_bail_ids[0].code9.id})
                        code_conf_valeur.create({'valeur': data11, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.credit_bail_ids[0].code10.id})
                    else:
                        break
                row += 1

        return True

    def edi_pm_value(self):
        pm_value_data = self.env['pm.value.erp']
        pm_value_edi = self.env['liasse.pm.value.erp']
        code_conf = self.env['liasse.code.erp']
        code_conf_valeur = self.env['liasse.code.line.erp']
        for rec in self:
            credit_bail_data_ids = pm_value_data.search([('balance_id', '=', rec.id)])
            credit_bail_edi_ids = pm_value_edi.search([], limit=1)
            credit_bail_data_obj = credit_bail_data_ids
            credit_bail_edi_obj = credit_bail_edi_ids
            if credit_bail_edi_obj:
                credit_bail_edi_obj[0].extra_field_clos.write({'valeur': rec.date_end})
                credit_bail_edi_obj[0].compte_princ.write({'valeur': rec.pm_compte_princ})
                credit_bail_edi_obj[0].montant_brut.write({'valeur': rec.pm_montant_brut})
                credit_bail_edi_obj[0].amort_cumul.write({'valeur': rec.pm_amort_cumul})
                credit_bail_edi_obj[0].val_net_amort.write({'valeur': rec.pm_val_net_amort})
                credit_bail_edi_obj[0].prod_cess.write({'valeur': rec.pm_prod_cess})
                credit_bail_edi_obj[0].plus_value.write({'valeur': rec.pm_plus_value})
                credit_bail_edi_obj[0].moins_value.write({'valeur': rec.pm_moins_value})

                if credit_bail_edi_obj.pm_val_ids:
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.pm_val_ids[0].code0.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.pm_val_ids[0].code1.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.pm_val_ids[0].code2.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.pm_val_ids[0].code3.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.pm_val_ids[0].code4.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.pm_val_ids[0].code5.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.pm_val_ids[0].code6.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.pm_val_ids[0].code7.id))
            row = 1
            for data in credit_bail_data_obj:
                data1 = data.date_cession
                data2 = data.compte_princ
                data3 = data.montant_brut
                data4 = data.amort_cumul
                data5 = data.val_net_amort
                data6 = data.prod_cess
                data7 = data.plus_value
                data8 = data.moins_value

                if credit_bail_edi_obj:
                    if credit_bail_edi_obj.pm_val_ids:
                        code_conf_valeur.create({'valeur': data1, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.pm_val_ids[0].code0.id})
                        code_conf_valeur.create({'valeur': data2, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.pm_val_ids[0].code1.id})
                        code_conf_valeur.create({'valeur': data3, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.pm_val_ids[0].code2.id})
                        code_conf_valeur.create({'valeur': data4, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.pm_val_ids[0].code3.id})
                        code_conf_valeur.create({'valeur': data5, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.pm_val_ids[0].code4.id})
                        code_conf_valeur.create({'valeur': data6, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.pm_val_ids[0].code5.id})
                        code_conf_valeur.create({'valeur': data7, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.pm_val_ids[0].code6.id})
                        code_conf_valeur.create({'valeur': data8, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.pm_val_ids[0].code7.id})
                    else:
                        break
                row += 1

        return True

    def edi_dotation(self):
        pm_value_data = self.env['dotation.amort.erp']
        pm_value_edi = self.env['liasse.dotation.erp']
        code_conf = self.env['liasse.code.erp']
        code_conf_valeur = self.env['liasse.code.line.erp']
        for rec in self:
            credit_bail_data_ids = pm_value_data.search([('balance_id', '=', rec.id)])
            credit_bail_edi_ids = pm_value_edi.search([], limit=1)
            credit_bail_data_obj = credit_bail_data_ids
            credit_bail_edi_obj = credit_bail_edi_ids
            if credit_bail_edi_obj:
                credit_bail_edi_obj.clos.write({'valeur': rec.date_end})
                credit_bail_edi_obj[0].date_from.write({'valeur': rec.date_start})
                credit_bail_edi_obj[0].date_end.write({'valeur': rec.date_end})
                credit_bail_edi_obj[0].montant_global.write({'valeur': rec.montant_dot})
                credit_bail_edi_obj[0].val_acq.write({'valeur': rec.val_acq})
                credit_bail_edi_obj[0].val_compt.write({'valeur': rec.val_compt})
                credit_bail_edi_obj[0].amort_ant.write({'valeur': rec.amort_ant})
                credit_bail_edi_obj[0].amort_ded_et.write({'valeur': rec.amort_ded_et})
                credit_bail_edi_obj[0].amort_ded_e.write({'valeur': rec.amort_ded_e})
                credit_bail_edi_obj[0].amort_fe.write({'valeur': rec.amort_fe})

                if credit_bail_edi_obj.dotation_line_ids:
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.dotation_line_ids[0].code0.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.dotation_line_ids[0].code1.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.dotation_line_ids[0].code2.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.dotation_line_ids[0].code3.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.dotation_line_ids[0].code4.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.dotation_line_ids[0].code5.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.dotation_line_ids[0].code6.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.dotation_line_ids[0].code7.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.dotation_line_ids[0].code8.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.dotation_line_ids[0].code9.id))
            row = 1
            for data in credit_bail_data_obj:
                data1 = data.code0
                data2 = data.code1
                data3 = data.code2
                data4 = data.code3
                data5 = data.code4
                data6 = data.code5
                data7 = data.code6
                data8 = data.code7
                data9 = data.code8
                data10 = data.code9

                if credit_bail_edi_obj:
                    if credit_bail_edi_obj.dotation_line_ids:
                        code_conf_valeur.create({'valeur': data1, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.dotation_line_ids[0].code0.id})
                        code_conf_valeur.create({'valeur': data2, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.dotation_line_ids[0].code1.id})
                        code_conf_valeur.create({'valeur': data3, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.dotation_line_ids[0].code2.id})
                        code_conf_valeur.create({'valeur': data4, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.dotation_line_ids[0].code3.id})
                        code_conf_valeur.create({'valeur': data5, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.dotation_line_ids[0].code4.id})
                        code_conf_valeur.create({'valeur': data6, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.dotation_line_ids[0].code5.id})
                        code_conf_valeur.create({'valeur': data7, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.dotation_line_ids[0].code6.id})
                        code_conf_valeur.create({'valeur': data8, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.dotation_line_ids[0].code7.id})
                        code_conf_valeur.create({'valeur': data9, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.dotation_line_ids[0].code8.id})
                        code_conf_valeur.create({'valeur': data10, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.dotation_line_ids[0].code9.id})
                    else:
                        break
                row += 1

        return True

    def edi_titre_particp(self):
        pm_value_data = self.env['titre.particip.erp']
        pm_value_edi = self.env['liasse.titre.particip.erp']
        code_conf = self.env['liasse.code.erp']
        code_conf_valeur = self.env['liasse.code.line.erp']
        for rec in self:
            credit_bail_data_ids = pm_value_data.search([('balance_id', '=', rec.id)])
            credit_bail_edi_ids = pm_value_edi.search([], limit=1)
            credit_bail_data_obj = credit_bail_data_ids
            credit_bail_edi_obj = credit_bail_edi_ids
            if credit_bail_edi_obj:
                credit_bail_edi_obj[0].code2.write({'valeur': rec.tp_capit_social})
                credit_bail_edi_obj[0].code3.write({'valeur': rec.tp_particip_cap})
                credit_bail_edi_obj[0].code4.write({'valeur': rec.tp_prix_global})
                credit_bail_edi_obj[0].code5.write({'valeur': rec.tp_val_compt})
                credit_bail_edi_obj[0].code6.write({'valeur': rec.tp_extr_date})
                credit_bail_edi_obj[0].code7.write({'valeur': rec.tp_extr_situation})
                credit_bail_edi_obj[0].code8.write({'valeur': rec.tp_extr_resultat})
                credit_bail_edi_obj[0].code9.write({'valeur': rec.tp_prod_inscrit})

                if credit_bail_edi_obj.titre_particip_ids:
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.titre_particip_ids[0].code0.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.titre_particip_ids[0].code1.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.titre_particip_ids[0].code2.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.titre_particip_ids[0].code3.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.titre_particip_ids[0].code4.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.titre_particip_ids[0].code5.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.titre_particip_ids[0].code6.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.titre_particip_ids[0].code7.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.titre_particip_ids[0].code8.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.titre_particip_ids[0].code9.id))
            row = 1
            for data in credit_bail_data_obj:
                data1 = data.raison_soc
                data2 = data.sect_activity
                data3 = data.capit_social
                data4 = data.particip_cap
                data5 = data.prix_global
                data6 = data.val_compt
                data7 = data.extr_date
                data8 = data.extr_situation
                data9 = data.extr_resultat
                data10 = data.prod_inscrit

                if credit_bail_edi_obj:
                    if credit_bail_edi_obj.titre_particip_ids:
                        code_conf_valeur.create({'valeur': data1, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.titre_particip_ids[
                                                     0].code0.id})
                        code_conf_valeur.create({'valeur': data2, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.titre_particip_ids[
                                                     0].code1.id})
                        code_conf_valeur.create({'valeur': data3, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.titre_particip_ids[
                                                     0].code2.id})
                        code_conf_valeur.create({'valeur': data4, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.titre_particip_ids[
                                                     0].code3.id})
                        code_conf_valeur.create({'valeur': data5, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.titre_particip_ids[
                                                     0].code4.id})
                        code_conf_valeur.create({'valeur': data6, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.titre_particip_ids[
                                                     0].code5.id})
                        code_conf_valeur.create({'valeur': data7, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.titre_particip_ids[
                                                     0].code6.id})
                        code_conf_valeur.create({'valeur': data8, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.titre_particip_ids[
                                                     0].code7.id})
                        code_conf_valeur.create({'valeur': data9, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.titre_particip_ids[
                                                     0].code8.id})
                        code_conf_valeur.create({'valeur': data10, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.titre_particip_ids[
                                                     0].code9.id})
                    else:
                        break
                row += 1

        return True

    def edi_repart_cs(self):
        pm_value_data = self.env['repart.cs.erp']
        pm_value_edi = self.env['liasse.repart.cs.erp']
        code_conf = self.env['liasse.code.erp']
        code_conf_valeur = self.env['liasse.code.line.erp']
        for rec in self:
            credit_bail_data_ids = pm_value_data.search([('balance_id', '=', rec.id)])
            credit_bail_edi_ids = pm_value_edi.search([], limit=1)
            credit_bail_data_obj = credit_bail_data_ids
            credit_bail_edi_obj = credit_bail_edi_ids
            if credit_bail_edi_obj:
                credit_bail_edi_obj[0].montant_capital.write({'valeur': rec.montant_rcs})
                if credit_bail_edi_obj.repart_cs_ids:
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.repart_cs_ids[0].code0.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.repart_cs_ids[0].code1.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.repart_cs_ids[0].code2.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.repart_cs_ids[0].code3.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.repart_cs_ids[0].code4.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.repart_cs_ids[0].code5.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.repart_cs_ids[0].code6.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.repart_cs_ids[0].code7.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.repart_cs_ids[0].code8.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.repart_cs_ids[0].code9.id))
            row = 1
            for data in credit_bail_data_obj:
                data1 = data.name
                data2 = data.id_fisc
                data3 = data.cin
                data4 = data.adress
                data5 = data.number_prec
                data6 = data.number_actual
                data7 = data.val_nom
                data8 = data.val_sousc
                data9 = data.val_appele
                data10 = data.val_lib

                if credit_bail_edi_obj:
                    if credit_bail_edi_obj.repart_cs_ids:
                        code_conf_valeur.create({'valeur': data1, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.repart_cs_ids[0].code0.id})
                        code_conf_valeur.create({'valeur': data2, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.repart_cs_ids[0].code1.id})
                        code_conf_valeur.create({'valeur': data3, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.repart_cs_ids[0].code2.id})
                        code_conf_valeur.create({'valeur': data4, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.repart_cs_ids[0].code3.id})
                        code_conf_valeur.create({'valeur': data5, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.repart_cs_ids[0].code4.id})
                        code_conf_valeur.create({'valeur': data6, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.repart_cs_ids[0].code5.id})
                        code_conf_valeur.create({'valeur': data7, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.repart_cs_ids[0].code6.id})
                        code_conf_valeur.create({'valeur': data8, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.repart_cs_ids[0].code7.id})
                        code_conf_valeur.create({'valeur': data9, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.repart_cs_ids[0].code8.id})
                        code_conf_valeur.create({'valeur': data10, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.repart_cs_ids[0].code9.id})
                    else:
                        break
                row += 1

        return True

    def edi_interets(self):
        in_data = self.env['interets.erp']
        in_edi = self.env['liasse.interets.erp']
        code_conf = self.env['liasse.code.erp']
        code_conf_valeur = self.env['liasse.code.line.erp']
        for rec in self:
            ina_data_ids = in_data.search([("type", "=", "0"), ('balance_id', '=', rec.id)])
            int_data_ids = in_data.search([("type", "=", "1"), ('balance_id', '=', rec.id)])
            in_edi_ids = in_edi.search([], limit=1)
            ina_data_obj = ina_data_ids
            int_data_obj = int_data_ids
            in_edi_obj = in_edi_ids
            if in_edi_obj:
                in_edi_obj.code0.write({'valeur': rec.date_end})
                in_edi_obj.code1.write({'valeur': rec.in_mont_pretl})
                in_edi_obj.code2.write({'valeur': rec.in_charge_global})
                in_edi_obj.code3.write({'valeur': rec.in_remb_princ})
                in_edi_obj.code4.write({'valeur': rec.in_remb_inter})
                in_edi_obj.code5.write({'valeur': rec.in_remb_actual_princ})
                in_edi_obj.code6.write({'valeur': rec.in_remb_actual_inter})

                if in_edi_obj.interets_associe:
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code0.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code1.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code2.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code3.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code4.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code5.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code6.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code7.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code8.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code9.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code10.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code11.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        in_edi_obj.interets_associe[0].code12.id))
                if in_edi_obj.interets_tier:
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code0.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code1.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code2.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code3.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code4.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code5.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code6.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code7.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code8.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code9.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code10.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code11.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(in_edi_obj.interets_tier[0].code12.id))
            row = 1
            for data in ina_data_obj:
                data1 = data.name
                data2 = data.adress
                data3 = data.cin
                data4 = data.mont_pretl
                data5 = data.date_pret
                data6 = data.duree_mois
                data7 = data.taux_inter
                data8 = data.charge_global
                data9 = data.remb_princ
                data10 = data.remb_inter
                data11 = data.remb_actual_princ
                data12 = data.remb_actual_inter
                data13 = data.observation

                if in_edi_obj:
                    if in_edi_obj.interets_associe:
                        code_conf_valeur.create({'valeur': data1, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code0.id})
                        code_conf_valeur.create({'valeur': data2, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code1.id})
                        code_conf_valeur.create({'valeur': data3, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code2.id})
                        code_conf_valeur.create({'valeur': data4, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code3.id})
                        code_conf_valeur.create({'valeur': data5, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code4.id})
                        code_conf_valeur.create({'valeur': data6, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code5.id})
                        code_conf_valeur.create({'valeur': data7, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code6.id})
                        code_conf_valeur.create({'valeur': data8, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code7.id})
                        code_conf_valeur.create({'valeur': data9, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code8.id})
                        code_conf_valeur.create({'valeur': data10, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code9.id})
                        code_conf_valeur.create({'valeur': data11, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code10.id})
                        code_conf_valeur.create({'valeur': data12, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code11.id})
                        code_conf_valeur.create({'valeur': data13, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_associe[0].code12.id})
                    else:
                        break
                row += 1

            row = 1
            for data in int_data_obj:
                data1 = data.name
                data2 = data.adress
                data3 = data.cin
                data4 = data.mont_pretl
                data5 = data.date_pret
                data6 = data.duree_mois
                data7 = data.taux_inter
                data8 = data.charge_global
                data9 = data.remb_princ
                data10 = data.remb_inter
                data11 = data.remb_actual_princ
                data12 = data.remb_actual_inter
                data13 = data.observation

                if in_edi_obj:
                    if in_edi_obj.interets_tier:
                        code_conf_valeur.create({'valeur': data1, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code0.id})
                        code_conf_valeur.create({'valeur': data2, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code1.id})
                        code_conf_valeur.create({'valeur': data3, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code2.id})
                        code_conf_valeur.create({'valeur': data4, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code3.id})
                        code_conf_valeur.create({'valeur': data5, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code4.id})
                        code_conf_valeur.create({'valeur': data6, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code5.id})
                        code_conf_valeur.create({'valeur': data7, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code6.id})
                        code_conf_valeur.create({'valeur': data8, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code7.id})
                        code_conf_valeur.create({'valeur': data9, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code8.id})
                        code_conf_valeur.create({'valeur': data10, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code9.id})
                        code_conf_valeur.create({'valeur': data11, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code10.id})
                        code_conf_valeur.create({'valeur': data12, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code11.id})
                        code_conf_valeur.create({'valeur': data13, 'ligne': row,
                                                 'code_id': in_edi_obj.interets_tier[0].code12.id})
                    else:
                        break
                row += 1

        return True

    def edi_beaux(self):
        pm_value_data = self.env['beaux.erp']
        pm_value_edi = self.env['liasse.beaux.erp']
        code_conf = self.env['liasse.code.erp']
        code_conf_valeur = self.env['liasse.code.line.erp']
        for rec in self:
            credit_bail_data_ids = pm_value_data.search([('balance_id', '=', rec.id)])
            credit_bail_edi_ids = pm_value_edi.search([], limit=1)
            credit_bail_data_obj = credit_bail_data_ids
            credit_bail_edi_obj = credit_bail_edi_ids
            if credit_bail_edi_obj:
                credit_bail_edi_obj[0].code0.write({'valeur': rec.bx_mont_pretl})
                credit_bail_edi_obj[0].code1.write({'valeur': rec.bx_charge_global})
                if credit_bail_edi_obj.beaux_ids:
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.beaux_ids[0].code0.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.beaux_ids[0].code1.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.beaux_ids[0].code2.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.beaux_ids[0].code3.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.beaux_ids[0].code4.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.beaux_ids[0].code5.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.beaux_ids[0].code6.id))
                    self.env.cr.execute('delete from liasse_code_line_erp where code_id=' + str(
                        credit_bail_edi_obj.beaux_ids[0].code7.id))
            row = 1
            for data in credit_bail_data_obj:
                data1 = data.nature
                data2 = data.lieu
                data3 = data.name
                data4 = data.date_loc
                data5 = data.mont_annuel
                data6 = data.mont_loyer
                data7 = data.nature_bail
                data8 = data.nature_periode

                if credit_bail_edi_obj:
                    if credit_bail_edi_obj.beaux_ids:
                        code_conf_valeur.create({'valeur': data1, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.beaux_ids[0].code0.id})
                        code_conf_valeur.create({'valeur': data2, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.beaux_ids[0].code1.id})
                        code_conf_valeur.create({'valeur': data3, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.beaux_ids[0].code2.id})
                        code_conf_valeur.create({'valeur': data4, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.beaux_ids[0].code3.id})
                        code_conf_valeur.create({'valeur': data5, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.beaux_ids[0].code4.id})
                        code_conf_valeur.create({'valeur': data6, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.beaux_ids[0].code5.id})
                        code_conf_valeur.create({'valeur': data7, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.beaux_ids[0].code6.id})
                        code_conf_valeur.create({'valeur': data8, 'ligne': row,
                                                 'code_id': credit_bail_edi_obj.beaux_ids[0].code7.id})
                    else:
                        break
                row += 1

        return True

    def edi_passage(self):
        ps_data = self.env['passage.erp']
        ps_edi = self.env['liasse.passage.erp']
        code_conf = self.env['liasse.code.erp']
        code_conf_valeur = self.env['liasse.code.line.erp']
        for rec in self:
            psrfc_data_ids = ps_data.search([("type", "=", "0"), ('balance_id', '=', rec.id)])
            psrfnc_data_ids = ps_data.search([("type", "=", "1"), ('balance_id', '=', rec.id)])
            psdfc_data_ids = ps_data.search([("type", "=", "2"), ('balance_id', '=', rec.id)])
            psdfnc_data_ids = ps_data.search([("type", "=", "3"), ('balance_id', '=', rec.id)])
            ps_edi_ids = ps_edi.search([], limit=1)
            psrfc_data_obj = psrfc_data_ids
            psrfnc_data_obj = psrfnc_data_ids
            psdfc_data_obj = psdfc_data_ids
            psdfnc_data_obj = psdfnc_data_ids
            ps_edi_obj = ps_edi_ids
            if ps_edi_obj:
                ps_edi_obj[0].code0.write({'valeur': rec.p_benifice_p})
                ps_edi_obj[0].code1.write({'valeur': rec.p_benifice_m})
                ps_edi_obj[0].code2.write({'valeur': rec.p_perte_p})
                ps_edi_obj[0].code3.write({'valeur': rec.p_perte_m})
                ps_edi_obj[0].code4.write({'valeur': rec.p_total_montantp})
                ps_edi_obj[0].code5.write({'valeur': rec.p_total_montantm})
                ps_edi_obj[0].code6.write({'valeur': rec.p_benificebp})
                ps_edi_obj[0].code7.write({'valeur': rec.p_benificebm})
                ps_edi_obj[0].code8.write({'valeur': rec.p_deficitfp})
                ps_edi_obj[0].code9.write({'valeur': rec.p_deficitfm})
                ps_edi_obj[0].code10.write({'valeur': rec.p_exo4p})
                # code_conf.write(ps_edi_obj[0].code11.id,{'valeur':rec.p_exo4m})
                ps_edi_obj[0].code12.write({'valeur': rec.p_exo3p})
                # code_conf.write(ps_edi_obj[0].code13.id,{'valeur':rec.p_exo3m})
                ps_edi_obj[0].code14.write({'valeur': rec.p_exo2p})
                # code_conf.write(ps_edi_obj[0].code15.id,{'valeur':rec.p_exo2m})
                ps_edi_obj[0].code16.write({'valeur': rec.p_exo1p})
                # code_conf.write(ps_edi_obj[0].code17.id,{'valeur':rec.p_exo1m})
                ps_edi_obj[0].code18.write({'valeur': rec.p_benificenfp})
                ps_edi_obj[0].code19.write({'valeur': rec.p_benificenfm})
                ps_edi_obj[0].code20.write({'valeur': rec.p_deficitnfp})
                ps_edi_obj[0].code21.write({'valeur': rec.p_deficitnfm})
                ps_edi_obj[0].code22.write({'valeur': rec.p_cumulafdm})
                ps_edi_obj[0].code23.write({'valeur': rec.p_exo4cumulp})
                ps_edi_obj[0].code24.write({'valeur': rec.p_exo3cumulp})
                ps_edi_obj[0].code25.write({'valeur': rec.p_exo2cumulp})
                ps_edi_obj[0].code26.write({'valeur': rec.p_exo1cumulp})

                if ps_edi_obj.passages_rfc:
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(ps_edi_obj.passages_rfc[0].code0.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(ps_edi_obj.passages_rfc[0].code1.id))
                if ps_edi_obj.passages_rfnc:
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(ps_edi_obj.passages_rfnc[0].code0.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(ps_edi_obj.passages_rfnc[0].code1.id))
                if ps_edi_obj.passages_dfc:
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(ps_edi_obj.passages_dfc[0].code0.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(ps_edi_obj.passages_dfc[0].code2.id))

                if ps_edi_obj.passages_dfnc:
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(ps_edi_obj.passages_dfnc[0].code0.id))
                    self.env.cr.execute(
                        'delete from liasse_code_line_erp where code_id=' + str(ps_edi_obj.passages_dfnc[0].code2.id))
            row = 1
            for data in psrfc_data_obj:
                data1 = data.name
                data2 = data.montant1
                data3 = data.montant2

                if ps_edi_obj:
                    if ps_edi_obj.passages_rfc:
                        code_conf_valeur.create({'valeur': data1, 'ligne': row,
                                                 'code_id': ps_edi_obj.passages_rfc[0].code0.id})
                        code_conf_valeur.create({'valeur': data2, 'ligne': row,
                                                 'code_id': ps_edi_obj.passages_rfc[0].code1.id})
                    else:
                        break
                row += 1

            row = 1
            for data in psrfnc_data_obj:
                data1 = data.name
                data2 = data.montant1
                data3 = data.montant2

                if ps_edi_obj:
                    if ps_edi_obj.passages_rfnc:
                        code_conf_valeur.create({'valeur': data1, 'ligne': row,
                                                 'code_id': ps_edi_obj.passages_rfnc[0].code0.id})
                        code_conf_valeur.create({'valeur': data2, 'ligne': row,
                                                 'code_id': ps_edi_obj.passages_rfnc[0].code1.id})
                    else:
                        break
                row += 1

            row = 1
            for data in psdfc_data_obj:
                data1 = data.name
                data2 = data.montant1
                data3 = data.montant2

                if ps_edi_obj:
                    if ps_edi_obj.passages_dfc:
                        code_conf_valeur.create({'valeur': data1, 'ligne': row,
                                                 'code_id': ps_edi_obj.passages_dfc[0].code0.id})
                        code_conf_valeur.create({'valeur': data3, 'ligne': row,
                                                 'code_id': ps_edi_obj.passages_dfc[0].code2.id})
                    else:
                        break
                row += 1

            for data in psdfnc_data_obj:
                data1 = data.name
                data2 = data.montant1
                data3 = data.montant2

                if ps_edi_obj:
                    if ps_edi_obj.passages_dfnc:
                        code_conf_valeur.create({'valeur': data1, 'ligne': row,
                                                 'code_id': ps_edi_obj.passages_dfnc[0].code0.id})
                        code_conf_valeur.create({'valeur': data3, 'ligne': row,
                                                 'code_id': ps_edi_obj.passages_dfnc[0].code2.id})
                    else:
                        break
                row += 1

        return True

    def edi_encouragement(self):
        affect = self.env['liasse.encour.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            affect_edi_ids = affect.search([], limit=1)
            affect_edi_obj = affect_edi_ids
            if affect_edi_obj:
                affect_edi_obj[0].code0.write({'valeur': rec.vente_imp_ep})
                affect_edi_obj[0].code1.write({'valeur': rec.vente_imp_epi})
                affect_edi_obj[0].code2.write({'valeur': rec.vente_imp_ept})
                affect_edi_obj[0].code3.write({'valeur': rec.vente_ex100_ep})
                affect_edi_obj[0].code4.write({'valeur': rec.vente_ex100_epi})
                affect_edi_obj[0].code5.write({'valeur': rec.vente_ex100_ept})
                affect_edi_obj[0].code6.write({'valeur': rec.vente_ex50_ep})
                affect_edi_obj[0].code7.write({'valeur': rec.vente_ex50_epi})
                affect_edi_obj[0].code8.write({'valeur': rec.vente_ex50_ept})
                affect_edi_obj[0].code9.write({'valeur': rec.vente_li_ep})
                affect_edi_obj[0].code10.write({'valeur': rec.vente_li_epi})
                affect_edi_obj[0].code11.write({'valeur': rec.vente_li_ept})
                affect_edi_obj[0].code12.write({'valeur': rec.vente_lex100_ep})
                affect_edi_obj[0].code13.write({'valeur': rec.vente_lex100_epi})
                affect_edi_obj[0].code14.write({'valeur': rec.vente_lex100_ept})
                affect_edi_obj[0].code15.write({'valeur': rec.vente_lex50_ep})
                affect_edi_obj[0].code16.write({'valeur': rec.vente_lex50_epi})
                affect_edi_obj[0].code17.write({'valeur': rec.vente_lex50_ept})
                affect_edi_obj[0].code18.write({'valeur': rec.pres_imp_ep})
                affect_edi_obj[0].code19.write({'valeur': rec.pres_imp_epi})
                affect_edi_obj[0].code20.write({'valeur': rec.pres_imp_ept})
                affect_edi_obj[0].code21.write({'valeur': rec.pres_ex100_ep})
                affect_edi_obj[0].code22.write({'valeur': rec.pres_ex100_epi})
                affect_edi_obj[0].code23.write({'valeur': rec.pres_ex100_ept})
                affect_edi_obj[0].code24.write({'valeur': rec.pres_ex50_ep})
                affect_edi_obj[0].code25.write({'valeur': rec.pres_ex50_epi})
                affect_edi_obj[0].code26.write({'valeur': rec.pres_ex50_ept})
                affect_edi_obj[0].code27.write({'valeur': rec.prod_acc_ep})
                affect_edi_obj[0].code28.write({'valeur': rec.prod_acc_epi})
                affect_edi_obj[0].code29.write({'valeur': rec.prod_acc_ept})
                affect_edi_obj[0].code30.write({'valeur': rec.prod_sub_ep})
                affect_edi_obj[0].code31.write({'valeur': rec.prod_sub_epi})
                affect_edi_obj[0].code32.write({'valeur': rec.prod_sub_ept})
                affect_edi_obj[0].code33.write({'valeur': rec.sub_eq_ep})
                affect_edi_obj[0].code34.write({'valeur': rec.sub_eq_epi})
                affect_edi_obj[0].code35.write({'valeur': rec.sub_eq_ept})
                affect_edi_obj[0].code36.write({'valeur': rec.sub_imp_ep})
                affect_edi_obj[0].code37.write({'valeur': rec.sub_imp_epi})
                affect_edi_obj[0].code38.write({'valeur': rec.sub_imp_ept})
                affect_edi_obj[0].code39.write({'valeur': rec.sub_ex100_ep})
                affect_edi_obj[0].code40.write({'valeur': rec.sub_ex100_epi})
                affect_edi_obj[0].code41.write({'valeur': rec.sub_ex100_ept})
                affect_edi_obj[0].code42.write({'valeur': rec.sub_ex50_ep})
                affect_edi_obj[0].code43.write({'valeur': rec.sub_ex50_epi})
                affect_edi_obj[0].code44.write({'valeur': rec.sub_ex50_ept})
                affect_edi_obj[0].code45.write({'valeur': rec.taux_part_ep})
                affect_edi_obj[0].code46.write({'valeur': rec.taux_part_epi})
                affect_edi_obj[0].code47.write({'valeur': rec.taux_part_ept})
                affect_edi_obj[0].code48.write({'valeur': rec.profit_g_ep})
                affect_edi_obj[0].code49.write({'valeur': rec.profit_g_epi})
                affect_edi_obj[0].code50.write({'valeur': rec.profit_g_ept})
                affect_edi_obj[0].code51.write({'valeur': rec.profit_ex_ep})
                affect_edi_obj[0].code52.write({'valeur': rec.profit_ex_epi})
                affect_edi_obj[0].code53.write({'valeur': rec.profit_ex_ept})
                affect_edi_obj[0].code54.write({'valeur': rec.total_g_ep})
                affect_edi_obj[0].code55.write({'valeur': rec.total_g_epi})
                affect_edi_obj[0].code56.write({'valeur': rec.total_g_ept})
        return True

    def edi_immo(self):
        affect = self.env['liasse.immo.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            affect_edi_ids = affect.search([], limit=1)
            affect_edi_obj = affect_edi_ids
            if affect_edi_obj:
                affect_edi_obj[0].code0.write({'valeur': rec.immonv_mb})
                affect_edi_obj[0].code1.write({'valeur': rec.immonv_aug_acq})
                affect_edi_obj[0].code2.write({'valeur': rec.immonv_aug_pd})
                affect_edi_obj[0].code3.write({'valeur': rec.immonv_aug_vir})
                affect_edi_obj[0].code4.write({'valeur': rec.immonv_dim_cess})
                affect_edi_obj[0].code5.write({'valeur': rec.immonv_dim_ret})
                affect_edi_obj[0].code6.write({'valeur': rec.immonv_dim_vir})
                affect_edi_obj[0].code7.write({'valeur': rec.immonv_mbf})
                affect_edi_obj[0].code8.write({'valeur': rec.immoi_mb})
                affect_edi_obj[0].code9.write({'valeur': rec.immoi_aug_acq})
                affect_edi_obj[0].code10.write({'valeur': rec.immoi_aug_pd})
                affect_edi_obj[0].code11.write({'valeur': rec.immoi_aug_vir})
                affect_edi_obj[0].code12.write({'valeur': rec.immoi_dim_cess})
                affect_edi_obj[0].code13.write({'valeur': rec.immoi_dim_ret})
                affect_edi_obj[0].code14.write({'valeur': rec.immoi_dim_vir})
                affect_edi_obj[0].code15.write({'valeur': rec.immoi_mbf})
                affect_edi_obj[0].code16.write({'valeur': rec.immonc_mb})
                affect_edi_obj[0].code17.write({'valeur': rec.immonc_aug_acq})
                affect_edi_obj[0].code18.write({'valeur': rec.immonc_aug_pd})
                affect_edi_obj[0].code19.write({'valeur': rec.immonc_aug_vir})
                affect_edi_obj[0].code20.write({'valeur': rec.immonc_dim_cess})
                affect_edi_obj[0].code21.write({'valeur': rec.immonc_dim_ret})
                affect_edi_obj[0].code22.write({'valeur': rec.immonc_dim_vir})
                affect_edi_obj[0].code23.write({'valeur': rec.immonc_mbf})

                affect_edi_obj[0].fp_mb.write({'valeur': rec.fp_mb})
                affect_edi_obj[0].fp_aug_acq.write({'valeur': rec.fp_aug_acq})
                affect_edi_obj[0].fp_aug_vir.write({'valeur': rec.fp_aug_vir})
                affect_edi_obj[0].fp_dim_cess.write({'valeur': rec.fp_dim_cess})
                affect_edi_obj[0].fp_dim_ret.write({'valeur': rec.fp_dim_ret})
                affect_edi_obj[0].fp_dim_vir.write({'valeur': rec.fp_dim_vir})
                affect_edi_obj[0].fp_mbf.write({'valeur': rec.fp_mbf})

                affect_edi_obj[0].charge_mb.write({'valeur': rec.charge_mb})
                affect_edi_obj[0].charge_aug_acq.write({'valeur': rec.charge_aug_acq})
                affect_edi_obj[0].charge_aug_vir.write({'valeur': rec.charge_aug_vir})
                affect_edi_obj[0].charge_dim_cess.write({'valeur': rec.charge_dim_cess})
                affect_edi_obj[0].charge_dim_ret.write({'valeur': rec.charge_dim_ret})
                affect_edi_obj[0].charge_dim_vir.write({'valeur': rec.charge_dim_vir})
                affect_edi_obj[0].charge_mbf.write({'valeur': rec.charge_mbf})

                affect_edi_obj[0].prime_mb.write({'valeur': rec.prime_mb})
                affect_edi_obj[0].prime_aug_acq.write({'valeur': rec.prime_aug_acq})
                affect_edi_obj[0].prime_aug_vir.write({'valeur': rec.prime_aug_vir})
                affect_edi_obj[0].prime_dim_cess.write({'valeur': rec.prime_dim_cess})
                affect_edi_obj[0].prime_dim_ret.write({'valeur': rec.prime_dim_ret})
                affect_edi_obj[0].prime_dim_vir.write({'valeur': rec.prime_dim_vir})
                affect_edi_obj[0].prime_mbf.write({'valeur': rec.prime_mbf})

                affect_edi_obj[0].immord_mb.write({'valeur': rec.immord_mb})
                affect_edi_obj[0].immord_aug_acq.write({'valeur': rec.immord_aug_acq})
                affect_edi_obj[0].immord_aug_vir.write({'valeur': rec.immord_aug_vir})
                affect_edi_obj[0].immord_dim_cess.write({'valeur': rec.immord_dim_cess})
                affect_edi_obj[0].immord_dim_ret.write({'valeur': rec.immord_dim_ret})
                affect_edi_obj[0].immord_dim_vir.write({'valeur': rec.immord_dim_vir})
                affect_edi_obj[0].immord_mbf.write({'valeur': rec.immord_mbf})

                affect_edi_obj[0].brevet_mb.write({'valeur': rec.brevet_mb})
                affect_edi_obj[0].brevet_aug_acq.write({'valeur': rec.brevet_aug_acq})
                affect_edi_obj[0].brevet_aug_vir.write({'valeur': rec.brevet_aug_vir})
                affect_edi_obj[0].brevet_dim_cess.write({'valeur': rec.brevet_dim_cess})
                affect_edi_obj[0].brevet_dim_ret.write({'valeur': rec.brevet_dim_ret})
                affect_edi_obj[0].brevet_dim_vir.write({'valeur': rec.brevet_dim_vir})
                affect_edi_obj[0].brevet_mbf.write({'valeur': rec.brevet_mbf})

                affect_edi_obj[0].fond_mb.write({'valeur': rec.fond_mb})
                affect_edi_obj[0].fond_aug_acq.write({'valeur': rec.fond_aug_acq})
                affect_edi_obj[0].fond_aug_vir.write({'valeur': rec.fond_aug_vir})
                affect_edi_obj[0].fond_dim_cess.write({'valeur': rec.fond_dim_cess})
                affect_edi_obj[0].fond_dim_ret.write({'valeur': rec.fond_dim_ret})
                affect_edi_obj[0].fond_dim_vir.write({'valeur': rec.fond_dim_vir})
                affect_edi_obj[0].fond_mbf.write({'valeur': rec.fond_mbf})

                affect_edi_obj[0].autre_incorp_mb.write({'valeur': rec.autre_incorp_mb})
                affect_edi_obj[0].autre_incorp_aug_acq.write(
                    {'valeur': rec.autre_incorp_aug_acq})
                affect_edi_obj[0].autre_incorp_aug_vir.write(
                    {'valeur': rec.autre_incorp_aug_vir})
                affect_edi_obj[0].autre_incorp_dim_cess.write(
                    {'valeur': rec.autre_incorp_dim_cess})
                affect_edi_obj[0].autre_incorp_dim_ret.write(
                    {'valeur': rec.autre_incorp_dim_ret})
                affect_edi_obj[0].autre_incorp_dim_vir.write(
                    {'valeur': rec.autre_incorp_dim_vir})
                affect_edi_obj[0].autre_incorp_mbf.write({'valeur': rec.autre_incorp_mbf})

                affect_edi_obj[0].terrain_mb.write({'valeur': rec.terrain_mb})
                affect_edi_obj[0].terrain_aug_acq.write({'valeur': rec.terrain_aug_acq})
                affect_edi_obj[0].terrain_aug_vir.write({'valeur': rec.terrain_aug_vir})
                affect_edi_obj[0].terrain_dim_cess.write({'valeur': rec.terrain_dim_cess})
                affect_edi_obj[0].terrain_dim_ret.write({'valeur': rec.terrain_dim_ret})
                affect_edi_obj[0].terrain_dim_vir.write({'valeur': rec.terrain_dim_vir})
                affect_edi_obj[0].terrain_mbf.write({'valeur': rec.terrain_mbf})

                affect_edi_obj[0].constructions_mb.write({'valeur': rec.constructions_mb})
                affect_edi_obj[0].constructions_aug_acq.write(
                    {'valeur': rec.constructions_aug_acq})
                affect_edi_obj[0].constructions_aug_vir.write(
                    {'valeur': rec.constructions_aug_vir})
                affect_edi_obj[0].constructions_dim_cess.write(
                    {'valeur': rec.constructions_dim_cess})
                affect_edi_obj[0].constructions_dim_ret.write(
                    {'valeur': rec.constructions_dim_ret})
                affect_edi_obj[0].constructions_dim_vir.write(
                    {'valeur': rec.constructions_dim_vir})
                affect_edi_obj[0].constructions_mbf.write({'valeur': rec.constructions_mbf})

                affect_edi_obj[0].inst_mb.write({'valeur': rec.inst_mb})

                affect_edi_obj[0].inst_aug_acq.write({'valeur': rec.inst_aug_acq})
                affect_edi_obj[0].inst_aug_vir.write({'valeur': rec.inst_aug_vir})
                affect_edi_obj[0].inst_dim_cess.write({'valeur': rec.inst_dim_cess})
                affect_edi_obj[0].inst_dim_ret.write({'valeur': rec.inst_dim_ret})
                affect_edi_obj[0].inst_dim_vir.write({'valeur': rec.inst_dim_vir})
                affect_edi_obj[0].inst_mbf.write({'valeur': rec.inst_mbf})

                affect_edi_obj[0].mat_mb.write({'valeur': rec.mat_mb})
                affect_edi_obj[0].mat_aug_acq.write({'valeur': rec.mat_aug_acq})
                affect_edi_obj[0].mat_aug_vir.write({'valeur': rec.mat_aug_vir})
                affect_edi_obj[0].mat_dim_cess.write({'valeur': rec.mat_dim_cess})
                affect_edi_obj[0].mat_dim_ret.write({'valeur': rec.mat_dim_ret})
                affect_edi_obj[0].mat_dim_vir.write({'valeur': rec.mat_dim_vir})
                affect_edi_obj[0].mat_mbf.write({'valeur': rec.mat_mbf})

                affect_edi_obj[0].mob_mb.write({'valeur': rec.mob_mb})
                affect_edi_obj[0].mob_aug_acq.write({'valeur': rec.mob_aug_acq})
                affect_edi_obj[0].mob_aug_vir.write({'valeur': rec.mob_aug_vir})
                affect_edi_obj[0].mob_dim_cess.write({'valeur': rec.mob_dim_cess})
                affect_edi_obj[0].mob_dim_ret.write({'valeur': rec.mob_dim_ret})
                affect_edi_obj[0].mob_dim_vir.write({'valeur': rec.mob_dim_vir})
                affect_edi_obj[0].mob_mbf.write({'valeur': rec.mob_mbf})

                affect_edi_obj[0].autre_corp_mb.write({'valeur': rec.autre_corp_mb})
                affect_edi_obj[0].autre_corp_aug_acq.write({'valeur': rec.autre_corp_aug_acq})
                affect_edi_obj[0].autre_corp_aug_vir.write({'valeur': rec.autre_corp_aug_vir})
                affect_edi_obj[0].autre_corp_dim_cess.write({'valeur': rec.autre_corp_dim_cess})
                affect_edi_obj[0].autre_corp_dim_ret.write({'valeur': rec.autre_corp_dim_ret})
                affect_edi_obj[0].autre_corp_dim_vir.write({'valeur': rec.autre_corp_dim_vir})
                affect_edi_obj[0].autre_corp_mbf.write({'valeur': rec.autre_corp_mbf})

                affect_edi_obj[0].immocc_mb.write({'valeur': rec.immocc_mb})
                affect_edi_obj[0].immocc_aug_acq.write({'valeur': rec.immocc_aug_acq})
                affect_edi_obj[0].immocc_aug_vir.write({'valeur': rec.immocc_aug_vir})
                affect_edi_obj[0].immocc_dim_cess.write({'valeur': rec.immocc_dim_cess})
                affect_edi_obj[0].immocc_dim_ret.write({'valeur': rec.immocc_dim_ret})
                affect_edi_obj[0].immocc_dim_vir.write({'valeur': rec.immocc_dim_vir})
                affect_edi_obj[0].immocc_mbf.write({'valeur': rec.immocc_mbf})

                affect_edi_obj[0].mati_mb.write({'valeur': rec.mati_mb})
                affect_edi_obj[0].mati_aug_acq.write({'valeur': rec.mati_aug_acq})
                affect_edi_obj[0].mati_aug_vir.write({'valeur': rec.mati_aug_vir})
                affect_edi_obj[0].mati_dim_cess.write({'valeur': rec.mati_dim_cess})
                affect_edi_obj[0].mati_dim_ret.write({'valeur': rec.mati_dim_ret})
                affect_edi_obj[0].mati_dim_vir.write({'valeur': rec.mati_dim_vir})
                affect_edi_obj[0].mati_mbf.write({'valeur': rec.mati_mbf})
        return True

    def edi_tva(self):
        affect = self.env['liasse.tva.erp']
        code_conf = self.env['liasse.code.erp']
        for rec in self:
            affect_edi_ids = affect.search([], limit=1)
            affect_edi_obj = affect_edi_ids
            if affect_edi_obj:
                affect_edi_obj[0].tva_facsd.write({'valeur': rec.tva_facsd})
                affect_edi_obj[0].tva_faco.write({'valeur': rec.tva_faco})
                affect_edi_obj[0].tva_facd.write({'valeur': rec.tva_facd})
                affect_edi_obj[0].tva_facsf.write({'valeur': rec.tva_facsf})
                affect_edi_obj[0].tva_recsd.write({'valeur': rec.tva_recsd})
                affect_edi_obj[0].tva_reco.write({'valeur': rec.tva_reco})
                affect_edi_obj[0].tva_recd.write({'valeur': rec.tva_recd})
                affect_edi_obj[0].tva_recsf.write({'valeur': rec.tva_recsf})
                affect_edi_obj[0].tva_charsd.write({'valeur': rec.tva_charsd})
                affect_edi_obj[0].tva_charo.write({'valeur': rec.tva_charo})
                affect_edi_obj[0].tva_chard.write({'valeur': rec.tva_chard})
                affect_edi_obj[0].tva_charsf.write({'valeur': rec.tva_charsf})
                affect_edi_obj[0].tva_immosd.write({'valeur': rec.tva_immosd})
                affect_edi_obj[0].tva_immoo.write({'valeur': rec.tva_immoo})
                affect_edi_obj[0].tva_immod.write({'valeur': rec.tva_immod})
                affect_edi_obj[0].tva_immosf.write({'valeur': rec.tva_immosf})
                affect_edi_obj[0].tva_totalsd.write({'valeur': rec.tva_totalsd})
                affect_edi_obj[0].tva_totalo.write({'valeur': rec.tva_totalo})
                affect_edi_obj[0].tva_totald.write({'valeur': rec.tva_totald})
                affect_edi_obj[0].tva_totalsf.write({'valeur': rec.tva_totalsf})
        return True

    def report_nouveau(self, ex_prec):
        print("call report_nouveau")
        # actiiiiif#
        balance = self.env['liasse.balance.erp']
        bilan_actif = self.env['liasse.bilan.actif.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        code_conf = self.env['liasse.code.erp']
        if ex_prec:
            for bal_rec in ex_prec:

                if bal_rec.actif:
                    for ac in bal_rec.actif:
                        print("report_nouveau 111===", ac.code0.code3.valeur)
                        ac.code0.code3.write({'valeur': ac.code3})
                        print("report_nouveau 222===", ac.code0.code3.valeur)
                else:
                    for code in bilan_actif_obj:
                        total1 = bal_rec.count_cell(code.code1)
                        total2 = bal_rec.count_cell(code.code2)
                        total3 = total1 - total2
                        print("report_nouveau 333===", code.code3.valeur)
                        code.code3.write({'valeur': total3})
                        print("report_nouveau 444===", code.code3.valeur)
        else:
            for code in bilan_actif_obj:
                print("report_nouveau 555===", code.code3.valeur)
                code.code3.write({'valeur': '0'})
                print("report_nouveau 666===", code.code3.valeur)

        # passif##########################################
        bilan_passif = self.env['liasse.bilan.passif.erp']
        bilan_passif_ids = bilan_passif.search([], order='sequence')
        bilan_passif_obj = bilan_passif_ids
        code_conf = self.env['liasse.code.erp']
        if ex_prec:
            for bal_rec in ex_prec:
                if bal_rec.passif:
                    for ac in bal_rec.passif:
                        ac.code0.code1.write({'valeur': ac.code1})
                else:
                    for code in bilan_passif_obj:
                        total1 = bal_rec.count_cell(code.code1)
                        print('total1 report: ', total1, 'code ', code.code1.code)
        else:
            for code in bilan_passif_obj:
                code.code1.write({'valeur': '0'})
        # cpc##########################
        bilan_actif = self.env['liasse.cpc.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        code_conf = self.env['liasse.code.erp']
        if ex_prec:
            for bal_rec in ex_prec:
                if bal_rec.cpc:
                    for ac in bal_rec.cpc:
                        ac.code0.code3.write({'valeur': ac.code3})
                else:
                    for code in bilan_actif_obj:
                        total1 = bal_rec.count_cell(code.code1)
                        total2 = bal_rec.count_cell(code.code2)

                        total3 = total1 + total2
                        code.code3.write({'valeur': total3})
        else:
            for code in bilan_actif_obj:
                code.code3.write({'valeur': '0'})

        #### det cpc #################################
        bilan_actif = self.env['liasse.det.cpc.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        if ex_prec:
            for bal_rec in ex_prec:
                if bal_rec.det_cpc:
                    for ac in bal_rec.det_cpc:
                        # TODO AMH CORRECT
                        # code_conf.write({'valeur': ac.code1})
                        ac.code0.code1.write({'valeur': ac.code1})
                else:
                    for code in bilan_actif_obj:
                        total1 = bal_rec.count_cell(code.code1)
                        # code_conf.write(cr,uid,code.code1.id,{'valeur':total1})
        else:
            for code in bilan_actif_obj:
                code.code1.write({'valeur': '0'})
                ### tfr################
        bilan_actif = self.env['liasse.tfr.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        if ex_prec:
            for bal_rec in ex_prec:
                if bal_rec.tfr:
                    for ac in bal_rec.tfr:
                        ac.code0.code1.write({'valeur': ac.code1})
                else:
                    bal_rec.edi_affectation()
                    for code in bilan_actif_obj:
                        total1 = bal_rec.count_cell(code.code1)
                    # code_conf.write(cr,uid,code.code1.id,{'valeur':total1})
        else:
            for code in bilan_actif_obj:
                code.code1.write({'valeur': '0'})
                # caf ##############################
        bilan_actif = self.env['liasse.caf.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        if ex_prec:
            for bal_rec in ex_prec:
                if bal_rec.caf:
                    for ac in bal_rec.caf:
                        ac.code0.code1.write({'valeur': ac.code1})
                else:
                    for code in bilan_actif_obj:
                        total1 = bal_rec.count_cell(code.code1)
        else:
            for code in bilan_actif_obj:
                code.code1.write({'valeur': '0'})
                ####### stock #####

        bilan_actif = self.env['liasse.stock.erp']
        bilan_actif_ids = bilan_actif.search([], order='sequence')
        bilan_actif_obj = bilan_actif_ids
        code_conf = self.env['liasse.code.erp']
        if ex_prec:
            for bal_rec in ex_prec:
                print('bal_rec ', bal_rec)
                if bal_rec.stock:
                    for ac in bal_rec.stock:
                        ac.code0.code3.write({'valeur': ac.code3})
                        ac.code0.code1.write({'valeur': ac.code1})
                        ac.code0.code2.write({'valeur': ac.code2})
                else:
                    for code in bilan_actif_obj:
                        total1 = bal_rec.count_cell(code.code1)
                        total2 = bal_rec.count_cell(code.code2)

                        total3 = total1 + total2
                        code.code3.write({'valeur': total3})
                    # code_conf.write(cr,uid,code.code1.id,{'valeur':total1})
                    # code_conf.write(cr,uid,code.code2.id,{'valeur':total2})
        else:
            for code in bilan_actif_obj:
                code.code3.write({'valeur': '0'})
                code.code1.write({'valeur': '0'})
                code.code2.write({'valeur': '0'})
        return True

    def count_cell(self, code):
        print("call count_cell")
        res = 0
        code_conf = self.env['liasse.code.erp']
        balance = self.env['liasse.balance.line']
        liasse_conf = self.env['liasse.configuration.erp']
        compte_conf_ids = liasse_conf.search([('code', '=', code.id)])
        compte_conf_obj = compte_conf_ids
        # print(code,'===1', compte_conf_obj)
        for compte_conf in compte_conf_obj:
            # print("iTER")
            if compte_conf.type in ['1']:
                # print('NOT')
                for rec in compte_conf.code_ids:
                    compte_conf_somme_ids = liasse_conf.search([('code', '=', rec.id)])
                    compte_conf_somme_obj = compte_conf_somme_ids
                    for compte_conf_somme in compte_conf_somme_obj:
                        for compte_id in compte_conf_somme.compte:
                            for rec2 in self:
                                compte_bal_somme_ids = balance.search(
                                    [('compte', '=like', compte_id.compte + '%'), ('balance_id', '=', rec2.id)])
                                compte_bal_somme_obj = compte_bal_somme_ids
                                for compte_bal_somme in compte_bal_somme_obj:
                                    res += compte_bal_somme.solde
                        for compte_id in compte_conf_somme.comptem:
                            for rec in self:
                                compte_bal_somme_ids = balance.search(
                                    [('compte', '=like', compte_id.compte + '%'), ('balance_id', '=', rec2.id)])
                                compte_bal_somme_obj = compte_bal_somme_ids
                                for compte_bal_somme in compte_bal_somme_obj:
                                    res -= compte_bal_somme.solde
                break
            elif compte_conf.type in ['2']:
                # print("YES")
                # compte_conf.code == "500":
                #    print("AAAAAAAAAA***************AAAAAAAAAA")
                # ("RES::", res)
                for rec in compte_conf.code_ids:
                    print("REC 11", rec, rec.valeur)
                    # if rec.code == "499":
                    #    print("CCCCCC*******************CCCCCCC :", rec.valeur)
                    res += float(rec.valeur)
                    # if rec.code == "499":
                    #    print("BBBBBBBBB*******************BBBBBBBBBBB :", res)
                # print("AFTER 1 LOOP", res)
                # print("min code:", )
                for rec in compte_conf.code_min_ids:
                    # print("REC-",rec, rec.valeur)
                    res -= float(rec.valeur)
            elif compte_conf.type in ['3']:
                for rec in compte_conf.code_ids:
                    if float(rec.valeur) > 0:
                        res += float(rec.valeur)
            elif compte_conf.type in ['4']:
                for rec in compte_conf.code_ids:
                    if float(rec.valeur) < 0:
                        res += abs(float(rec.valeur))
            else:
                for compte_id in compte_conf.compte:
                    for bal_rec in self:
                        compte_bal_somme_ids = balance.search(
                            [('compte', '=like', compte_id.compte + '%'), ('balance_id', '=', bal_rec.id)])
                        compte_bal_somme_obj = compte_bal_somme_ids
                        for compte_bal_somme in compte_bal_somme_obj:
                            res += compte_bal_somme.solde
                for compte_id in compte_conf.comptem:
                    for bal_rec in self:
                        compte_bal_somme_ids = balance.search(
                            [('compte', '=like', compte_id.compte + '%'), ('balance_id', '=', bal_rec.id)])
                        compte_bal_somme_obj = compte_bal_somme_ids
                        for compte_bal_somme in compte_bal_somme_obj:
                            res -= compte_bal_somme.solde
        print("count_cell 111=====", code.code, code.valeur)
        code.write({'valeur': res})
        print("count_cell 222=====", code.code, code.valeur)
        # print("RETURN", res)
        return res

    def count_init(self, code):
        res = 0
        code_conf = self.env['liasse.code.erp']
        balance = self.env['liasse.balance.line']
        liasse_conf = self.env['liasse.configuration.erp']
        compte_conf_ids = liasse_conf.search([('code', '=', code.id)])
        compte_conf_obj = compte_conf_ids
        for compte_conf in compte_conf_obj:
            if compte_conf.type in ['1']:
                for rec in compte_conf.code_ids:
                    compte_conf_somme_ids = liasse_conf.search([('code', '=', rec.id)])
                    compte_conf_somme_obj = compte_conf_somme_ids
                    for compte_conf_somme in compte_conf_somme_obj:
                        for compte_id in compte_conf_somme.compte:
                            for rec2 in self:
                                compte_bal_somme_ids = balance.search(
                                    [('compte', '=like', compte_id.compte + '%'),
                                     ('balance_id', '=', rec2.id)])
                                compte_bal_somme_obj = compte_bal_somme_ids
                                for compte_bal_somme in compte_bal_somme_obj:
                                    res += abs(compte_bal_somme.init_balance)
                        for compte_id in compte_conf_somme.comptem:
                            for rec in self:
                                compte_bal_somme_ids = balance.search(
                                    [('compte', '=like', compte_id.compte + '%'),
                                     ('balance_id', '=', rec2.id)])
                                compte_bal_somme_obj = compte_bal_somme_ids
                                for compte_bal_somme in compte_bal_somme_obj:
                                    res -= abs(compte_bal_somme.init_balance)
                break
            elif compte_conf.type in ['2']:
                for rec in compte_conf.code_ids:
                    res += float(rec.valeur)
                for rec in compte_conf.code_min_ids:
                    res -= float(rec.valeur)
            else:
                for compte_id in compte_conf.compte:
                    for bal_rec in self:
                        compte_bal_somme_ids = balance.search([('compte', '=like', compte_id.compte + '%'),
                                                               ('balance_id', '=', bal_rec.id)])
                        compte_bal_somme_obj = compte_bal_somme_ids
                        for compte_bal_somme in compte_bal_somme_obj:
                            res += abs(compte_bal_somme.init_balance)
                for compte_id in compte_conf.comptem:
                    for bal_rec in self:
                        compte_bal_somme_ids = balance.search([('compte', '=like', compte_id.compte + '%'),
                                                               ('balance_id', '=', bal_rec.id)])
                        compte_bal_somme_obj = compte_bal_somme_ids
                        for compte_bal_somme in compte_bal_somme_obj:
                            res -= abs(compte_bal_somme.init_balance)
        code.write({'valeur': res})
        return res

    def generate_xml(self):
        doc = etree.Element("odoo", nsmap={})
        data = etree.SubElement(doc, "data", noupdate="1")
        data.append(etree.Comment("Compte"))

        actif_ids = self.env["liasse.configuration.erp"].search([])
        actif_obj = actif_ids
        for line in actif_obj:
            record = etree.SubElement(data, "record", model="liasse.configuration.erp",
                                      id='code_' + str(line.code.code))
            field1 = etree.SubElement(record, "field", name="code", ref='code_' + str(line.code.code))
            field1 = etree.SubElement(record, "field", name="type")
            field1.text = str(line.type)
            if line.code_ids:
                cd = []
                for td in line.code_ids:
                    cd.append('code_' + td.code)
                field1 = etree.SubElement(record, "field", name="code_ids",
                                          eval="[(6, 0, " + str(cd).replace("'", '') + ")]")
            if line.code_min_ids:
                cd = []
                for td in line.code_min_ids:
                    cd.append('code_' + td.code)
                field1 = etree.SubElement(record, "field", name="code_min_ids",
                                          eval="[(6, 0, " + str(cd).replace("'", '') + ")]")

        xml_data = "%s" % (
            etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        )
        self.write({
            'output2': base64.b64encode(xml_data)
        })

        return True

    def file_parsing(self):
        for rec in self:
            self.env.cr.execute(""" delete from liasse_balance_line where balance_id='%s' """ % rec.id)
            dateb = rec.name
            balance_line = self.env['liasse.balance.line']
            [data_table] = self.read()
            print("**************************")
            print(type(data_table))
            print("**************************")
            bal_field = data_table.get("file_data")
            if not bal_field:
                raise ValidationError("Veuillez indiquer le fichier CSV !")
            print("**##**##**##**##11111111111**##**##**##**##**")
            print(bal_field)
            print("**##**##**##**##**##**##**##**##**")
            data_bal = base64.decodestring(bal_field)
            print("**##**##**##**##22222222222**##**##**##**##**")
            print(data_bal)  # b64decode
            print("**##**##**##**##**##**##**##**##**")
            iCount = 0

            try:
                reader = data_bal.decode("utf-8").split("\n")
                print("**##**##**##**##333333**##**##**##**##**")
                print(reader)  # b64decode
                print("**##**##**##**##**##**##**##**##**")
                print("=================", len(reader))
                data = {}

                iID = 0
                str_separator = '";"'
                row = ""

                for row in reader:
                    # row = row.replace('"',"").replace("\r","")
                    print(row, len(row))
                    iCount += 1
                    if len(row) < 4:
                        continue

                    if iCount == 1:
                        line = row.split(str_separator)
                        if len(line) < 5:
                            str_separator = '","'
                            line = row.split(str_separator)
                        if len(line) < 5:
                            str_separator = ';'
                            line = row.split(str_separator)
                        if len(line) < 5:
                            str_separator = ','
                            line = row.split(str_separator)
                    line = row.split(str_separator)
                    if len(line) < 5:
                        if len(row) < 5:
                            raise ValidationError('La ligne %s du fichier contient moins de 5 champs !\n %s' % iCount,
                                                  row)
                            continue
                    if iCount == 1:
                        if line[0].find('id') >= 0:
                            iID = 1
                            iCount = 0

                        if line[0].find('CODE') >= 0:
                            iCount = 0
                            continue
                    if len(line) >= 5 + iID:
                        # print (line)
                        if line[iID + 0] == '':
                            continue
                        line[iID + 0] = line[iID + 0].replace('"', '').replace("\r", "")
                        data["compte"] = line[iID + 0]
                        data["lib"] = line[iID + 1]
                        data["init_balance"] = line[iID + 2].replace(" ", "").replace(",", ".").replace("\r",
                                                                                                        "").replace(
                            '"', '')
                        if data["init_balance"] == '':
                            data["init_balance"] = 0
                        data["debit"] = line[iID + 3].replace(" ", "").replace(",", ".").replace("\r", "").replace('"',
                                                                                                                   '')
                        if data["debit"] == '':
                            data["debit"] = 0
                        data["credit"] = line[iID + 4].replace(" ", "").replace(",", ".").replace("\r", "").replace('"',
                                                                                                                    '')
                        if data["credit"] == '':
                            data["credit"] = 0
                        data["exercice"] = dateb
                        data["balance_id"] = data_table['id']
                        balance_line.create(data)
                        # pprint(data)
                        data = {}
                    # else:
                    # raise osv.except_osv(('Erreur!'), ("Impossible d'importer le fichier, veuillez vérifier que le fichier est correct !"))
            except:
                raise ValidationError(
                    "Impossible d'importer le fichier, veuillez vérifier que le fichier est correct !\nErreur au niveau de la ligne ")
            # except:
            #     raise ValidationError(
            #         "Impossible d'importer le fichier, veuillez vérifier que le fichier est correct !\nErreur au niveau de la ligne %s :\n %s" % (
            #             iCount, row))
            # TEST

    def action_t7(self):

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'credi.bail.erp',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('balance_id', '=', self.id)],
            'context': {'default_balance_id': self.id}
        }

    def action_t10(self):

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pm.value.erp',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('balance_id', '=', self.id)],
            'context': {'default_balance_id': self.id}
        }

    def action_t11(self):

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'titre.particip.erp',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('balance_id', '=', self.id)],
            'context': {'default_balance_id': self.id}
        }

    def action_t13(self):

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'repart.cs.erp',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('balance_id', '=', self.id)],
            'context': {'default_balance_id': self.id}
        }

    def action_t16(self):

        return {
            'name': "Dotation",
            'type': 'ir.actions.act_window',
            'res_model': 'dotation.amort.erp',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('balance_id', '=', self.id)],
            'context': {'default_balance_id': self.id}
        }

    def action_t18_associe(self):

        return {
            'name': "Interet Associe",
            'type': 'ir.actions.act_window',
            'res_model': 'interets.erp',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('balance_id', '=', self.id), ('type', '=', '0')],
            'context': {'default_balance_id': self.id, 'default_type': '0'}
        }

    def action_t18_tiers(self):

        return {
            'name': "Interets Tiers",
            'type': 'ir.actions.act_window',
            'res_model': 'interets.erp',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('balance_id', '=', self.id), ('type', '=', '1')],
            'context': {'default_balance_id': self.id, 'default_type': '1'}
        }

    def action_t19(self):

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'beaux.erp',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('balance_id', '=', self.id)],
            'context': {'default_balance_id': self.id}
        }

    # def check_account_signe(self, account):
    #     signe = 1
    #     if account.startswith('4') or account.startswith('1') or account.startswith('55') or account.startswith('59') or \
    #             account.startswith('7') or account.startswith('28') or account.startswith('29') or account.startswith(
    #         '39'):
    #         signe = -1
    #     return signe
    ################### added #################

    def generate_balance(self):
        """Default export is PDF."""
        for rec in self:
            self.env.cr.execute(""" delete from liasse_balance_line where balance_id='%s' """ % rec.id)
            dateb = rec.name
            balance_line = self.env['liasse.balance.line']

            [data_table] = self.read()
            ec = self.env["account.move.line"].read_group(
                [('state', '=', 'posted'),('date', '>=', self.date_start), ('date', '<=', self.date_end), ('company_id', '=', self.company_id.id),('display_type', 'not in', ('line_section', 'line_note'))], ["account_id", "debit", "credit"],
                groupby="account_id")

            list_account_id = []
            for r in ec:

                data = {}
                account_id = r["account_id"][1].split(" ")
                list_account_id.append(account_id)
                data["compte"] = account_id[0]
                data["lib"] = r["account_id"][1].replace(account_id[0] + " ", '')  # account_id[1:len(account_id)]
                if self.exercice_prec:
                    ecp = self.env["account.move.line"].read_group(
                        [  # ('date', '>=', self.exercice_prec.date_start),
                            ('state', '=', 'posted'),
                            ('date', '<', self.date_start),
                            ("account_id", "=", r["account_id"][0]), ('company_id', '=', self.company_id.id),('display_type', 'not in', ('line_section', 'line_note'))],
                        ["account_id", "debit", "credit"], groupby="account_id")

                    if len(ecp) != 0:
                        if account_id[0].startswith('6') or account_id[0].startswith('7'):
                            data["init_balance"] = 0
                        else:
                            data["init_balance"] = ecp[0]["debit"] - ecp[0]["credit"]

                    else:
                        data["init_balance"] = 0
                else:
                    data["init_balance"] = 0

                data["debit"] = r["debit"]

                data["credit"] = r["credit"]

                data["exercice"] = dateb
                data["balance_id"] = data_table['id']
                balance_line.create(data)
                pprint(data)
            if self.exercice_prec:
                ecp = self.env["account.move.line"].read_group(
                    [  # ('date', '>=', self.exercice_prec.date_start),
                        ('state', '=', 'posted'),
                        ('date', '<=', self.date_start), ('company_id', '=', self.company_id.id),('display_type', 'not in', ('line_section', 'line_note'))
                    ],
                    ["account_id", "debit", "credit"], groupby="account_id")
                for r in ecp:
                    print(r["account_id"])
                    data = {}
                    account_id = r["account_id"][1].split(" ")
                    if account_id not in list_account_id and r["debit"] - r["credit"] != 0:
                        list_account_id.append(account_id)
                        data["compte"] = account_id[0]
                        data["lib"] = r["account_id"][1].replace(account_id[0] + " ",
                                                                 '')  # account_id[1:len(account_id)]
                        if account_id[0].startswith('6') or account_id[0].startswith('7'):
                            data["init_balance"] = 0
                        else:
                            data["init_balance"] = r["debit"] - r["credit"]

                        data["debit"] = 0

                        data["credit"] = 0

                        data["exercice"] = dateb
                        data["balance_id"] = data_table['id']
                        balance_line.create(data)

class kzm_account_move_line(models.Model):
    _inherit = 'account.move.line'

    state = fields.Selection(related="move_id.state")
