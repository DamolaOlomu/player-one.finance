from fastapi import FastAPI
from typing import List
from pydantic import BaseModel, Field, Optional, constr, condecimal
import uuid
from uuid import UUID, uuid4 
import random
from enum import Enum
from datetime import datetime, timedelta
import string
from decimal import Decimal
from sqlalchemy import Column, String, DateTime, Numeric, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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


class PaymentResponse(BaseModel):
    payment: Payments
    status: PaymentStatus
    message: Optional[str]= None

class RecurringPayment(BaseModel):
    recurring_id: UUID = uuid4()
    user_id: UUID = uuid4()
    recurring_date: datetime = Field(default_factory=datetime.now)
    recurring_status: str
    recurring_message: Optional[str] = None


class CardPaymentRequest(BaseModel):
    user_id: UUID = uuid4()
    amount: Decimal
    currency: str
    customer_name: str
    card_number: str = Field(..., min_length=16, max_length=19, regex=r'^\d{16,19}$')
    card_expiry: str = Field(..., min_length= 3, max_length=5, regex=r'^\/d{0[1-9]2[2-6]}$')
    cvv: str = Field(..., min_length=3, max_length=4, regex=r'^\d{3,4}$')
    status: PaymentStatus
    transaction_reference: uuid.UUID


class CardPaymentResponse(BaseModel):
    card_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_payment(payment_request: CardPaymentRequest) -> CardPaymentResponse:
    card_payment_id : UUID = uuid4()
    status = PaymentStatus.confirmed 
    timestamp = datetime.utcnow()
    
    return CardPaymentResponse(
        card_payment_id=card_payment_id,
        status=status,
        timestamp=timestamp
    )


class UssdPaymentRequest(BaseModel):
    session_id: UUID = uuid4()
    phone_number: str
    text: str


class SmsRequest(BaseModel):
    session_id: UUID = uuid4()
    message:str


class BankAccountRequest(BaseModel):
    account_id: UUID = uuid4()
    account_name: str
    account_number: str = Field(...,min_length=10, max_length=10)
    bank_name: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

def generate_account_number(length: int = 10) -> str:
    return ''.join(random.choices(string.digits, k=length))

TRANSFER_TIMEOUT = timedelta(minutes=30)


class BankTransferRequest(BaseModel):
    transfer_id: UUID = uuid4()
    account_id: UUID = uuid4()
    account_name: str
    account_number: str = Field(..., min_length=10, max_length=10)
    bank_name: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)
    transfer_timeout: timedelta = TRANSFER_TIMEOUT

class BankTransferResponse(BaseModel):
    transfer_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_transfer(transfer_request: BankTransferRequest) -> BankTransferResponse:
    transfer_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return BankTransferResponse(
        transfer_id=transfer_id,
        status=status,
        timestamp=timestamp
    )


class WalletPaymentRequest(BaseModel):
    wallet_id: UUID = uuid4()
    wallet_name: str
    wallet_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WalletPaymentResponse(BaseModel):
    wallet_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_wallet_payment(wallet_request: WalletPaymentRequest) -> WalletPaymentResponse:
    wallet_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return WalletPaymentResponse(
        wallet_payment_id=wallet_payment_id,
        status=status,
        timestamp=timestamp
    )

class WalletTransferRequest(BaseModel):
    transfer_id: UUID = uuid4()
    wallet_id: UUID = uuid4()
    wallet_name: str
    wallet_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)
    transfer_timeout: timedelta = TRANSFER_TIMEOUT

class WalletTransferResponse(BaseModel):
    transfer_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_wallet_transfer(transfer_request: WalletTransferRequest) -> WalletTransferResponse:
    transfer_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return WalletTransferResponse(
        transfer_id=transfer_id,
        status=status,
        timestamp=timestamp
    )


class QrPaymentRequest(BaseModel):
    qr_id: UUID = uuid4()
    qr_code: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class QrPaymentResponse(BaseModel):
    qr_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow


def process_qr_payment(qr_request: QrPaymentRequest) -> QrPaymentResponse:
    qr_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return QrPaymentResponse(
        qr_payment_id=qr_payment_id,
        status=status,
        timestamp=timestamp
    )

class PosPaymentRequest(BaseModel):
    pos_id: UUID = uuid4()
    pos_name: str
    pos_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PosPaymentResponse(BaseModel):
    pos_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_pos_payment(pos_request: PosPaymentRequest) -> PosPaymentResponse:
    pos_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return PosPaymentResponse(
        pos_payment_id=pos_payment_id,
        status=status,
        timestamp=timestamp
    )

