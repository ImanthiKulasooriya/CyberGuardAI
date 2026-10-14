from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from sqlalchemy import func

from ..database import get_db
from ..models import SecurityEvent
from ..models import Alert


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db)
):

    total_events = (
        db.query(SecurityEvent)
        .count()
    )


    total_attacks = (
        db.query(SecurityEvent)
        .filter(
            SecurityEvent.prediction == "Attack"
        )
        .count()
    )


    total_normal = (
        db.query(SecurityEvent)
        .filter(
            SecurityEvent.prediction == "Normal"
        )
        .count()
    )


    high_risk = (
        db.query(SecurityEvent)
        .filter(
            SecurityEvent.risk_level == "HIGH"
        )
        .count()
    )


    medium_risk = (
        db.query(SecurityEvent)
        .filter(
            SecurityEvent.risk_level == "MEDIUM"
        )
        .count()
    )


    low_risk = (
        db.query(SecurityEvent)
        .filter(
            SecurityEvent.risk_level == "LOW"
        )
        .count()
    )


    open_alerts = (
        db.query(Alert)
        .filter(
            Alert.status == "OPEN"
        )
        .count()
    )


    resolved_alerts = (
        db.query(Alert)
        .filter(
            Alert.status == "RESOLVED"
        )
        .count()
    )


    return {

        "total_events": total_events,

        "total_attacks": total_attacks,

        "total_normal": total_normal,

        "risk_distribution": {

            "high": high_risk,

            "medium": medium_risk,

            "low": low_risk
        },

        "alerts": {

            "open": open_alerts,

            "resolved": resolved_alerts
        }
    }