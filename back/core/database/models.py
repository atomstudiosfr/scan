from sqlalchemy import VARCHAR, DateTime, ForeignKey, Index, Integer, func, Boolean, NUMERIC, Column, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "book"
    __table_args__ = (
        Index("address_multi_criteria_idx", "street_line1_desc", "city_nm", "postal_cd", "contact_nm", "company_nm"),
        Index('address_idx1_corrected_by_country_cd_last_updated_user', 'corrected_by', 'country_cd', 'last_updated_user'),
    )

    share_id = mapped_column(VARCHAR(50), primary_key=True, comment="Unique id of the corrected address")
    street_line1_desc = mapped_column(VARCHAR(150), comment="Street address line 1")
    street_line2_desc = mapped_column(VARCHAR(150), comment="Street address line 2")
    street_line3_desc = mapped_column(VARCHAR(150), comment="Street address line 3")
    street_line4_desc = mapped_column(VARCHAR(150), comment="Street address line 4")
    city_nm = mapped_column(VARCHAR(50), comment="City name")
    postal_cd = mapped_column(VARCHAR(20), comment="Postal code")
    country_cd = mapped_column(VARCHAR(2), comment="Country ISO 3166 alpha 2 code")
    geocode_rank = mapped_column(Integer, comment="Geo Rank")
    latitude = mapped_column(NUMERIC(11, 8), default=0.0, comment="Latitude of the corrected address")
    longitude = mapped_column(NUMERIC(11, 8), default=0.0, comment="Longitude of the corrected address")
    street_number = mapped_column(VARCHAR(50), nullable=True, comment="Street house number")
    street_name = mapped_column(VARCHAR(50), nullable=True, comment="Street name")
    urban_cd = mapped_column(VARCHAR(50), nullable=True, comment="Detail of urban code")
    state_prov_cd = mapped_column(VARCHAR(50), nullable=True, comment="State or province code")
    contact_nm = mapped_column(VARCHAR(50), nullable=True, comment="Package recipient or contact name")
    company_nm = mapped_column(VARCHAR(100), nullable=True, comment="Package receiving company name")
    phone_number = mapped_column(VARCHAR(20), nullable=True, comment="Phone number corresponding to this address")
    street_side = mapped_column(VARCHAR(10), nullable=True, comment="The side of the street")
    segment_id = mapped_column(VARCHAR(20), nullable=True, comment="AEFS geo segment id")
    last_updated_date = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    creation_date = mapped_column(DateTime, default=func.now())
    creation_user = mapped_column(VARCHAR(50), comment="The user at the origin of the creation")
    corrected_by = mapped_column(VARCHAR(50),
                                 comment="Indicate by which provider a correction has been made (USER, AEFS, GOOGLE, ARCGIS, ...)")
    last_updated_user = mapped_column(VARCHAR(50), comment="The last user that updated this record")
    correction_stop_type = mapped_column(VARCHAR(500), comment="Address correction stop type")
    aefs_address_type_cd = mapped_column(VARCHAR(50), nullable=True, comment="AEFS Address Type")
    aefs_state = mapped_column(VARCHAR(50), nullable=True, comment="AEFS Address State")
    aefs_raw_address_id = mapped_column(VARCHAR(50), nullable=True, comment="AEFS Raw AddressID")
    aefs_geocode_rank = mapped_column(Integer, nullable=True, comment="AEFS Geocode rank")
    aefs_latitude = mapped_column(NUMERIC(11, 8), nullable=True, comment="AEFS latitude")
    aefs_longitude = mapped_column(NUMERIC(11, 8), nullable=True, comment="AEFS longitude")

