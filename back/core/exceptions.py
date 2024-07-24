import logging
from typing import Any

from fastapi import HTTPException


class AEFSFailToUpdateAddressException(Exception):
    pass


class JMSNoReprocessException(Exception):
    pass


class BaseHTTPException(HTTPException):
    message: str = ''
    field: str = ''
    status: str = 'warning'
    status_code: int = 409
    info: str = ''

    def __init__(self, info: Any = None) -> None:
        if info:
            self.info = info
        logging.error(f'BUSINESS-ERROR - "message": {self.message}, "status": {self.status}, "field": {self.field}, "info": {self.info}')
        super().__init__(
            status_code=self.status_code, detail={"message": self.message, "status": self.status, "field": self.field, "info": self.info},
            headers=None
        )


class AEFSUnavailable(BaseHTTPException):
    status_code = 500
    message = 'AEFS service is unavailable'
    status = 'error'
    info = 'AEFS service is not currently available, the address has not been corrected. Please retry in a moment'


class NotAuthorizedUserException(BaseHTTPException):
    status_code = 401
    message = "Action not authorized"
    info = 'You don\'t have the role to process this action Change (check role on image?)'


class AEFSCannotValidateAddress(BaseHTTPException):
    status_code = 503
    message = f"AEFS cannot validate the address"
    info = 'Address you send seems to be invalid according to AEFS'


class AEFSIsDown(BaseHTTPException):
    status_code = 503
    message = f"AEFS is down"
    info = 'AEFS process is currently not available due to technical issues'


class AEFSMaxCallReached(BaseHTTPException):
    status_code = 503
    message = f"Max calls to AEFS has been reached"
    info = 'Error call limit reached'


class SameAddress(BaseHTTPException):
    message = f"You need to change a least one field of the address"
    info = ('you cannot save the address if this correction is already existing we the same data pls change one or more of'
            ' the filed to save properly or keep it that way and weep the already corrected data')


class MaxSearchBarCallReached(BaseHTTPException):
    status_code = 403
    message = f"Max calls to provider or search bar have been reached"
    info = 'Error call limit reached'


class ProviderNotKnown(BaseHTTPException):
    status_code = 403
    message = f"Provider not config in the code but is in the database please contact the SIMBA team"
    info = 'A problem with the config as occurred it will not work until there a is a correction on that'


class MaxCallForCountryReached(BaseHTTPException):
    status_code = 403
    message = f"Max calls to config country have been reached"
    info = 'Error call limit reached'


class InvalidPostalCode(BaseHTTPException):
    status_code = 409
    message = f"Wrong postal code format"
    field = "postal_cd"


class InvalidLatitude(BaseHTTPException):
    status_code = 409
    message = f"Lat,Lon is mandatory and must be corrected"
    field = "latitude"


class InvalidCityName(BaseHTTPException):
    status_code = 409
    message = f"City name is mandatory"
    field = "city_nm"


class InvalidStreetLine1(BaseHTTPException):
    status_code = 409
    message = f"Street line 1 is mandatory"
    field = "street_line_1"


class InvalidCountryCode(BaseHTTPException):
    status_code = 409
    message = f"the country code is not the same as the original"
    field = "country_cd"


class NoCorrectedAddressFound(BaseHTTPException):
    status_code = 204
    message = "No Corrected Address found"


class NoAddressFromProvider(BaseHTTPException):
    status_code = 204
    message = "No Address found for the provider"


class NotAllowedToCallAEFS(BaseHTTPException):
    status_code = 403
    message = "AEFS limit has been reached. Please wait tomorrow to call AEFS"


class NotAllowedToCallGoogle(BaseHTTPException):
    status_code = 403
    message = "GOOGLE limit has been reached. Please wait tomorrow to call GOOGLE"


class NotAllowedToCallArcGIS(BaseHTTPException):
    status_code = 403
    message = "ArcGIS limit has been reached. Please wait tomorrow to call ArcGIS"


class NotAllowedToCallFindr(BaseHTTPException):
    status_code = 403
    message = "FINDR limit has been reached. Please wait tomorrow to call FINDR"


class NoReverseGeocodingAvailable(BaseHTTPException):
    status_code = 204
    message = "No reverse geocoding available"
