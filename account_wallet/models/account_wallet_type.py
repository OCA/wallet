# © 2015  Laetitia Gangloff, Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountWalletType(models.Model):
    _name = "account.wallet.type"
    _description = "Wallet Type"
    _check_company_auto = True

    name = fields.Char(translate=True, required=True)
    sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Wallet Sequence",
        copy=False,
        check_company=True,
        help="This field contains the information related to the numbering "
        "of the wallet of this type.",
        required=True,
    )
    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account",
        ondelete="restrict",
        index=True,
        required=True,
    )
    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
        ondelete="restrict",
        help="Journal use to empty the wallet",
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        ondelete="restrict",
        help="Product use to fill the wallet",
        required=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
        required=True,
    )

    no_anonymous = fields.Boolean(
        help="Check this box if you want to generate only nominative wallets."
    )

    _sql_constraints = [
        (
            "product_wallet_type_uniq",
            "unique(product_id, company_id)",
            "A wallet type with the product already exists",
        ),
        (
            "account_wallet_uniq",
            "unique(account_id)",
            "A wallet type with this account already exists",
        ),
    ]

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id and not self.account_id:
            self.account_id = self.product_id._get_product_accounts()["income"]