class BankPaymentRequest(BaseModel):
    bank_id: UUID = uuid4()
    bank_name: str
    bank_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BankPaymentResponse(BaseModel):
    bank_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow  

def process_bank_payment(bank_request: BankPaymentRequest) -> BankPaymentResponse:
    bank_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return BankPaymentResponse(
        bank_payment_id=bank_payment_id,
        status=status,
        timestamp=timestamp
    )


class LinkPaymentRequest(BaseModel):
    link_id: UUID = uuid4()
    link_name: str
    link_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LinkPaymentResponse(BaseModel):
    link_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_link_payment(link_request: LinkPaymentRequest) -> LinkPaymentResponse:
    link_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return LinkPaymentResponse(
        link_payment_id=link_payment_id,
        status=status,
        timestamp=timestamp
    )


class MobileMoneyPaymentRequest(BaseModel):
    mobile_id: UUID = uuid4()
    mobile_name: str
    mobile_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MobileMoneyPaymentResponse(BaseModel):
    mobile_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_mobile_money_payment(mobile_request: MobileMoneyPaymentRequest) -> MobileMoneyPaymentResponse:
    mobile_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return MobileMoneyPaymentResponse(
        mobile_payment_id=mobile_payment_id,
        status=status,
        timestamp=timestamp
    )


class MpesaPaymentRequest(BaseModel):
    mpesa_id: UUID = uuid4()
    mpesa_name: str
    mpesa_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MpesaPaymentResponse(BaseModel):
    mpesa_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_mpesa_payment(mpesa_request: MpesaPaymentRequest) -> MpesaPaymentResponse:
    mpesa_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return MpesaPaymentResponse(
        mpesa_payment_id=mpesa_payment_id,
        status=status,
        timestamp=timestamp
    )

class AirtelMoneyPaymentRequest(BaseModel):
    airtel_id: UUID = uuid4()
    airtel_name: str
    airtel_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AirtelMoneyPaymentResponse(BaseModel):
    airtel_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_airtel_money_payment(airtel_request: AirtelMoneyPaymentRequest) -> AirtelMoneyPaymentResponse:
    airtel_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return AirtelMoneyPaymentResponse(
        airtel_payment_id=airtel_payment_id,
        status=status,
        timestamp=timestamp
    )

class VodafoneCashPaymentRequest(BaseModel):
    vodafone_id: UUID = uuid4()
    vodafone_name: str
    vodafone_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class VodafoneCashPaymentResponse(BaseModel):
    vodafone_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_vodafone_cash_payment(vodafone_request: VodafoneCashPaymentRequest) -> VodafoneCashPaymentResponse:
    vodafone_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return VodafoneCashPaymentResponse(
        vodafone_payment_id=vodafone_payment_id,
        status=status,
        timestamp=timestamp
    )

class TigoCashPaymentRequest(BaseModel):
    tigo_id: UUID = uuid4()
    tigo_name: str
    tigo_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TigoCashPaymentResponse(BaseModel):
    tigo_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_tigo_cash_payment(tigo_request: TigoCashPaymentRequest) -> TigoCashPaymentResponse:
    tigo_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return TigoCashPaymentResponse(
        tigo_payment_id=tigo_payment_id,
        status=status,
        timestamp=timestamp
    )



class EFTPaymentRequest(BaseModel):
    eft_id: UUID = uuid4()
    eft_name: str
    eft_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EFTPaymentResponse(BaseModel):
    eft_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_eft_payment(eft_request: EFTPaymentRequest) -> EFTPaymentResponse:
    eft_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return EFTPaymentResponse(
        eft_payment_id=eft_payment_id,
        status=status,
        timestamp=timestamp
    )

class SnapScanPaymentRequest(BaseModel):
    snapscan_id: UUID = uuid4()
    snapscan_name: str
    snapscan_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SnapScanPaymentResponse(BaseModel):
    snapscan_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_snapscan_payment(snapscan_request: SnapScanPaymentRequest) -> SnapScanPaymentResponse:
    snapscan_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return SnapScanPaymentResponse(
        snapscan_payment_id=snapscan_payment_id,
        status=status,
        timestamp=timestamp
    )

class ApplePayPaymentRequest(BaseModel):
    user_id: UUID
    amount: Decimal
    currency: str
    payment_reference: str
    description: Optional[str] = None

class ApplePayPaymentResponse(BaseModel):
    applepay_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

