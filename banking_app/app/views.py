
"""
Fab QuickStart 0.1.2

Current Working Directory: /Users/tylerband/git/fab-quick-start/nw-app

From: /Users/tylerband/git/fab-quick-start/banking_logic/venv/bin/fab-quick-start

Using Python: 3.7.3 (default, Aug 16 2020, 10:27:01)
[Clang 11.0.0 (clang-1100.0.33.17)]

Favorites: ['name', 'description']

Non Favorites: ['id']

At: 2020-09-24 17:11:04.278549

"""

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from . import appbuilder, db
from .models import *




class Valid_Acct_TypeModelView(ModelView):
   datamodel = SQLAInterface(ValidAcctType)
   list_columns = ["AcctDescription", "AcctType"]
   show_columns = ["AcctDescription", "AcctType"]
   edit_columns = ["AcctDescription", "AcctType"]
   add_columns = ["AcctDescription", "AcctType"]
   related_views = []

appbuilder.add_view(
      Valid_Acct_TypeModelView, "Valid_Acct_Type List", icon="fa-folder-open-o", category="Menu")





class CHECKING_TRANSModelView(ModelView):
   datamodel = SQLAInterface(CHECKINGTRAN)
   list_columns = ["TransId", "CHECKING.AcctNum", "AcctNum", "CustNum", "Total"]
   show_columns = ["TransId", "CHECKING.AcctNum", "AcctNum", "CustNum", "TransDate", "DepositAmt", "WithdrawlAmt", "Total", "ChkNo", "ImageURL"]
   edit_columns = ["TransId", "AcctNum", "CustNum", "TransDate", "DepositAmt", "WithdrawlAmt",  "ChkNo", "ImageURL"]
   add_columns = ["TransId", "AcctNum", "CustNum", "TransDate", "DepositAmt", "WithdrawlAmt", "ChkNo", "ImageURL"]
   related_views = []

appbuilder.add_view(
      CHECKING_TRANSModelView, "CHECKINGTRANS List", icon="fa-folder-open-o", category="Menu")


# table already generated per recursion: CHECKINGTRANS


class CHECKINGModelView(ModelView):
   datamodel = SQLAInterface(CHECKING)
   list_columns = ["AcctNum", "CUSTOMER.Name", "valid_credit.creditCode", "CustNum", "Deposits","Withdrawls", "AvailableBalance"]
   show_columns = ["AcctNum", "CUSTOMER.Name", "valid_credit.creditCode", "CustNum", "Deposits", "Withdrawls", "CurrentBalance", "AvailableBalance", "ItemCount", "CreditCode", "CreditLimit", "AcctType"]
   edit_columns = ["AcctNum", "CustNum", "Deposits", "Withdrawls", "CreditCode", "CreditLimit", "AcctType"]
   add_columns = ["AcctNum", "CustNum", "Deposits", "Withdrawls", "CreditCode", "CreditLimit", "AcctType"]
   related_views = [CHECKING_TRANSModelView, CHECKING_TRANSModelView]

appbuilder.add_view(
      CHECKINGModelView, "CHECKING List", icon="fa-folder-open-o", category="Menu")





class valid_creditModelView(ModelView):
   datamodel = SQLAInterface(ValidCredit)
   list_columns = ["creditCode", "displayValue", "MaxCreditLimit"]
   show_columns = ["creditCode", "displayValue", "MaxCreditLimit"]
   edit_columns = ["creditCode", "displayValue", "MaxCreditLimit"]
   add_columns = ["creditCode", "displayValue", "MaxCreditLimit"]
   related_views = [CHECKINGModelView]

appbuilder.add_view(
      valid_creditModelView, "valid_credit List", icon="fa-folder-open-o", category="Menu")





class ALERTModelView(ModelView):
   datamodel = SQLAInterface(ALERT)
   list_columns = ["AlertID", "CUSTOMER.Name", "CustNum", "AcctNum", "WhenBalance"]
   show_columns = ["AlertID", "CUSTOMER.Name", "CustNum", "AcctNum", "WhenBalance", "AccountBalance", "EmailAddress"]
   edit_columns = ["AlertID", "CustNum", "AcctNum", "WhenBalance", "AccountBalance", "EmailAddress"]
   add_columns = ["AlertID", "CustNum", "AcctNum", "WhenBalance", "AccountBalance", "EmailAddress"]
   related_views = []

appbuilder.add_view(
      ALERTModelView, "ALERT List", icon="fa-folder-open-o", category="Menu")


# table already generated per recursion: CHECKING


class LOC_TRANSACTIONSModelView(ModelView):
   datamodel = SQLAInterface(LOCTRANSACTION)
   list_columns = ["TransId", "LINE_OF_CREDIT.CustNum", "TransDate", "PaymentAmt", "ChargeAmt"]
   show_columns = ["TransId", "LINE_OF_CREDIT.CustNum", "TransDate", "PaymentAmt", "ChargeAmt", "ChargeType", "CustNum", "AcctNum"]
   edit_columns = ["TransId", "TransDate", "PaymentAmt", "ChargeAmt", "ChargeType", "CustNum", "AcctNum"]
   add_columns = ["TransId", "TransDate", "PaymentAmt", "ChargeAmt", "ChargeType", "CustNum", "AcctNum"]
   related_views = []

appbuilder.add_view(
      LOC_TRANSACTIONSModelView, "LOC_TRANSACTIONS List", icon="fa-folder-open-o", category="Menu")


# table already generated per recursion: LOC_TRANSACTIONS


