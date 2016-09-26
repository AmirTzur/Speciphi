import re
from mobileesp import mdetect


class MobileDetectionMiddleware(object):
    """
    Useful middleware to detect if the user is
    on a mobile device.
    """

    def process_request(self, request):
        is_tablet = False
        is_phone = False
        is_mobile = False
        is_desktop = False
        is_ios = False
        is_android = False
        is_symbian = False
        is_windows = False
        is_blackberry = False
        is_palm = False
        is_opera = False
        device_type = ''

        user_agent = request.META.get("HTTP_USER_AGENT")
        http_accept = request.META.get("HTTP_ACCEPT")
        if user_agent and http_accept:
            agent = mdetect.UAgentInfo(userAgent=user_agent, httpAccept=http_accept)
            is_tablet = agent.detectTierTablet()
            is_phone = agent.detectTierIphone()
            is_mobile = is_tablet or is_phone or agent.detectMobileQuick()
            is_desktop = not is_mobile
            is_ios = agent.detectIos()
            is_android = agent.detectAndroid()
            is_symbian = agent.detectSymbianOS()
            is_windows = agent.detectWindowsPhone() or agent.detectWindowsMobile()
            is_blackberry = agent.detectBlackBerry()
            is_palm = agent.detectPalmOS() or agent.detectPalmWebOS()
            is_opera = agent.detectOperaMobile()

        if is_mobile:
            device_type += 'mobile, '
        if is_tablet:
            device_type += 'tablet, '
        if is_phone:
            device_type += 'phone, '
        if is_desktop:
            device_type += 'desktop, '
        if is_ios:
            device_type += 'ios, '
        if is_android:
            device_type += 'android, '
        if is_symbian:
            device_type += 'symbian, '
        if is_windows:
            device_type += 'windows, '
        if is_blackberry:
            device_type += 'blackberry, '
        if is_palm:
            device_type += 'palm, '
        if is_opera:
            device_type += 'opera, '

        request.device_type = device_type
