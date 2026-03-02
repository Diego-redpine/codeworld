"""Supabase data source for Red Pine business metrics.

Connects to Supabase for live customer/revenue data.
Falls back to config values when no credentials are provided.
Can auto-discover credentials from redpine-os .env files.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from towns.metrics import RedPineMetrics, CustomerRecord

log = logging.getLogger(__name__)


def load_env_from_project(project_path: str) -> dict[str, str]:
    """Read Supabase credentials from a redpine-os project's .env files.

    Checks dashboard/.env.local first, then onboarding/.env.
    Returns dict with 'url' and 'key' if found.
    """
    env_files = [
        Path(project_path) / "dashboard" / ".env.local",
        Path(project_path) / "onboarding" / ".env",
    ]

    result = {}
    for env_file in env_files:
        if not env_file.exists():
            continue
        try:
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")

                if key == "NEXT_PUBLIC_SUPABASE_URL" and "url" not in result:
                    result["url"] = value
                elif key == "NEXT_PUBLIC_SUPABASE_ANON_KEY" and "key" not in result:
                    result["key"] = value
        except OSError:
            continue

        # Stop as soon as we have both
        if "url" in result and "key" in result:
            break

    return result


class RedPineDataSource:
    """Fetches Red Pine business data from Supabase with local fallback."""

    def __init__(self, url: str | None, key: str | None, fallback: dict):
        self._url = url
        self._key = key
        self._fallback = fallback
        self._client = None

        if url and key:
            try:
                from supabase import create_client
                self._client = create_client(url, key)
                log.info("Connected to Supabase")
            except ImportError:
                log.warning("supabase-py not installed, using fallback data")
            except Exception as e:
                log.warning(f"Supabase connection failed: {e}")

    @property
    def connected(self) -> bool:
        return self._client is not None

    async def fetch_metrics(self) -> RedPineMetrics:
        """Fetch metrics from Supabase, falling back to config."""
        if self._client is not None:
            try:
                customers = self._query_customers()
                revenue = self._query_revenue()
                agents = self._query_active_agents()
                return RedPineMetrics(
                    revenue=revenue,
                    customer_count=len(customers),
                    customers=customers,
                    active_agents=agents,
                )
            except Exception as e:
                log.warning(f"Supabase query failed: {e}")

        # Fallback to config values
        return RedPineMetrics(
            revenue=float(self._fallback.get("revenue", 0)),
            customer_count=int(self._fallback.get("customers", 0)),
        )

    def fetch_metrics_sync(self) -> RedPineMetrics:
        """Synchronous version of fetch_metrics."""
        if self._client is not None:
            try:
                customers = self._query_customers()
                revenue = self._query_revenue()
                agents = self._query_active_agents()
                return RedPineMetrics(
                    revenue=revenue,
                    customer_count=len(customers),
                    customers=customers,
                    active_agents=agents,
                )
            except Exception as e:
                log.warning(f"Supabase query failed: {e}")

        return RedPineMetrics(
            revenue=float(self._fallback.get("revenue", 0)),
            customer_count=int(self._fallback.get("customers", 0)),
        )

    def _query_customers(self) -> list[CustomerRecord]:
        """Query customer records from Supabase contacts table."""
        if self._client is None:
            return []
        try:
            response = self._client.table("contacts").select(
                "id, type, name, status, created_at"
            ).execute()
            return [
                CustomerRecord(
                    business_id=str(row.get("id", "")),
                    business_type=row.get("type", "other"),
                    name=row.get("name", "Unknown"),
                    status=row.get("status", "active"),
                    created_at=row.get("created_at", ""),
                )
                for row in (response.data or [])
            ]
        except Exception as e:
            log.warning(f"Customer query failed: {e}")
            return []

    def _query_revenue(self) -> float:
        """Query revenue from paid invoices in Supabase."""
        if self._client is None:
            return 0.0
        try:
            response = self._client.table("invoices").select(
                "amount_cents"
            ).eq("status", "paid").execute()
            # amount_cents → dollars
            return sum(row.get("amount_cents", 0) for row in (response.data or [])) / 100.0
        except Exception as e:
            log.warning(f"Revenue query failed: {e}")
            return float(self._fallback.get("revenue", 0))

    def _query_active_agents(self) -> int:
        """Query count of active AI agent subscriptions."""
        if self._client is None:
            return 0
        try:
            response = self._client.table("agent_subscriptions").select(
                "id", count="exact"
            ).eq("status", "active").execute()
            return response.count or 0
        except Exception as e:
            log.warning(f"Agent subscription query failed: {e}")
            return 0
