from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Annotations(BaseModel):
    facet: Optional[bool] = None
    facetsort: Optional[str] = None
    disjunctive: Optional[bool] = None
    sortable: Optional[bool] = None

class FieldModel(BaseModel):
    name: str
    description: Optional[str] = None
    annotations: Annotations
    label: str
    type: str

class DCAT(BaseModel):
    created: Optional[str] = None
    issued: Optional[str] = None
    creator: Optional[str] = None
    contributor: Optional[str] = None
    contact_name: str
    contact_email: str
    accrualperiodicity: Optional[str] = None
    spatial: Optional[str] = None
    temporal: Optional[str] = None
    granularity: Optional[str] = None
    dataquality: Optional[str] = None
    publisher_type: Optional[str] = None
    conforms_to: Optional[str] = None
    temporal_coverage_start: Optional[str] = None
    temporal_coverage_end: Optional[str] = None
    accessRights: Optional[str] = None
    relation: Optional[str] = None

class Semantic(BaseModel):
    rml_mapping: Optional[str] = None
    classes: Optional[str] = None
    properties: Optional[str] = None

class DCATAPIT(BaseModel):
    publisher_id: Optional[str] = None

class Default(BaseModel):
    title: str
    description: str
    theme: List[str]
    keyword: Optional[str] = None
    license: str
    license_url: str
    language: str
    metadata_languages: List[str]
    timezone: str
    modified: str
    modified_updates_on_metadata_change: bool
    modified_updates_on_data_change: bool
    data_processed: str
    metadata_processed: str
    geographic_reference: Optional[str] = None
    geographic_reference_auto: bool
    territory: Optional[str] = None
    geometry_types: Optional[str] = None
    bbox: Optional[str] = None
    publisher: Optional[str] = None
    references: str
    records_count: int
    attributions: Optional[str] = None
    source_domain: Optional[str] = None
    source_domain_title: Optional[str] = None
    source_domain_address: Optional[str] = None
    source_dataset: Optional[str] = None
    shared_catalog: Optional[str] = None
    federated: bool
    oauth_scope: Optional[str] = None
    parent_domain: Optional[str] = None
    update_frequency: Optional[str] = None

class Metas(BaseModel):
    dcat: DCAT
    semantic: Semantic
    dcat_ap_it: DCATAPIT
    default: Default

class DatasetResponse(BaseModel):
    visibility: str
    dataset_id: str
    dataset_uid: str
    has_records: bool
    features: List[str]
    attachments: List[Any]
    alternative_exports: List[Any]
    data_visible: bool
    fields: List[FieldModel]
    metas: Metas
