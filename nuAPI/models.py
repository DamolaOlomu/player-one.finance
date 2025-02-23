from decimal import Decimal
import string
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from uuid import UUID, uuid4
from datetime import date, datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum as SQLAlchemyEnum, DateTime, Numeric, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"

class User(BaseModel):
    id: UUID = uuid4()
    name: str
    email: str
    password: str

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    customer_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    billing_address = Column(String, nullable=False)
    access_token = Column(String, nullable=False)

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, default=lambda: str(uuid4()), nullable=False)
    payment_reference = Column(String, default=lambda: str(uuid4()), nullable=False)
    payment_method = Column(String, nullable=False)
    payment_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    NGN = "NGN"
    KES = "KES"
    GHS = "GHS"
    ZAR = "ZAR"

class Authorization(BaseModel):
    access_token: str
    token_type: str
    token_history: List[str]

class TwoFA(BaseModel):
    phone_number: str
    sms: str
    code: str
    third_party_auth: bool

class FraudDetection(Base):
    __tablename__ = 'fraud_detection'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    transaction_id = Column(String, nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    transaction_amount = Column(Numeric, nullable=False)
    transaction_currency = Column(String, nullable=False)
    transaction_status = Column(String, nullable=False)
    transaction_message = Column(String, nullable=True)
    fraud_score = Column(Integer, nullable=False)
    fraud_flag = Column(Boolean, nullable=False)
    fraud_reason = Column(String, nullable=True)
    user_ips = Column(JSON, nullable=False)
    user_devices = Column(JSON, nullable=False)
    user_locations = Column(JSON, nullable=False)
    user_emails = Column(JSON, nullable=False)
    user_phone_numbers = Column(JSON, nullable=False)
    user_cards = Column(JSON, nullable=False)
    user_accounts = Column(JSON, nullable=False)

class KYCStatus(str, Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"

class KYCModel(Base):
    __tablename__ = 'kyc'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    document_type = Column(String, nullable=False)  # Can be National ID, Passport, Driver's License, etc.
    document_number = Column(String, nullable=False)
    issued_by = Column(String, nullable=False)  # Issuing authority of the document
    document_expiry = Column(Date, nullable=False)  # Document expiry date
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(KYCStatus), default=KYCStatus.pending, nullable=False)  # Can be Pending, Approved, Rejected

class Refund(Base):
    __tablename__ = 'refunds'

    refund_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    transaction_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    refund_method = Column(String, nullable=False)
    refund_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)

class Dispute(BaseModel):
    dispute_id: UUID = uuid4()
    transaction_id: UUID
    amount: Decimal
    currency: str
    date: datetime = Field(default_factory=datetime.now)
    account_reference: UUID = uuid4()
    payment_reference: UUID = uuid4()
    dispute_method: str
    dispute_gateway_response: str
    status: str
    message: Optional[str] = None

class AuditTrail(Base):
    __tablename__ = 'audit_trail'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    details = Column(String, nullable=True)

class PaymentChannel(str, Enum):
    card = "card"
    bank = "bank"
    wallet = "wallet"
    ussd = "ussd"
    qr = "qr"
    pos = "pos"

class CustomerSupport(Base):
    __tablename__ = 'customer_support'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    interaction = Column(JSON, nullable=False)
    interaction_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    interaction_type = Column(String, nullable=False)
    interaction_status = Column(String, nullable=False)
    interaction_message = Column(String, nullable=True)

class Merchant(Base):
    __tablename__ = 'merchants'

    merchant_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    merchant_name = Column(String, nullable=False)
    merchant_email = Column(String, nullable=False)
    merchant_phone = Column(String, nullable=False)
    merchant_address = Column(String, nullable=False)
    merchant_website = Column(String, nullable=False)
    merchant_logo = Column(String, nullable=True)
    merchant_description = Column(String, nullable=True)
    merchant_category = Column(String, nullable=False)
    merchant_status = Column(String, nullable=False)
    merchant_account = Column(String, nullable=False)

class Encryption(Base):
    __tablename__ = 'encryption'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    encryption_key = Column(String, nullable=False)
    encryption_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    encryption_status = Column(String, nullable=False)
    encryption_message = Column(String, nullable=True)

class Subscription(Base):
    __tablename__ = 'subscriptions'

    subscription_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    subscription_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    subscription_status = Column(String, nullable=False)
    subscription_message = Column(String, nullable=True)

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    method_type = Column(String, nullable=False)
    details = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Charge(Base):
    __tablename__ = 'charges'

    charge_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_method = Column(String, nullable=False)
    payment_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)

class RecurringCharges(Base):
    __tablename__ = 'recurringcharges'

    recurringcharge_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_method = Column(String, nullable=False)
    payment_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    frequency = Column(String, nullable=False)
    interval = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    duration_unit = Column(String, nullable=False)
    next_payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    payment_history = Column(JSON, nullable=False)

class Card(Base):
    __tablename__ = 'cards'

    card_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    card_number = Column(String, nullable=False)
    card_name = Column(String, nullable=False)
    card_expiry = Column(String, nullable=False)
    card_cvv = Column(String, nullable=False)
    card_type = Column(String, nullable=False)
    card_status = Column(String, nullable=False)
    card_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    card_message = Column(String, nullable=True)

class Bank(Base):
    __tablename__ = 'banks'

    bank_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    bank_branch = Column(String, nullable=False)
    bank_account = Column(String, nullable=False)
    bank_status = Column(String, nullable=False)
    bank_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    bank_message = Column(String, nullable=True)

class Wallet(Base):
    __tablename__ = 'wallets'

    wallet_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    wallet_name = Column(String, nullable=False)
    wallet_number = Column(String, nullable=False)
    wallet_status = Column(String, nullable=False)
    wallet_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    wallet_message = Column(String, nullable=True)

