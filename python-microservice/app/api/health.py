"""
Health Check Endpoints
Kubernetes-compatible liveness and readiness probes
"""
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import psutil
import time

router = APIRouter()

start_time = time.time()


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness():
    """
    Liveness probe - indicates if the application is running
    """
    return {"status": "alive", "timestamp": time.time()}


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness():
    """
    Readiness probe - indicates if the application is ready to serve traffic
    """
    # Add checks for dependencies (database, cache, etc.)
    checks = {
        "database": await check_database(),
        "cache": await check_cache(),
    }
    
    all_healthy = all(checks.values())
    
    if all_healthy:
        return {
            "status": "ready",
            "checks": checks,
            "timestamp": time.time()
        }
    else:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "checks": checks,
                "timestamp": time.time()
            }
        )


@router.get("/metrics/health", status_code=status.HTTP_200_OK)
async def health_metrics():
    """
    Detailed health metrics
    """
    uptime = time.time() - start_time
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    return {
        "uptime_seconds": uptime,
        "cpu_usage_percent": cpu_percent,
        "memory_usage_percent": memory.percent,
        "memory_available_mb": memory.available / (1024 * 1024),
        "timestamp": time.time()
    }


async def check_database() -> bool:
    """Check database connectivity"""
    try:
        # Implement actual database check
        # Example: await database.execute("SELECT 1")
        return True
    except Exception:
        return False


async def check_cache() -> bool:
    """Check cache connectivity"""
    try:
        # Implement actual cache check
        # Example: await redis.ping()
        return True
    except Exception:
        return False