class LINE_OF_CREDITModelView(ModelView):
   datamodel = SQLAInterface(LINEOFCREDIT)
   list_columns = ["CustNum", "CUSTOMER.Name", "AcctNum", "OverdaftFeeAmt", "LineOfCreditAmt"]
   show_columns = ["CustNum", "CUSTOMER.Name", "AcctNum", "OverdaftFeeAmt", "LineOfCreditAmt", "TotalCharges", "TotalPayments", "AvailableBalance", "Id"]
   edit_columns = ["CustNum", "AcctNum", "OverdaftFeeAmt", "LineOfCreditAmt", "TotalCharges", "TotalPayments", "AvailableBalance", "Id"]
   add_columns = ["CustNum", "AcctNum", "OverdaftFeeAmt", "LineOfCreditAmt", "TotalCharges", "TotalPayments", "AvailableBalance", "Id"]
   related_views = [LOC_TRANSACTIONSModelView, LOC_TRANSACTIONSModelView]

appbuilder.add_view(
      LINE_OF_CREDITModelView, "LINE_OF_CREDIT List", icon="fa-folder-open-o", category="Menu")





class SAVINGS_TRANSModelView(ModelView):
   datamodel = SQLAInterface(SAVINGSTRAN)
   list_columns = ["TransId", "SAVINGS.AcctNum", "AcctNum", "CustNum", "Total"]
   show_columns = ["TransId", "SAVINGS.AcctNum", "AcctNum", "CustNum", "TransDate", "DepositAmt", "WithdrawlAmt", "Total"]
   edit_columns = ["TransId", "AcctNum", "CustNum", "TransDate", "DepositAmt", "WithdrawlAmt"]
   add_columns = ["TransId", "AcctNum", "CustNum", "TransDate", "DepositAmt", "WithdrawlAmt"]
   related_views = []

appbuilder.add_view(
      SAVINGS_TRANSModelView, "SAVINGSTRANS List", icon="fa-folder-open-o", category="Menu")


# table already generated per recursion: SAVINGSTRANS


class SAVINGSModelView(ModelView):
   datamodel = SQLAInterface(SAVING)
   list_columns = ["AcctNum", "CUSTOMER.Name", "CustNum", "Deposits", "Withdrawls",  "AvailableBalance"]
   show_columns = ["AcctNum", "CUSTOMER.Name", "CustNum", "Deposits", "Withdrawls", "CurrentBalance", "AvailableBalance", "ItemCount", "AcctType"]
   edit_columns = ["AcctNum", "CustNum", "Deposits", "Withdrawls", "AcctType"]
   add_columns = ["AcctNum", "CustNum", "Deposits", "Withdrawls",  "AcctType"]
   related_views = [SAVINGS_TRANSModelView, SAVINGS_TRANSModelView]

appbuilder.add_view(
      SAVINGSModelView, "SAVINGS List", icon="fa-folder-open-o", category="Menu")





class TRANSFER_FUNDSModelView(ModelView):
   datamodel = SQLAInterface(TRANSFERFUND)
   list_columns = ["TransId", "CUSTOMER.Name", "FromAcct", "FromCustNum", "ToAcct"]
   show_columns = ["TransId", "CUSTOMER.Name", "FromAcct", "FromCustNum", "ToAcct", "ToCustNum", "TransferAmt", "TransDate"]
   edit_columns = ["TransId", "FromAcct", "FromCustNum", "ToAcct", "ToCustNum", "TransferAmt", "TransDate"]
   add_columns = ["TransId", "FromAcct", "FromCustNum", "ToAcct", "ToCustNum", "TransferAmt", "TransDate"]
   related_views = []

appbuilder.add_view(
      TRANSFER_FUNDSModelView, "TRANSFER_FUNDS List", icon="fa-folder-open-o", category="Menu")


# table already generated per recursion: TRANSFER_FUNDS


class CUSTOMERModelView(ModelView):
   datamodel = SQLAInterface(CUSTOMER)
   list_columns = ["Name", "valid_state.stateName", "CustNum", "CheckingAcctBal", "SavingsAcctBal", "TotalBalance"]
   show_columns = ["Name", "valid_state.stateName", "CustNum", "Street", "City", "State", "ZIP", "Phone", "emailAddress", "CheckingAcctBal", "SavingsAcctBal", "TotalBalance"]
   edit_columns = ["Name", "CustNum", "Street", "City", "State", "ZIP", "Phone", "emailAddress"]
   add_columns = ["Name", "CustNum", "Street", "City", "State", "ZIP", "Phone", "emailAddress"]
   related_views = [ALERTModelView, CHECKINGModelView, LINE_OF_CREDITModelView, SAVINGSModelView, TRANSFER_FUNDSModelView, TRANSFER_FUNDSModelView]

appbuilder.add_view(
      CUSTOMERModelView, "CUSTOMER List", icon="fa-folder-open-o", category="Menu")





class valid_stateModelView(ModelView):
   datamodel = SQLAInterface(ValidState)
   list_columns = ["stateName", "stateCode"]
   show_columns = ["stateName", "stateCode"]
   edit_columns = ["stateName", "stateCode"]
   add_columns = ["stateName", "stateCode"]
   related_views = [CUSTOMERModelView]

appbuilder.add_view(
      valid_stateModelView, "valid_state List", icon="fa-folder-open-o", category="Menu")


# table already generated per recursion: CUSTOMER# table already generated per recursion: ALERT# table already generated per recursion: CHECKING# table already generated per recursion: LINE_OF_CREDIT# table already generated per recursion: SAVINGS# table already generated per recursion: TRANSFER_FUNDS# table already generated per recursion: CHECKINGTRANS# table already generated per recursion: LOC_TRANSACTIONS# table already generated per recursion: SAVINGSTRANS#  12 table(s) in model; generated 12 page(s), including 6 related_view(s).


