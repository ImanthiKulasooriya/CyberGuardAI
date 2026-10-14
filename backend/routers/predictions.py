import pandas as pd

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session

from ..ml_service import predict_dataframe
from ..database import get_db
from ..models import SecurityEvent
from ..models import Alert


router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)


# Process 5,000 rows at a time
CHUNK_SIZE = 5000


@router.post("/csv")
async def predict_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # ======================================================
    # 1. Validate file
    # ======================================================

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file provided."
        )

    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    # ======================================================
    # 2. Prepare counters
    # ======================================================

    total_records = 0

    attack_count = 0
    normal_count = 0

    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0

    all_results = []

    # ======================================================
    # 3. Read CSV in chunks
    # ======================================================

    try:

        # Make sure file starts from beginning
        file.file.seek(0)

        chunks = pd.read_csv(
            file.file,
            chunksize=CHUNK_SIZE
        )

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=f"Invalid CSV file: {error}"
        )

    # ======================================================
    # 4. Process each chunk
    # ======================================================

    try:

        for chunk_number, df_chunk in enumerate(
            chunks,
            start=1
        ):

            print(
                f"Processing chunk {chunk_number} "
                f"({len(df_chunk)} rows)..."
            )

            # ------------------------------------------------
            # Run ML prediction for this chunk
            # ------------------------------------------------

            results = predict_dataframe(
                df_chunk
            )

            # ------------------------------------------------
            # Create database objects
            # ------------------------------------------------

            events = []

            for result in results:

                event = SecurityEvent(

                    prediction=result["prediction"],

                    confidence=result["confidence"],

                    attack_probability=result[
                        "attack_probability"
                    ],

                    normal_probability=result[
                        "normal_probability"
                    ],

                    risk_level=result[
                        "risk_level"
                    ],

                    source=file.filename
                )

                events.append(event)

            # ------------------------------------------------
            # Add all events at once
            # ------------------------------------------------

            db.add_all(events)

            # Flush once for the whole chunk
            # instead of once for every row

            db.flush()

            # ------------------------------------------------
            # Create alerts
            # ------------------------------------------------

            alerts = []

            for event, result in zip(
                events,
                results
            ):

                if result["prediction"] == "Attack":

                    alert = Alert(

                        event_id=event.id,

                        severity=result[
                            "risk_level"
                        ],

                        title=(
                            "Potential Cybersecurity Attack"
                        ),

                        message=(
                            "An attack was detected with "
                            f"{result['attack_probability']}% "
                            "attack probability."
                        ),

                        status="OPEN"
                    )

                    alerts.append(alert)

            # ------------------------------------------------
            # Add alerts in batch
            # ------------------------------------------------

            if alerts:

                db.add_all(alerts)

            # ------------------------------------------------
            # Commit this chunk
            # ------------------------------------------------

            db.commit()

            # ------------------------------------------------
            # Update counters
            # ------------------------------------------------

            total_records += len(results)

            attack_count += sum(
                result["prediction"] == "Attack"
                for result in results
            )

            normal_count += sum(
                result["prediction"] == "Normal"
                for result in results
            )

            high_risk_count += sum(
                result["risk_level"] == "HIGH"
                for result in results
            )

            medium_risk_count += sum(
                result["risk_level"] == "MEDIUM"
                for result in results
            )

            low_risk_count += sum(
                result["risk_level"] == "LOW"
                for result in results
            )

            # Keep results for frontend
            all_results.extend(results)

            print(
                f"Completed chunk {chunk_number}. "
                f"Total processed: {total_records}"
            )

    except Exception as error:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Prediction or database error: {error}"
        )

    # ======================================================
    # 5. Return response
    # ======================================================

    return {

        "filename": file.filename,

        "total_records": total_records,

        "attack_count": attack_count,

        "normal_count": normal_count,

        "high_risk_count": high_risk_count,

        "medium_risk_count": medium_risk_count,

        "low_risk_count": low_risk_count,

        "results": all_results
    }