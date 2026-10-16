from django.conf import settings


# 템플릿에서 지도·경로 API 키를 쓸 수 있게 넘겨준다 (값은 환경변수에서 읽음)
def api_keys(request):
    return {
        'kakao_js_key': settings.KAKAO_JS_KEY,
        'tmap_app_key': settings.TMAP_APP_KEY,
    }
