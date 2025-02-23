from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import Optional

class PaymentStatus(str, Enum):
    confirmed = "confirmed"
    pending = "pending"
    failed = "failed"
    refunded = "refunded"
    disputed = "disputed"
    cancelled = "cancelled"

class CardPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    customer_name: str
    card_number: str = Field(..., min_length=16, max_length=19, pattern=r'^\d{16,19}$')
    card_expiry: str = Field(..., min_length=3, max_length=5, pattern=r'^\d{2}/\d{2}$')
    cvv: str = Field(..., min_length=3, max_length=4, pattern=r'^\d{3,4}$')
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class CardPaymentResponse(BaseModel):
    card_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class BankTransferRequest(BaseModel):
    transfer_id: UUID = Field(default_factory=uuid4)
    account_id: UUID = Field(default_factory=uuid4)
    account_name: str
    account_number: str = Field(..., min_length=10, max_length=10)
    bank_name: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BankTransferResponse(BaseModel):
    transfer_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class BankPaymentRequest(BaseModel):
    bank_id: UUID = Field(default_factory=uuid4)
    bank_name: str
    bank_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BankPaymentResponse(BaseModel):
    bank_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CashPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class CashPaymentResponse(BaseModel):
    cash_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class LinkPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class LinkPaymentResponse(BaseModel):
    link_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MobileMoneyPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class MobileMoneyPaymentResponse(BaseModel):
    mobile_money_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MpesaPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class MpesaPaymentResponse(BaseModel):
    mpesa_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AirtelMoneyPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class AirtelMoneyPaymentResponse(BaseModel):
    airtel_money_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class VodafoneCashPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class VodafoneCashPaymentResponse(BaseModel):
    vodafone_cash_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class TigoCashPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class TigoCashPaymentResponse(BaseModel):
    tigo_cash_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class EFTPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class EFTPaymentResponse(BaseModel):
    eft_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SnapScanPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class SnapScanPaymentResponse(BaseModel):
    snapscan_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ApplePayPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class ApplePayPaymentResponse(BaseModel):
    applepay_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class GooglePayPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class GooglePayPaymentResponse(BaseModel):
    googlepay_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SamsungPayPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class SamsungPayPaymentResponse(BaseModel):
    samsungpay_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MTNMobileMoneyPaymentRequest(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    amount: Decimal
    currency: str
    status: PaymentStatus
    transaction_reference: UUID = Field(default_factory=uuid4)

class MTNMobileMoneyPaymentResponse(BaseModel):
    mtn_mobile_money_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class BankAccountRequest(BaseModel):
    account_id: UUID = Field(default_factory=uuid4)
    account_name: str
    account_number: str = Field(..., min_length=10, max_length=10)
    bank_name: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BankAccountResponse(BaseModel):
    account_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)