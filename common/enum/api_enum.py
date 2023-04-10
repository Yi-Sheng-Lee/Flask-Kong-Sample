from enum import Enum

web_80 = ''.join(['h', 't', 't', 'p'])
web_443 = ''.join(['h', 't', 't', 'p', 's'])


class OtxApiUrl(Enum):
    OTX_MALWARE = web_443 + "://otx.alienvault.com/otxapi/malware?days=1&limit=50&dashboard=1"
    OTX_INDICATORS = web_443 + "://otx.alienvault.com/otxapi/indicators?days=1&limit=50&dashboard=1"
    OTX_SUBSCRIBE_PULSES = web_443 + "://otx.alienvault.com/api/v1/pulses/subscribed"
    OTX_PULSES_DETAIL = web_443 + "://otx.alienvault.com/api/v1/pulses/{pulses_id}"
    OTX_RELATED = web_443 + "://otx.alienvault.com/api/v1/pulses"
    OTX_INDICATOR_LIST = web_443 + "://otx.alienvault.com/otxapi/indicators/?type={type}&include_inactive=0&sort=-modified&q=&page={page}&limit={limit}"
    OTX_MALWARE_PULSES_LIST = web_443 + "://otx.alienvault.com/otxapi/pulses/related?malware_family={malware}&sort=-created&page={page}&limit={limit}"
    OTX_INDICATOR_DETAIL = web_443 + "://otx.alienvault.com/otxapi/indicators/{type}/general/{ioc}"


class LogMasterApiUrl(Enum):
    EPS = web_80 + "://%s/rest/lm/v1.0/EPS"


class AlienVaultApi(Enum):
    ASSET_LIST = web_443 + "://{url}/ossim/av_asset/asset/providers/load_assets_info.php?func=list"
    ASSET_INFO = web_443 + "://{url}/ossim/av_asset/asset/providers/load_assets_info.php?func=device&from=0&maxrows=100&id={asset_id}"


class IsacWizardApi(Enum):
    DEVICES_DATA = web_80 + "://{url}/api/1.0/openapi/company/devices"
    DASHBOARD_DATA_STATS = web_80 + "://{url}/api/1.0/info-center/dashboard/stats/{type}"
    OTX_INDICATORS = web_80 + "://{url}/api/1.0/info-center/dashboard/indicators/{type}"
    OTX_INDICATOR_DETAIL = web_80 + "://{url}/api/1.0/info-center/dashboard/indicator/{type}"
    OTX_MALWARE_PULSES = web_80 + "://{url}/api/1.0/info-center/dashboard/pulses/malware"
    OTX_PULSES_DETAIL = web_80 + "://{url}/api/1.0/info-center/dashboard/pulses/{pulses_id}"
    INFO_PULSES_RELATED_OTX = web_80 + "://{url}/api/1.0/info-center/related/{pid}"
    REGION_DEVICE_DASHBOARD = web_80 + "://{url}/api/1.0/openapi/company/devices/region"
    SENSOR_DEVICE_DASHBOARD = web_80 + "://{url}/api/1.0/openapi/company/devices/sensor/{uid}"
    DEVICE_REGION_DASHBOARD = web_80 + "://{url}/api/1.0/info-center/dashboard/ot/factory"
    DEVICE_STATUS_INFO = web_80 + "://{url}/api/1.0/info-center/dashboard/ot/device/{uid}"


class KongApi(Enum):
    CONSUMER = web_80 + "://{url}:8001/consumers"
    CONSUMER_JWT = web_80 + "://{url}:8001/consumers/{consumer}/jwt"
