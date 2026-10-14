from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session
from sqlalchemy import func

import csv
import io

from ..database import get_db
from ..models import SecurityEvent
from ..models import Alert


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# ==========================================================
# SECURITY REPORT SUMMARY
# ==========================================================

@router.get("/summary")
def get_report_summary(
    db: Session = Depends(get_db)
):

    # ------------------------------------------------------
    # Event statistics
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # Risk distribution
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # Alert statistics
    # ------------------------------------------------------

    total_alerts = (
        db.query(Alert)
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


    # ------------------------------------------------------
    # Detection rate
    # ------------------------------------------------------

    if total_events > 0:

        attack_percentage = round(
            (total_attacks / total_events) * 100,
            2
        )

        normal_percentage = round(
            (total_normal / total_events) * 100,
            2
        )

    else:

        attack_percentage = 0

        normal_percentage = 0


    # ------------------------------------------------------
    # Average confidence
    # ------------------------------------------------------

    average_confidence = (
        db.query(
            func.avg(
                SecurityEvent.confidence
            )
        )
        .scalar()
    )


    if average_confidence is None:

        average_confidence = 0

    else:

        average_confidence = round(
            float(average_confidence),
            2
        )


    # ------------------------------------------------------
    # Average attack probability
    # ------------------------------------------------------

    average_attack_probability = (
        db.query(
            func.avg(
                SecurityEvent.attack_probability
            )
        )
        .scalar()
    )


    if average_attack_probability is None:

        average_attack_probability = 0

    else:

        average_attack_probability = round(
            float(average_attack_probability),
            2
        )


    # ------------------------------------------------------
    # Return report
    # ------------------------------------------------------

    return {

        "report_title":
            "CyberGuard AI Security Report",

        "event_summary": {

            "total_events":
                total_events,

            "total_attacks":
                total_attacks,

            "total_normal":
                total_normal,

            "attack_percentage":
                attack_percentage,

            "normal_percentage":
                normal_percentage
        },

        "risk_distribution": {

            "high":
                high_risk,

            "medium":
                medium_risk,

            "low":
                low_risk
        },

        "alert_summary": {

            "total_alerts":
                total_alerts,

            "open_alerts":
                open_alerts,

            "resolved_alerts":
                resolved_alerts
        },

        "detection_summary": {

            "average_confidence":
                average_confidence,

            "average_attack_probability":
                average_attack_probability,

            "model":
                "Random Forest",

            "task":
                "Binary Network Attack Detection",

            "dataset":
                "UNSW-NB15"
        }
    }


# ==========================================================
# DOWNLOAD SECURITY REPORT
# ==========================================================

@router.get("/download")
def download_report(
    db: Session = Depends(get_db)
):

    # ------------------------------------------------------
    # Get all security events
    # ------------------------------------------------------

    events = (
        db.query(SecurityEvent)
        .order_by(
            SecurityEvent.timestamp.desc()
        )
        .all()
    )


    # ------------------------------------------------------
    # Create CSV in memory
    # ------------------------------------------------------

    output = io.StringIO()

    writer = csv.writer(output)


    # ------------------------------------------------------
    # Report title
    # ------------------------------------------------------

    writer.writerow([
        "CyberGuard AI Security Report"
    ])

    writer.writerow([])


    # ------------------------------------------------------
    # Event summary
    # ------------------------------------------------------

    total_events = len(events)

    total_attacks = sum(
        event.prediction == "Attack"
        for event in events
    )

    total_normal = sum(
        event.prediction == "Normal"
        for event in events
    )


    if total_events > 0:

        attack_percentage = round(
            (total_attacks / total_events) * 100,
            2
        )

        normal_percentage = round(
            (total_normal / total_events) * 100,
            2
        )

    else:

        attack_percentage = 0
        normal_percentage = 0


    writer.writerow([
        "EVENT SUMMARY"
    ])

    writer.writerow([
        "Total Events",
        total_events
    ])

    writer.writerow([
        "Total Attacks",
        total_attacks
    ])

    writer.writerow([
        "Normal Traffic",
        total_normal
    ])

    writer.writerow([
        "Attack Rate (%)",
        attack_percentage
    ])

    writer.writerow([
        "Normal Rate (%)",
        normal_percentage
    ])

    writer.writerow([])


    # ------------------------------------------------------
    # Risk distribution
    # ------------------------------------------------------

    high_risk = sum(
        event.risk_level == "HIGH"
        for event in events
    )

    medium_risk = sum(
        event.risk_level == "MEDIUM"
        for event in events
    )

    low_risk = sum(
        event.risk_level == "LOW"
        for event in events
    )


    writer.writerow([
        "RISK DISTRIBUTION"
    ])

    writer.writerow([
        "High Risk",
        high_risk
    ])

    writer.writerow([
        "Medium Risk",
        medium_risk
    ])

    writer.writerow([
        "Low Risk",
        low_risk
    ])

    writer.writerow([])


    # ------------------------------------------------------
    # Alert statistics
    # ------------------------------------------------------

    total_alerts = (
        db.query(Alert)
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


    writer.writerow([
        "ALERT SUMMARY"
    ])

    writer.writerow([
        "Total Alerts",
        total_alerts
    ])

    writer.writerow([
        "Open Alerts",
        open_alerts
    ])

    writer.writerow([
        "Resolved Alerts",
        resolved_alerts
    ])

    writer.writerow([])


    # ------------------------------------------------------
    # Detection summary
    # ------------------------------------------------------

    average_confidence = (
        db.query(
            func.avg(
                SecurityEvent.confidence
            )
        )
        .scalar()
    )

    average_attack_probability = (
        db.query(
            func.avg(
                SecurityEvent.attack_probability
            )
        )
        .scalar()
    )


    average_confidence = round(
        float(average_confidence or 0),
        2
    )

    average_attack_probability = round(
        float(
            average_attack_probability or 0
        ),
        2
    )


    writer.writerow([
        "DETECTION SUMMARY"
    ])

    writer.writerow([
        "Model",
        "Random Forest"
    ])

    writer.writerow([
        "Dataset",
        "UNSW-NB15"
    ])

    writer.writerow([
        "Task",
        "Binary Network Attack Detection"
    ])

    writer.writerow([
        "Average Confidence (%)",
        average_confidence
    ])

    writer.writerow([
        "Average Attack Probability (%)",
        average_attack_probability
    ])

    writer.writerow([])


    # ------------------------------------------------------
    # Individual security events
    # ------------------------------------------------------

    writer.writerow([
        "SECURITY EVENTS"
    ])

    writer.writerow([
        "ID",
        "Timestamp",
        "Prediction",
        "Confidence (%)",
        "Attack Probability (%)",
        "Normal Probability (%)",
        "Risk Level",
        "Source"
    ])


    for event in events:

        writer.writerow([

            event.id,

            event.timestamp,

            event.prediction,

            event.confidence,

            event.attack_probability,

            event.normal_probability,

            event.risk_level,

            event.source
        ])


    # ------------------------------------------------------
    # Prepare response
    # ------------------------------------------------------

    output.seek(0)


    return StreamingResponse(

        iter([
            output.getvalue()
        ]),

        media_type="text/csv",

        headers={
            "Content-Disposition":
                "attachment; filename=cyberguard_security_report.csv"
        }
    )