def process_applepay_payment(applepay_request: ApplePayPaymentRequest) -> ApplePayPaymentResponse:
    applepay_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return ApplePayPaymentResponse(
        applepay_payment_id=applepay_payment_id,
        status=status,
        timestamp=timestamp
    )

class GooglePayPaymentRequest(BaseModel):
    user_id: UUID
    amount: Decimal
    currency: str
    payment_reference: str
    description: Optional[str] = None

class GooglePayPaymentResponse(BaseModel):
    googlepay_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

def process_googlepay_payment(googlepay_request: GooglePayPaymentRequest) -> GooglePayPaymentResponse:
    googlepay_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return GooglePayPaymentResponse(
        googlepay_payment_id=googlepay_payment_id,
        status=status,
        timestamp=timestamp
    )

class PayPalPaymentRequest(BaseModel):
    user_id: UUID
    amount: Decimal
    currency: str
    payment_reference: str
    description: Optional[str] = None

class PayPalPaymentResponse(BaseModel):
    paypal_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

def process_paypal_payment(paypal_request: PayPalPaymentRequest) -> PayPalPaymentResponse:
    paypal_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return PayPalPaymentResponse(
        paypal_payment_id=paypal_payment_id,
        status=status,
        timestamp=timestamp
    )

class StripePaymentRequest(BaseModel):
    user_id: UUID
    amount: Decimal
    currency: str
    payment_reference: str
    description: Optional[str] = None

class StripePaymentResponse(BaseModel):
    stripe_payment_id: UUID = Field(default_factory=uuid4)
    status: PaymentStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)

def process_stripe_payment(stripe_request: StripePaymentRequest) -> StripePaymentResponse:
    stripe_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return StripePaymentResponse(
        stripe_payment_id=stripe_payment_id,
        status=status,
        timestamp=timestamp
    )

class SamsungPayPaymentRequest(BaseModel):
    samsungpay_id: UUID = uuid4()
    samsungpay_name: str
    samsungpay_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SamsungPayPaymentResponse(BaseModel):
    samsungpay_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_samsungpay_payment(samsungpay_request: SamsungPayPaymentRequest) -> SamsungPayPaymentResponse:
    samsungpay_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return SamsungPayPaymentResponse(
        samsungpay_payment_id=samsungpay_payment_id,
        status=status,
        timestamp=timestamp
    )

class AirtelTigoMoneyPaymentRequest(BaseModel):
    airteltigo_id: UUID = uuid4()
    airteltigo_name: str
    airteltigo_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AirtelTigoMoneyPaymentResponse(BaseModel):
    airteltigo_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_airteltigo_money_payment(airteltigo_request: AirtelTigoMoneyPaymentRequest) -> AirtelTigoMoneyPaymentResponse:
    airteltigo_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return AirtelTigoMoneyPaymentResponse(
        airteltigo_payment_id=airteltigo_payment_id,
        status=status,
        timestamp=timestamp
    )

class MTNMobileMoneyPaymentRequest(BaseModel):
    mtn_id: UUID = uuid4()
    mtn_name: str
    mtn_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MTNMobileMoneyPaymentResponse(BaseModel):
    mtn_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_mtn_mobile_money_payment(mtn_request: MTNMobileMoneyPaymentRequest) -> MTNMobileMoneyPaymentResponse:
    mtn_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return MTNMobileMoneyPaymentResponse(
        mtn_payment_id=mtn_payment_id,
        status=status,
        timestamp=timestamp
    )

class VodafoneMobileMoneyPaymentRequest(BaseModel):
    vodafone_id: UUID = uuid4()
    vodafone_name: str
    vodafone_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class VodafoneMobileMoneyPaymentResponse(BaseModel):
    vodafone_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow

def process_vodafone_mobile_money_payment(vodafone_request: VodafoneMobileMoneyPaymentRequest) -> VodafoneMobileMoneyPaymentResponse:
    vodafone_payment_id: UUID = uuid4()
    status = PaymentStatus.confirmed
    timestamp = datetime.utcnow()

    return VodafoneMobileMoneyPaymentResponse(
        vodafone_payment_id=vodafone_payment_id,
        status=status,
        timestamp=timestamp
    )


class DedicatedVirtualAccountRequest(BaseModel):
    virtual_id: UUID = uuid4()
    virtual_name: str
    virtual_account_number: str = Field(..., min_length=10, max_length=10)
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DedicatedVirtualAccountResponse(BaseModel):
    virtual_payment_id: UUID = uuid4()
    status: PaymentStatus
    timestamp: datetime.utcnow


