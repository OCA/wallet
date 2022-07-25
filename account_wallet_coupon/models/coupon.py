# Copyright 2022 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CouponCoupon(models.Model):

    _name = "coupon.coupon"
    _inherit = ["code.format.mixin", _name]

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    _code_mask = {"mask": "code_mask", "template": "company_id"}

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.code = res._generate_code()
        return res
