from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import SecurityEvent


router = APIRouter(
    prefix="/events",
    tags=["Security Events"]
)


# ======================================================
# GET PAGINATED SECURITY EVENTS
# ======================================================

@router.get("/")
def get_events(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # Total number of events
    # --------------------------------------------------

    total = db.query(SecurityEvent).count()


    # --------------------------------------------------
    # Calculate offset
    # --------------------------------------------------

    offset = (page - 1) * limit


    # --------------------------------------------------
    # Get only the required page
    # --------------------------------------------------

    events = (
        db.query(SecurityEvent)
        .order_by(
            SecurityEvent.timestamp.desc()
        )
        .offset(offset)
        .limit(limit)
        .all()
    )


    # --------------------------------------------------
    # Calculate total pages
    # --------------------------------------------------

    total_pages = (
        (total + limit - 1) // limit
        if total > 0
        else 1
    )


    # --------------------------------------------------
    # Return response
    # --------------------------------------------------

    return {

        "total": total,

        "page": page,

        "limit": limit,

        "total_pages": total_pages,

        "events": [

            {
                "id": event.id,

                "timestamp": event.timestamp,

                "prediction": event.prediction,

                "confidence": event.confidence,

                "attack_probability": event.attack_probability,

                "normal_probability": event.normal_probability,

                "risk_level": event.risk_level,

                "source": event.source

            }

            for event in events
        ]
    }


# ======================================================
# GET SINGLE SECURITY EVENT
# ======================================================

@router.get("/{event_id}")
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):

    event = (
        db.query(SecurityEvent)
        .filter(
            SecurityEvent.id == event_id
        )
        .first()
    )


    if event is None:

        raise HTTPException(
            status_code=404,
            detail="Security event not found."
        )


    return {

        "id": event.id,

        "timestamp": event.timestamp,

        "prediction": event.prediction,

        "confidence": event.confidence,

        "attack_probability": event.attack_probability,

        "normal_probability": event.normal_probability,

        "risk_level": event.risk_level,

        "source": event.source
    }
