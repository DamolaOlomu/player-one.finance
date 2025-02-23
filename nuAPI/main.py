from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from nuAPI.models import Payments, RecurringPayment, Base
from nuAPI.database import SessionLocal, engine
from nuAPI.schemas import (
    CardPaymentRequest, CardPaymentResponse,
    BankTransferRequest, BankTransferResponse,
    BankPaymentRequest, BankPaymentResponse,
    CashPaymentRequest, CashPaymentResponse,
    LinkPaymentRequest, LinkPaymentResponse,
    MobileMoneyPaymentRequest, MobileMoneyPaymentResponse,
    MpesaPaymentRequest, MpesaPaymentResponse,
    AirtelMoneyPaymentRequest, AirtelMoneyPaymentResponse,
    VodafoneCashPaymentRequest, VodafoneCashPaymentResponse,
    TigoCashPaymentRequest, TigoCashPaymentResponse,
    EFTPaymentRequest, EFTPaymentResponse,
    SnapScanPaymentRequest, SnapScanPaymentResponse,
    ApplePayPaymentRequest, ApplePayPaymentResponse,
    GooglePayPaymentRequest, GooglePayPaymentResponse,
    SamsungPayPaymentRequest, SamsungPayPaymentResponse,
    MTNMobileMoneyPaymentRequest, MTNMobileMoneyPaymentResponse,
    BankAccountRequest, BankAccountResponse,
)

from sqlalchemy import Column, String, DateTime, Numeric, Integer, Boolean, JSON, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum

Base = declarative_base()

class PaymentStatus(str, Enum):
    confirmed = "confirmed"
    pending = "pending"
    failed = "failed"
    refunded = "refunded"
    disputed = "disputed"
    cancelled = "cancelled"

class BankAccount(Base):
    __tablename__ = 'bank_accounts'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    account_number = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    account_status = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello!": "Welcome to PlayerOne Finance!"}



# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a payment
def create_payment(db: Session, payment_request):
    payment = Payments(
        user_id=str(payment_request.user_id),
        amount=payment_request.amount,
        currency=payment_request.currency,
        payment_status=payment_request.status,
        transaction_reference=str(uuid4())
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

# Read payment by ID
def get_payment(db: Session, payment_id: str):
    return db.query(Payments).filter(Payments.id == payment_id).first()

# Update payment
def update_payment(db: Session, payment_id: str, payment_request):
    payment = db.query(Payments).filter(Payments.id == payment_id).first()
    if payment:
        payment.amount = payment_request.amount
        payment.currency = payment_request.currency
        payment.payment_status = payment_request.status
        db.commit()
        db.refresh(payment)
    return payment

# Delete payment
def delete_payment(db: Session, payment_id: str):
    payment = db.query(Payments).filter(Payments.id == payment_id).first()
    if payment:
        db.delete(payment)
        db.commit()
    return payment

# Card Payments Endpoints
@app.post("/card-payments/", response_model=CardPaymentResponse)
def create_card_payment(payment_request: CardPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return CardPaymentResponse(
        card_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/card-payments/{payment_id}", response_model=CardPaymentResponse)
def read_card_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return CardPaymentResponse(
        card_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/card-payments/{payment_id}", response_model=CardPaymentResponse)
def update_card_payment(payment_id: str, payment_request: CardPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return CardPaymentResponse(
        card_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/card-payments/{payment_id}", response_model=CardPaymentResponse)
def delete_card_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return CardPaymentResponse(
        card_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Bank Transfer Payments Endpoints
@app.post("/bank-transfers/", response_model=BankTransferResponse)
def create_bank_transfer(payment_request: BankTransferRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return BankTransferResponse(
        transfer_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/bank-transfers/{payment_id}", response_model=BankTransferResponse)
def read_bank_transfer(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return BankTransferResponse(
        transfer_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/bank-transfers/{payment_id}", response_model=BankTransferResponse)
def update_bank_transfer(payment_id: str, payment_request: BankTransferRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return BankTransferResponse(
        transfer_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/bank-transfers/{payment_id}", response_model=BankTransferResponse)
def delete_bank_transfer(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return BankTransferResponse(
        transfer_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Bank Payments Endpoints
@app.post("/bank-payments/", response_model=BankPaymentResponse)
def create_bank_payment(payment_request: BankPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return BankPaymentResponse(
        bank_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/bank-payments/{payment_id}", response_model=BankPaymentResponse)
def read_bank_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return BankPaymentResponse(
        bank_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/bank-payments/{payment_id}", response_model=BankPaymentResponse)
def update_bank_payment(payment_id: str, payment_request: BankPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return BankPaymentResponse(
        bank_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/bank-payments/{payment_id}", response_model=BankPaymentResponse)
def delete_bank_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return BankPaymentResponse(
        bank_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Cash Payments Endpoints
@app.post("/cash-payments/", response_model=CashPaymentResponse)
def create_cash_payment(payment_request: CashPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return CashPaymentResponse(
        cash_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/cash-payments/{payment_id}", response_model=CashPaymentResponse)
def read_cash_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return CashPaymentResponse(
        cash_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/cash-payments/{payment_id}", response_model=CashPaymentResponse)
def update_cash_payment(payment_id: str, payment_request: CashPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return CashPaymentResponse(
        cash_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/cash-payments/{payment_id}", response_model=CashPaymentResponse)
def delete_cash_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return CashPaymentResponse(
        cash_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Link Payments Endpoints
@app.post("/link-payments/", response_model=LinkPaymentResponse)
def create_link_payment(payment_request: LinkPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return LinkPaymentResponse(
        link_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/link-payments/{payment_id}", response_model=LinkPaymentResponse)
def read_link_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return LinkPaymentResponse(
        link_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/link-payments/{payment_id}", response_model=LinkPaymentResponse)
def update_link_payment(payment_id: str, payment_request: LinkPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return LinkPaymentResponse(
        link_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/link-payments/{payment_id}", response_model=LinkPaymentResponse)
def delete_link_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return LinkPaymentResponse(
        link_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Mobile Money Payments Endpoints
@app.post("/mobile-money-payments/", response_model=MobileMoneyPaymentResponse)
def create_mobile_money_payment(payment_request: MobileMoneyPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return MobileMoneyPaymentResponse(
        mobile_money_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/mobile-money-payments/{payment_id}", response_model=MobileMoneyPaymentResponse)
def read_mobile_money_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return MobileMoneyPaymentResponse(
        mobile_money_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/mobile-money-payments/{payment_id}", response_model=MobileMoneyPaymentResponse)
def update_mobile_money_payment(payment_id: str, payment_request: MobileMoneyPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return MobileMoneyPaymentResponse(
        mobile_money_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/mobile-money-payments/{payment_id}", response_model=MobileMoneyPaymentResponse)
def delete_mobile_money_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return MobileMoneyPaymentResponse(
        mobile_money_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Mpesa Payments Endpoints
@app.post("/mpesa-payments/", response_model=MpesaPaymentResponse)
def create_mpesa_payment(payment_request: MpesaPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return MpesaPaymentResponse(
        mpesa_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/mpesa-payments/{payment_id}", response_model=MpesaPaymentResponse)
def read_mpesa_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return MpesaPaymentResponse(
        mpesa_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/mpesa-payments/{payment_id}", response_model=MpesaPaymentResponse)
def update_mpesa_payment(payment_id: str, payment_request: MpesaPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return MpesaPaymentResponse(
        mpesa_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/mpesa-payments/{payment_id}", response_model=MpesaPaymentResponse)
def delete_mpesa_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return MpesaPaymentResponse(
        mpesa_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Airtel Money Payments Endpoints
@app.post("/airtel-money-payments/", response_model=AirtelMoneyPaymentResponse)
def create_airtel_money_payment(payment_request: AirtelMoneyPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return AirtelMoneyPaymentResponse(
        airtel_money_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
   )

@app.get("/airtel-money-payments/{payment_id}", response_model=AirtelMoneyPaymentResponse)
def read_airtel_money_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return AirtelMoneyPaymentResponse(
        airtel_money_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/airtel-money-payments/{payment_id}", response_model=AirtelMoneyPaymentResponse)
def update_airtel_money_payment(payment_id: str, payment_request: AirtelMoneyPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return AirtelMoneyPaymentResponse(
        airtel_money_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/airtel-money-payments/{payment_id}", response_model=AirtelMoneyPaymentResponse)
def delete_airtel_money_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return AirtelMoneyPaymentResponse(
        airtel_money_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Vodafone Cash Payments Endpoints
@app.post("/vodafone-cash-payments/", response_model=VodafoneCashPaymentResponse)
def create_vodafone_cash_payment(payment_request: VodafoneCashPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return VodafoneCashPaymentResponse(
        vodafone_cash_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/vodafone-cash-payments/{payment_id}", response_model=VodafoneCashPaymentResponse)
def read_vodafone_cash_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return VodafoneCashPaymentResponse(
        vodafone_cash_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/vodafone-cash-payments/{payment_id}", response_model=VodafoneCashPaymentResponse)
def update_vodafone_cash_payment(payment_id: str, payment_request: VodafoneCashPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return VodafoneCashPaymentResponse(
        vodafone_cash_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/vodafone-cash-payments/{payment_id}", response_model=VodafoneCashPaymentResponse)
def delete_vodafone_cash_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return VodafoneCashPaymentResponse(
        vodafone_cash_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Tigo Cash Payments Endpoints
@app.post("/tigo-cash-payments/", response_model=TigoCashPaymentResponse)
def create_tigo_cash_payment(payment_request: TigoCashPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return TigoCashPaymentResponse(
        tigo_cash_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/tigo-cash-payments/{payment_id}", response_model=TigoCashPaymentResponse)
def read_tigo_cash_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return TigoCashPaymentResponse(
        tigo_cash_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/tigo-cash-payments/{payment_id}", response_model=TigoCashPaymentResponse)
def update_tigo_cash_payment(payment_id: str, payment_request: TigoCashPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return TigoCashPaymentResponse(
        tigo_cash_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/tigo-cash-payments/{payment_id}", response_model=TigoCashPaymentResponse)
def delete_tigo_cash_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return TigoCashPaymentResponse(
        tigo_cash_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# EFT Payments Endpoints
@app.post("/eft-payments/", response_model=EFTPaymentResponse)
def create_eft_payment(payment_request: EFTPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return EFTPaymentResponse(
        eft_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/eft-payments/{payment_id}", response_model=EFTPaymentResponse)
def read_eft_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return EFTPaymentResponse(
        eft_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/eft-payments/{payment_id}", response_model=EFTPaymentResponse)
def update_eft_payment(payment_id: str, payment_request: EFTPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return EFTPaymentResponse(
        eft_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/eft-payments/{payment_id}", response_model=EFTPaymentResponse)
def delete_eft_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return EFTPaymentResponse(
        eft_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# SnapScan Payments Endpoints
@app.post("/snapscan-payments/", response_model=SnapScanPaymentResponse)
def create_snapscan_payment(payment_request: SnapScanPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return SnapScanPaymentResponse(
        snapscan_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/snapscan-payments/{payment_id}", response_model=SnapScanPaymentResponse)
def read_snapscan_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return SnapScanPaymentResponse(
        snapscan_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/snapscan-payments/{payment_id}", response_model=SnapScanPaymentResponse)
def update_snapscan_payment(payment_id: str, payment_request: SnapScanPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return SnapScanPaymentResponse(
        snapscan_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/snapscan-payments/{payment_id}", response_model=SnapScanPaymentResponse)
def delete_snapscan_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return SnapScanPaymentResponse(
        snapscan_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Apple Pay Payments Endpoints
@app.post("/apple-pay-payments/", response_model=ApplePayPaymentResponse)
def create_apple_pay_payment(payment_request: ApplePayPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return ApplePayPaymentResponse(
        applepay_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/apple-pay-payments/{payment_id}", response_model=ApplePayPaymentResponse)
def read_apple_pay_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return ApplePayPaymentResponse(
        applepay_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/apple-pay-payments/{payment_id}", response_model=ApplePayPaymentResponse)
def update_apple_pay_payment(payment_id: str, payment_request: ApplePayPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return ApplePayPaymentResponse(
        applepay_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/apple-pay-payments/{payment_id}", response_model=ApplePayPaymentResponse)
def delete_apple_pay_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return ApplePayPaymentResponse(
        applepay_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Google Pay Payments Endpoints
@app.post("/google-pay-payments/", response_model=GooglePayPaymentResponse)
def create_google_pay_payment(payment_request: GooglePayPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return GooglePayPaymentResponse(
        googlepay_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/google-pay-payments/{payment_id}", response_model=GooglePayPaymentResponse)
def read_google_pay_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return GooglePayPaymentResponse(
        googlepay_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/google-pay-payments/{payment_id}", response_model=GooglePayPaymentResponse)
def update_google_pay_payment(payment_id: str, payment_request: GooglePayPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return GooglePayPaymentResponse(
        googlepay_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/google-pay-payments/{payment_id}", response_model=GooglePayPaymentResponse)
def delete_google_pay_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return GooglePayPaymentResponse(
        googlepay_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Samsung Pay Payments Endpoints
@app.post("/samsung-pay-payments/", response_model=SamsungPayPaymentResponse)
def create_samsung_pay_payment(payment_request: SamsungPayPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return SamsungPayPaymentResponse(
        samsungpay_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/samsung-pay-payments/{payment_id}", response_model=SamsungPayPaymentResponse)
def read_samsung_pay_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return SamsungPayPaymentResponse(
        samsungpay_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/samsung-pay-payments/{payment_id}", response_model=SamsungPayPaymentResponse)
def update_samsung_pay_payment(payment_id: str, payment_request: SamsungPayPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return SamsungPayPaymentResponse(
        samsungpay_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/samsung-pay-payments/{payment_id}", response_model=SamsungPayPaymentResponse)
def delete_samsung_pay_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return SamsungPayPaymentResponse(
        samsungpay_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# MTN Mobile Money Payments Endpoints
@app.post("/mtn-mobile-money-payments/", response_model=MTNMobileMoneyPaymentResponse)
def create_mtn_mobile_money_payment(payment_request: MTNMobileMoneyPaymentRequest, db: Session = Depends(get_db)):
    payment = create_payment(db=db, payment_request=payment_request)
    return MTNMobileMoneyPaymentResponse(
        mtn_mobile_money_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.get("/mtn-mobile-money-payments/{payment_id}", response_model=MTNMobileMoneyPaymentResponse)
def read_mtn_mobile_money_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = get_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return MTNMobileMoneyPaymentResponse(
        mtn_mobile_money_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.put("/mtn-mobile-money-payments/{payment_id}", response_model=MTNMobileMoneyPaymentResponse)
def update_mtn_mobile_money_payment(payment_id: str, payment_request: MTNMobileMoneyPaymentRequest, db: Session = Depends(get_db)):
    payment = update_payment(db=db, payment_id=payment_id, payment_request=payment_request)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return MTNMobileMoneyPaymentResponse(
        mtn_mobile_money_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

@app.delete("/mtn-mobile-money-payments/{payment_id}", response_model=MTNMobileMoneyPaymentResponse)
def delete_mtn_mobile_money_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = delete_payment(db=db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return MTNMobileMoneyPaymentResponse(
        mtn_mobile_money_payment_id=payment.payment_id,
        status=payment.payment_status,
        timestamp=payment.timestamp
    )

# Bank Account Endpoints
@app.post("/bank-accounts/", response_model=BankAccountResponse)
def create_bank_account(bank_account_request: BankAccountRequest, db: Session = Depends(get_db)):
    bank_account = RecurringPayment(
        user_id=str(bank_account_request.user_id),
        account_number=bank_account_request.account_number,
        bank_name=bank_account_request.bank_name,
        account_type=bank_account_request.account_type,
        account_status=bank_account_request.status
    )
    db.add(bank_account)
    db.commit()
    db.refresh(bank_account)
    return BankAccountResponse(
        bank_account_id=bank_account.account_id,
        status=bank_account.account_status,
        timestamp=bank_account.timestamp
    )

@app.get("/bank-accounts/{bank_account_id}", response_model=BankAccountResponse)
def read_bank_account(bank_account_id: str, db: Session = Depends(get_db)):
    bank_account = db.query(RecurringPayment).filter(RecurringPayment.id == bank_account_id).first()
    if bank_account is None:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return BankAccountResponse(
        bank_account_id=bank_account.account_id,
        status=bank_account.account_status,
        timestamp=bank_account.timestamp
    )

@app.put("/bank-accounts/{bank_account_id}", response_model=BankAccountResponse)
def update_bank_account(bank_account_id: str, bank_account_request: BankAccountRequest, db: Session = Depends(get_db)):
    bank_account = db.query(RecurringPayment).filter(RecurringPayment.id == bank_account_id).first()
    if bank_account:
        bank_account.account_number = bank_account_request.account_number
        bank_account.bank_name = bank_account_request.bank_name
        bank_account.account_type = bank_account_request.account_type
        bank_account.account_status = bank_account_request.status
        db.commit()
        db.refresh(bank_account)
    return BankAccountResponse(
        bank_account_id=bank_account.account_id,
        status=bank_account.account_status,
        timestamp=bank_account.timestamp
    )

@app.delete("/bank-accounts/{bank_account_id}", response_model=BankAccountResponse)
def delete_bank_account(bank_account_id: str, db: Session = Depends(get_db)):
    bank_account = db.query(RecurringPayment).filter(RecurringPayment.id == bank_account_id).first()
    if bank_account:
        db.delete(bank_account)
        db.commit()
    return BankAccountResponse(
        bank_account_id=bank_account.account_id,
        status=bank_account.account_status,
        timestamp=bank_account.timestamp
    )