class Ussd(Base):
    __tablename__ = 'ussd'

    ussd_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    ussd_number = Column(String, nullable=False)
    ussd_status = Column(String, nullable=False)
    ussd_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    ussd_message = Column(String, nullable=True)

class Qr(Base):
    __tablename__ = 'qr'

    qr_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    qr_code = Column(String, nullable=False)
    qr_status = Column(String, nullable=False)
    qr_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    qr_message = Column(String, nullable=True)

class Pos(Base):
    __tablename__ = 'pos'

    pos_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    pos_number = Column(String, nullable=False)
    pos_status = Column(String, nullable=False)
    pos_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    pos_message = Column(String, nullable=True)

class PaymentStatus(str, Enum):
    confirmed = "confirmed"
    pending = "pending"
    failed = "failed"
    refunded = "refunded"
    disputed = "disputed"
    cancelled = "cancelled"

class MobileMoney(Base):
    __tablename__ = 'mobilemoney'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    payment_status = Column(SQLAlchemyEnum(PaymentStatus), nullable=False)
    transaction_reference = Column(String, default=lambda: str(uuid4()), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

class CashPayments(Base):
    __tablename__ = 'cashpayment'

    cashpayment_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    cashpayment_number = Column(String, nullable=False)
    cashpayment_status = Column(String, nullable=False)
    cashpayment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    cashpayment_message = Column(String, nullable=True)

class SnapScan(Base):
    __tablename__ = 'snapscan'

    snapscan_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    snapscan_number = Column(String, nullable=False)
    snapscan_status = Column(String, nullable=False)
    snapscan_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    snapscan_message = Column(String, nullable=True)

class ApplePay(Base):
    __tablename__ = 'applepay'

    applepay_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    applepay_number = Column(String, nullable=False)
    applepay_status = Column(String, nullable=False)
    applepay_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    applepay_message = Column(String, nullable=True)

class GooglePay(Base):
    __tablename__ = 'googlepay'

    googlepay_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    googlepay_number = Column(String, nullable=False)
    googlepay_status = Column(String, nullable=False)
    googlepay_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    googlepay_message = Column(String, nullable=True)

class SamsungPay(Base):
    __tablename__ = 'samsungpay'

    samsungpay_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    samsungpay_number = Column(String, nullable=False)
    samsungpay_status = Column(String, nullable=False)
    samsungpay_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    samsungpay_message = Column(String, nullable=True)

class BulkCharge(Base):
    __tablename__ = 'bulkcharge'

    bulkcharge_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_method = Column(String, nullable=False)
    payment_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)
    bulkcharge_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    bulkcharge_message = Column(String, nullable=True)

class BulkRefund(Base):
    __tablename__ = 'bulkrefund'

    bulkrefund_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    refund_method = Column(String, nullable=False)
    refund_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)
    bulkrefund_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    bulkrefund_message = Column(String, nullable=True)

class BulkDispute(Base):
    __tablename__ = 'bulkdispute'

    bulkdispute_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    dispute_method = Column(String, nullable=False)
    dispute_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)
    bulkdispute_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    bulkdispute_message = Column(String, nullable=True)

class SplitPayment(Base):
    __tablename__ = 'splitpayment'

    splitpayment_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_method = Column(String, nullable=False)
    payment_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)
    splitpayment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    splitpayment_message = Column(String, nullable=True)

class MultiSplitPayment(Base):
    __tablename__ = 'multisplitpayment'

    multisplitpayment_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_method = Column(String, nullable=False)
    payment_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)
    multisplitpayment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    multisplitpayment_message = Column(String, nullable=True)

class PaymentPlan(Base):
    __tablename__ = 'paymentplan'

    paymentplan_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_method = Column(String, nullable=False)
    payment_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)
    paymentplan_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    paymentplan_message = Column(String, nullable=True)

class DedicatedVirtualAccount(Base):
    __tablename__ = 'dedicatedvirtualaccount'

    dedicatedvirtualaccount_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_method = Column(String, nullable=False)
    payment_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)
    dedicatedvirtualaccount_number = Column(String, nullable=False)
    dedicatedvirtualaccount_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    dedicatedvirtualaccount_message = Column(String, nullable=True)

class PaymentLink(Base):
    __tablename__ = 'paymentlink'

    paymentlink_id= Column(String, primary_key=True, default=lambda: str(uuid4()))
    paymentlink_url = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_method = Column(String, nullable=False)
    payment_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)
    paymentlink_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    paymentlink_message = Column(String, nullable=True)

class PaymentRequest(Base):
    __tablename__ = 'paymentrequest'

    paymentrequest_id= Column(String, primary_key=True, default=lambda: str(uuid4()))
    paymentrequest_url = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_reference = Column(String, nullable=False, default=lambda: str(uuid4()))
    payment_method = Column(String, nullable=False)
    payment_gateway_response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)
    paymentrequest_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    paymentrequest_message = Column(String, nullable=True)

class PaymentStatus(str, Enum):
    confirmed = "confirmed"
    pending = "pending"
    failed = "failed"
    refunded = "refunded"
    disputed = "disputed"
    cancelled = "cancelled"

class Payments(Base):
    __tablename__ = 'payments'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    payment_id = Column(String, default=lambda: str(uuid4()), nullable=False)
    payment_reference = Column(String, default=lambda: str(uuid4()), nullable=False)
    payment_status = Column(SQLAlchemyEnum(PaymentStatus), nullable=False)
    transaction_reference = Column(String, default=lambda: str(uuid4()), nullable=False)
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

class RecurringPayment(Base):
    __tablename__ = 'recurring_payments'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    recurring_status = Column(String, nullable=False)
    recurring_date = Column(DateTime, nullable=False)
    recurring_message = Column(String, nullable=True)