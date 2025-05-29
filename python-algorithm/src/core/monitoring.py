import time
import functools
from typing import Callable, Dict, Any, Optional

from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Prometheus metrics
REQUEST_COUNT = Counter(
    "recommendation_request_total", 
    "Total number of recommendation requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "recommendation_request_latency_seconds",
    "Request latency in seconds",
    ["method", "endpoint"]
)

RECOMMENDATION_COUNT = Counter(
    "recommendations_generated_total",
    "Total number of recommendations generated",
    ["algorithm_version", "user_segment"]
)

CACHE_HIT = Counter(
    "cache_hit_total",
    "Total number of cache hits",
    ["cache_type"]
)

CACHE_MISS = Counter(
    "cache_miss_total",
    "Total number of cache misses",
    ["cache_type"]
)

# OpenTelemetry configuration placeholder
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.semconv.resource import ResourceAttributes
    
    HAVE_OPENTELEMETRY = True
except ImportError:
    HAVE_OPENTELEMETRY = False


def setup_monitoring(app: FastAPI):
    """
    Set up monitoring for the FastAPI application.
    """
    # Add Prometheus metrics endpoint
    @app.get("/metrics")
    async def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    
    # Setup request middleware for global request tracking
    @app.middleware("http")
    async def monitor_requests(request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        return response
    
    # Setup OpenTelemetry if available and enabled
    if HAVE_OPENTELEMETRY:
        from src.core.config import settings
        
        if settings.ENABLE_OPENTELEMETRY and settings.OTEL_EXPORTER_OTLP_ENDPOINT:
            resource = Resource(attributes={
                ResourceAttributes.SERVICE_NAME: settings.PROJECT_NAME
            })
            
            provider = TracerProvider(resource=resource)
            trace.set_tracer_provider(provider)
            
            # Configure exporter based on environment variables
            if settings.OTEL_EXPORTER_OTLP_ENDPOINT:
                from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
                
                otlp_exporter = OTLPSpanExporter(
                    endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT,
                    insecure=True,
                )
                span_processor = BatchSpanProcessor(otlp_exporter)
                provider.add_span_processor(span_processor)


def track_request(func: Callable) -> Callable:
    """
    Decorator to track individual endpoint requests with more detail.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Extract user_id and algorithm_version if available in kwargs
        user_id = kwargs.get("user_id", "unknown")
        algorithm_version = kwargs.get("algorithm_version", "v1")
        
        # Create span if OpenTelemetry is available
        if HAVE_OPENTELEMETRY:
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(func.__name__) as span:
                span.set_attribute("user_id", user_id)
                span.set_attribute("algorithm_version", algorithm_version)
                
                result = await func(*args, **kwargs)
                
                # Add result metadata to span
                if isinstance(result, dict) and "recommendations" in result:
                    span.set_attribute("recommendation_count", len(result["recommendations"]))
        else:
            result = await func(*args, **kwargs)
        
        # Record execution time
        duration = time.time() - start_time
        
        # Custom detailed metrics
        user_segment = "premium" if user_id.startswith("prem_") else "standard"
        RECOMMENDATION_COUNT.labels(
            algorithm_version=algorithm_version,
            user_segment=user_segment
        ).inc()
        
        return result
    
    return wrapper


def track_cache(cache_type: str = "default"):
    """
    Decorator to track cache hits and misses.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # First argument is expected to be the cache key
            result = func(*args, **kwargs)
            
            if result is not None:
                CACHE_HIT.labels(cache_type=cache_type).inc()
            else:
                CACHE_MISS.labels(cache_type=cache_type).inc()
            
            return result
        
        return wrapper
    
    return decorator

