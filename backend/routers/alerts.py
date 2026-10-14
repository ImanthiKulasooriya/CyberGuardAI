
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Alert


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


# ======================================================
# GET PAGINATED ALERTS
# ======================================================

@router.get("/")
def get_alerts(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # Total number of alerts
    # --------------------------------------------------

    total = db.query(Alert).count()


    # --------------------------------------------------
    # Calculate offset
    # --------------------------------------------------

    offset = (page - 1) * limit


    # --------------------------------------------------
    # Get only the required page
    # --------------------------------------------------

    alerts = (
        db.query(Alert)
        .order_by(
            Alert.timestamp.desc()
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

        "alerts": [

            {
                "id": alert.id,

                "event_id": alert.event_id,

                "timestamp": alert.timestamp,

                "title": alert.title,

                "severity": alert.severity,

                "message": alert.message,

                "status": alert.status

            }

            for alert in alerts
        ]
    }


# ======================================================
# GET SINGLE ALERT
# ======================================================

@router.get("/{alert_id}")
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = (
        db.query(Alert)
        .filter(
            Alert.id == alert_id
        )
        .first()
    )


    if alert is None:

        raise HTTPException(
            status_code=404,
            detail="Alert not found."
        )


    return {

        "id": alert.id,

        "event_id": alert.event_id,

        "timestamp": alert.timestamp,

        "title": alert.title,

        "severity": alert.severity,

        "message": alert.message,

        "status": alert.status
    }


# ======================================================
# RESOLVE ALERT
# ======================================================

@router.put("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = (
        db.query(Alert)
        .filter(
            Alert.id == alert_id
        )
        .first()
    )


    if alert is None:

        raise HTTPException(
            status_code=404,
            detail="Alert not found."
        )


    if alert.status == "RESOLVED":

        return {

            "message": "Alert is already resolved.",

            "alert_id": alert.id,

            "status": alert.status

        }


    alert.status = "RESOLVED"

    db.commit()

    db.refresh(alert)


    return {

        "message": "Alert resolved successfully.",

        "alert_id": alert.id,

        "status": alert.status

    }
