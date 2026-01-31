from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.models.envelope import OnionooEnvelope


class ExitPolicySummary(BaseModel):
    """
    Summary version of an exit policy.

    Upstream provides either "accept" or "reject" (or both in edge cases).
    Values are TCP ports or port ranges as strings.
    """

    model_config = ConfigDict(extra="allow")

    accept: list[str] | None = Field(
        default=None,
        description=(
            "If present, the relay accepts these TCP ports/port ranges for most IP addresses "
            "and rejects all other ports."
        ),
    )
    reject: list[str] | None = Field(
        default=None,
        description=(
            "If present, the relay rejects these TCP ports/port ranges for most IP addresses "
            "and accepts all other ports."
        ),
    )


class DetailsRelay(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    nickname: str = Field(description="Relay nickname (1–19 alphanumerical characters).")
    fingerprint: str = Field(
        description="Relay fingerprint (40 upper-case hexadecimal characters)."
    )
    or_addresses: list[str] = Field(
        description="OR addresses (IP:port or port lists) where the relay accepts onion-routing."
    )
    dir_address: str | None = Field(
        default=None,
        description="Directory address (IPv4:port) where the relay accepts directory connections.",
    )
    exit_addresses: list[str] | None = Field(
        default=None,
        description="IPv4 exit addresses used by this relay in the past 24 hours (if any).",
    )

    last_seen: str = Field(
        description="UTC timestamp when this relay was last seen in a consensus."
    )
    last_changed_address_or_port: str = Field(
        description="UTC timestamp when this relay last changed its OR/dir address or port."
    )
    first_seen: str = Field(
        description="UTC timestamp when this relay was first seen in a consensus."
    )

    running: bool = Field(
        description="Whether this relay was listed as running in the last consensus."
    )
    hibernating: bool | None = Field(
        default=None,
        description=(
            "Whether the relay indicated it is hibernating in its last known server descriptor "
            "(if available)."
        ),
    )

    consensus_weight: int = Field(
        description=(
            "Consensus weight used in path selection (unit is arbitrary; currently ~KB/s)."
        )
    )

    # Common optional fields (many more exist; extra fields are allowed)
    flags: list[str] | None = Field(
        default=None, description="Relay flags assigned by the directory authorities."
    )
    country: str | None = Field(default=None, description="Two-letter country code from GeoIP.")
    country_name: str | None = Field(default=None, description="Country name from GeoIP.")
    region_name: str | None = Field(default=None, description="Region name from GeoIP.")
    city_name: str | None = Field(default=None, description="City name from GeoIP.")
    latitude: float | None = Field(default=None, description="Latitude from GeoIP.")
    longitude: float | None = Field(default=None, description="Longitude from GeoIP.")

    as_number: str | None = Field(
        default=None,
        validation_alias="as",
        serialization_alias="as",
        description="AS number string from AS database (e.g. 'AS1234').",
    )
    as_name: str | None = Field(default=None, description="AS name from AS database.")

    host_name: str | None = Field(
        default=None,
        description=(
            "Deprecated: reverse DNS host name for the relay's primary IP address "
            "(may be omitted if unknown)."
        ),
    )
    verified_host_names: list[str] | None = Field(
        default=None,
        description="Reverse DNS host names that could be verified via matching A records.",
    )
    unverified_host_names: list[str] | None = Field(
        default=None,
        description="Reverse DNS host names that could not be verified via matching A records.",
    )

    last_restarted: str | None = Field(
        default=None, description="UTC timestamp when the relay was last (re-)started (if known)."
    )

    bandwidth_rate: int | None = Field(
        default=None, description="Relay BandwidthRate (bytes per second), if known."
    )
    bandwidth_burst: int | None = Field(
        default=None, description="Relay BandwidthBurst (bytes per second), if known."
    )
    observed_bandwidth: int | None = Field(
        default=None, description="Observed relay bandwidth (bytes per second), if known."
    )
    advertised_bandwidth: int | None = Field(
        default=None,
        description="Advertised relay bandwidth (bytes per second), derived from rate/burst/observed.",
    )

    overload_general_timestamp: int | None = Field(
        default=None,
        description="Timestamp indicating relay overload state (OOM/ntor drop/port exhaustion), if any.",
    )

    exit_policy: list[str] | None = Field(default=None, description="Exit policy lines, if known.")
    exit_policy_summary: ExitPolicySummary | None = Field(
        default=None, description="Summary of exit policy for IPv4."
    )
    exit_policy_v6_summary: ExitPolicySummary | None = Field(
        default=None, description="Summary of exit policy for IPv6."
    )

    contact: str | None = Field(default=None, description="Relay operator contact line.")
    platform: str | None = Field(default=None, description="Platform string (OS and Tor version).")
    version: str | None = Field(
        default=None, description="Tor version without leading 'Tor' (from consensus), if known."
    )
    recommended_version: bool | None = Field(
        default=None, description="Whether the relay version is recommended (if known)."
    )
    version_status: str | None = Field(
        default=None,
        description=(
            "Version status (recommended/experimental/obsolete/new in series/unrecommended), if known."
        ),
    )

    effective_family: list[str] | None = Field(
        default=None,
        description="Fingerprints in effective (mutual) family. Includes own fingerprint.",
    )
    alleged_family: list[str] | None = Field(
        default=None, description="Fingerprints in alleged (non-mutual) family, if any."
    )
    indirect_family: list[str] | None = Field(
        default=None, description="Fingerprints in indirect family graph, if any."
    )

    consensus_weight_fraction: float | None = Field(
        default=None,
        description="Fraction of consensus weight compared to all relays (if running).",
    )
    guard_probability: float | None = Field(
        default=None, description="Approx. probability of being selected as guard (if available)."
    )
    middle_probability: float | None = Field(
        default=None, description="Approx. probability of being selected as middle (if available)."
    )
    exit_probability: float | None = Field(
        default=None, description="Approx. probability of being selected as exit (if available)."
    )
    measured: bool | None = Field(
        default=None, description="Whether consensus weight is based on bandwidth measurements."
    )

    unreachable_or_addresses: list[str] | None = Field(
        default=None,
        description="Declared OR addresses that some authorities found unreachable (if any).",
    )


class DetailsBridge(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    nickname: str = Field(description="Bridge nickname (1–19 alphanumerical characters).")
    hashed_fingerprint: str = Field(
        description="SHA-1 hash of the bridge fingerprint (40 upper-case hexadecimal characters)."
    )
    or_addresses: list[str] = Field(
        description=(
            "Sanitized OR addresses (IP:port or port lists). IPs are sanitized and not real bridge IPs."
        )
    )
    last_seen: str = Field(
        description="UTC timestamp when this bridge was last seen in bridge status."
    )
    first_seen: str = Field(
        description="UTC timestamp when this bridge was first seen in bridge status."
    )
    running: bool = Field(
        description=(
            "Whether this bridge was successfully tested by bridgestrap, or listed as running if untested."
        )
    )

    flags: list[str] | None = Field(
        default=None, description="Bridge flags assigned by the bridge authority."
    )
    last_restarted: str | None = Field(
        default=None, description="UTC timestamp when the bridge was last (re-)started (if known)."
    )
    advertised_bandwidth: int | None = Field(
        default=None, description="Advertised bandwidth (bytes per second), if known."
    )
    overload_general_timestamp: int | None = Field(
        default=None,
        description="Timestamp indicating bridge overload state (OOM/ntor drop/port exhaustion), if any.",
    )
    platform: str | None = Field(default=None, description="Platform string (OS and Tor version).")
    version: str | None = Field(
        default=None, description="Tor version without leading 'Tor' (from descriptor), if known."
    )
    recommended_version: bool | None = Field(
        default=None, description="Whether the bridge version is recommended (if known)."
    )
    version_status: str | None = Field(
        default=None,
        description=(
            "Version status (recommended/experimental/obsolete/new in series/unrecommended), if known."
        ),
    )
    transports: list[str] | None = Field(
        default=None, description="Supported pluggable transports."
    )
    blocklist: list[str] | None = Field(
        default=None,
        description="Country codes where this bridge is not served because it is believed to be blocked.",
    )
    bridgedb_distributor: str | None = Field(
        default=None,
        validation_alias="bridgedb_distributor",
        description="BridgeDB distributor this bridge is assigned to (if any).",
    )
    contact: str | None = Field(default=None, description="Bridge operator contact line.")


class DetailsResponse(OnionooEnvelope[DetailsRelay, DetailsBridge]):
    pass
