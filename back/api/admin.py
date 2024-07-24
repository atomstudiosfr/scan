from sqladmin import Admin, ModelView

from core.database.models import (
    Address,
    ConfigCountryToProvider,
    Mapping,
    Provider,
    ProviderResult,
    CountrySearchProvider, AddressCorrectionRequest, AutoCorrectionAllowedCities,
)


def add(app, engine):
    admin = Admin(app, engine)

    class EditingMixin:
        can_create = False
        can_edit = False
        can_delete = False

    class AddressAdmin(EditingMixin, ModelView, model=Address):
        column_list = Address.__table__.columns.keys()
        column_searchable_list = [Address.share_id, Address.city_nm, Address.company_nm, Address.contact_nm]
        name = "Address"
        name_plural = "Addresses"
        icon = "fa-solid fa-map"

    class AddressCorrectionRequestAdmin(EditingMixin, ModelView, model=AddressCorrectionRequest):
        column_list = AddressCorrectionRequest.__table__.columns.keys()
        column_searchable_list = [Address.share_id, Address.city_nm, Address.company_nm, Address.contact_nm]
        name = "Address Correction Request"
        name_plural = "Address Correction Requests"
        icon = "fa-solid fa-map"

    class AutoCorrectionAllowedCitiesAdmin(EditingMixin, ModelView, model=AutoCorrectionAllowedCities):
        column_list = AutoCorrectionAllowedCities.__table__.columns.keys()
        column_searchable_list = [AutoCorrectionAllowedCities.country_code, AutoCorrectionAllowedCities.city_name]
        name = "Auto Correction - Allowed Cities"
        name_plural = "Auto Correction - Allowed Cities"
        icon = "fa-solid fa-map"

    class MappingAdmin(EditingMixin, ModelView, model=Mapping):
        column_list = Mapping.__table__.columns.keys()
        column_searchable_list = [Mapping.original_share_id, Mapping.new_share_id]
        name = "Mapping"
        name_plural = "Mappings"
        icon = "fa-solid fa-link"

    class ConfigCountryToProviderAdmin(EditingMixin, ModelView, model=ConfigCountryToProvider):
        column_list = ConfigCountryToProvider.__table__.columns.keys()
        column_searchable_list = [ConfigCountryToProvider.country_code]
        name = "ConfigCountryToProvider"
        name_plural = "ConfigCountryToProvider"
        icon = "fa-solid fa-earth-americas"

    class ProviderAdmin(EditingMixin, ModelView, model=Provider):
        column_list = Provider.__table__.columns.keys()
        column_searchable_list = [Provider.provider_name]
        name = "Provider"
        name_plural = "Providers"
        icon = "fa-solid fa-paper-plane"

    class ProviderResultAdmin(EditingMixin, ModelView, model=ProviderResult):
        column_list = ProviderResult.__table__.columns.keys()
        column_searchable_list = [ProviderResult.provider_name, ProviderResult.share_id]
        name = "ProviderResult"
        name_plural = "ProviderResults"
        icon = "fa-solid fa-square-poll-horizontal"

    class CountrySearchProviderAdmin(EditingMixin, ModelView, model=CountrySearchProvider):
        column_list = CountrySearchProvider.__table__.columns.keys()
        column_searchable_list = [CountrySearchProvider.country_code]
        name = "CountrySearchProvider"
        name_plural = "CountrySearchProvider"
        icon = "fa-solid fa-paper-plane"

    admin.add_view(AddressAdmin)
    admin.add_view(AddressCorrectionRequestAdmin)
    admin.add_view(AutoCorrectionAllowedCitiesAdmin)
    admin.add_view(MappingAdmin)
    admin.add_view(ConfigCountryToProviderAdmin)
    admin.add_view(ProviderAdmin)
    admin.add_view(ProviderResultAdmin)
    admin.add_view(CountrySearchProviderAdmin)
