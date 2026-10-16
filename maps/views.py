from django.shortcuts import render


# 지도 표시
def display_map(request):
    return render(request, 'maps/kakao_maps.html')
