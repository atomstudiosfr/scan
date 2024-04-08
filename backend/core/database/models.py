from sqlalchemy import VARCHAR, DateTime, ForeignKey, Index, Integer, func, Boolean, NUMERIC, Column, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Address(Base):
    __tablename__ = "address"
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


class Mapping(Base):
    __tablename__ = "mapping"
    __table_args__ = (
        Index("mapping_newshareid_idx", "new_share_id"),
    )

    original_share_id = mapped_column(VARCHAR(50), primary_key=True, comment="AEFS unique id")
    new_share_id = mapped_column(ForeignKey("address.share_id", ondelete="SET NULL"))
    creation_date = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    last_updated_date = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    creation_user = mapped_column(VARCHAR(50), comment="creation user")
    last_updated_user = mapped_column(VARCHAR(50), comment="The last user that updated this record")
    to_delete = mapped_column(Boolean(), default=False, comment='Indicate if the mapping between original and corrected address is deleted')
    mapping = relationship("Address", foreign_keys=[new_share_id])


class ConfigCountryToProvider(Base):
    __tablename__ = "config_country_to_provider"
    __table_args__ = (
        Index("config_country_provider_idx", "provider_name"),
    )

    country_code = mapped_column(VARCHAR(2), primary_key=True, comment="Country ISO 3166 alpha 2 code.")
    provider_name = mapped_column(ForeignKey("provider.provider_name", ondelete="SET NULL"), primary_key=True)
    last_updated_date = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    max_calls_per_country = mapped_column(Integer, comment="number of maximum API calls allowed per day per country for auto " "correction")
    min_geocode_rank = mapped_column(Integer, comment="Minimum geocode rank to be eligible for autocorrection processing")
    max_geocode_rank = mapped_column(Integer, comment="Maximum geocode rank accepted from the provider to be saved in database")
    call_order = mapped_column(Integer, comment="Order to call the provider")
    provider = relationship("Provider", foreign_keys=[provider_name])
    enable_notification = mapped_column(Boolean(), default=True, comment="Enable notification (default is true)")

    def is_infinite_calls(self):
        return self.max_calls_per_country == -1

    def is_geocode_rank_acceptable_for_saving(self, geocode_rank):
        return self.max_geocode_rank >= geocode_rank

    def is_geocode_rank_acceptable_for_autocorrection_process(self, geocode_rank):
        return self.min_geocode_rank < geocode_rank

    def __str__(self):
        return f'CountryConfigToProvider<{self.country_code}, {self.provider_name}>'


class AutoCorrectionAllowedCities(Base):
    __tablename__ = "auto_correction_allowed_cities"

    country_code = mapped_column(VARCHAR(2), primary_key=True, comment="Country ISO 3166 alpha 2 code")
    city_name = mapped_column(VARCHAR(50), primary_key=True, comment="Name of the city")


class Provider(Base):
    __tablename__ = "provider"

    provider_name = mapped_column(VARCHAR(20), primary_key=True, comment="Provider name")
    max_search_bar_calls = mapped_column(Integer, comment="number of maximum API calls allowed from search bar per day")
    max_global_calls = mapped_column(Integer, comment="number of maximum API calls allowed per day globally")
    last_updated_date = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def is_infinite_calls(self):
        return self.max_global_calls == -1

    def is_infinite_max_search_bar_calls(self):
        return self.max_search_bar_calls == -1

    def __str__(self):
        return f'Provider<{self.provider_name}>'


class ProviderResult(Base):
    __tablename__ = "provider_result"
    __table_args__ = (
        Index('provider_result_idx', 'provider_name'),
    )

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    share_id = mapped_column(VARCHAR(50), nullable=True, comment="ShareID from SHARE for correction")
    provider_name = mapped_column(ForeignKey("provider.provider_name", ondelete="SET NULL"))
    xml_message = mapped_column(JSONB(none_as_null=True), comment='message data')
    creation_date = mapped_column(DateTime, default=func.now())
    provider = relationship("Provider", foreign_keys=[provider_name])


class AddressCorrectionRequest(Base):

    __tablename__ = 'address_correction_request'
    __table_args__ = (
        Index('acr_x01_trackid_shareid', 'parcel_id', 'share_id', 'requester', unique=True),
        Index('acr_x02_shareid', 'share_id'),
        Index('acr_x03_shareid_generated_sent', 'share_id', 'generated', 'sent'),
        Index('acr_x04_shareid_generated_requester', 'share_id', 'generated', 'requester'),
        Index('address_update_time_idx', 'updated_datetime'),
    )

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    unique_id = mapped_column(VARCHAR(50))
    parcel_id = mapped_column(VARCHAR(50))
    share_id = mapped_column(VARCHAR(50), nullable=False)
    geocode_rank = mapped_column(Integer, nullable=True)
    input_message = mapped_column(JSONB(none_as_null=True), comment='Message received by the application')
    output_message = mapped_column(JSONB(none_as_null=True), comment='Message sent to the external system')
    output_message_raw = mapped_column(Text, comment='raw message sent to the external system')
    output_datetime = mapped_column(DateTime, comment='Time when the message is generated')
    generated = mapped_column(Boolean(), default=False, comment='Indicate if the message has been generated')
    sent = mapped_column(Boolean(), default=False, comment='Indicate if the message has been sent to the external system')
    sent_datetime = mapped_column(DateTime, comment='Time when the message is sent to the external system')
    response_message = mapped_column(JSONB(none_as_null=True), comment='Response made by the external system')
    requester = mapped_column(VARCHAR(50), comment='Requester (AEFS, IROADS, ESTAR, ...)')
    geocode = mapped_column(VARCHAR(20), comment='The geocode region of the request')
    created_datetime = mapped_column(DateTime, default=func.now())
    updated_datetime = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class CountrySearchProvider(Base):
    __tablename__ = "country_search_provider"

    country_code = mapped_column(VARCHAR(2), primary_key=True, comment="Country ISO 3166 alpha 2 code.")
    provider_name = mapped_column(ForeignKey("provider.provider_name", ondelete="CASCADE"), primary_key=True)
    last_updated_date = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    provider = relationship("Provider", foreign_keys=[provider_name])


class AddressAccess(Base):
    __tablename__ = "address_access"
    __table_args__ = (
        Index('address_access_idx', 'last_access_date'),
    )

    original_share_id = mapped_column(VARCHAR(50), primary_key=True, comment="AEFS unique id")
    last_access_date = mapped_column(DateTime, default=func.now(), onupdate=func.now())
