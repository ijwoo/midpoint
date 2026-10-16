# Midpoint — 중간지점 찾기

여러 명의 출발지를 입력하면 모두의 한가운데에 있는 지하철역·기차역·버스터미널을 찾아 주는 웹 서비스입니다.
출발지마다 그 거점까지 걸리는 시간과 요금을 한 화면에서 비교할 수 있습니다.

2023년에 처음 만들었고, 2025년에 AI 도구의 도움을 받아 UI를 다시 정리했습니다.

- 데모: https://midpoint-eight.vercel.app
- 프로젝트 소개: https://imjaewoo.dev/work/midpoint

## 주요 기능

- **중간지점 계산** — 최대 5개 출발지의 좌표 평균으로 중간 지점을 구합니다.
- **교통 거점 탐색** — 중간 지점 10km 이내에서 지하철역 → 기차역 → 버스터미널 순으로 찾습니다.
- **근거리 예외 처리** — 모든 출발지가 중간 지점에서 2km 이내면 교통 거점 대신 중간 지점을 보여 주고 "이 근처에서 만나보세요"라고 안내합니다.
- **대중교통 경로** — 각 출발지에서 중간 거점까지의 소요 시간과 요금을 보여 주고, 경로를 지도 위에 선으로 그립니다 (SK T맵 API).
- **모달 장소 검색** — 출발지 입력칸을 누르면 카카오 장소 검색 모달에서 바로 고를 수 있습니다.
- **현재 위치 추가** — GPS로 받은 내 위치를 주소로 바꿔 입력합니다.
- **사이드바 장소 검색** — 키워드로 검색한 뒤 "출발지로 지정" 버튼으로 바로 추가합니다.
- **모바일 최적화** — 하단 시트 패널, 44px 터치 영역, iOS 입력 확대 방지를 적용했습니다.

## 기술 스택

| 구분 | 기술 |
|---|---|
| Backend | Python 3.11, Django 4.2 |
| Frontend | HTML5, CSS3, Vanilla JS |
| Map / 검색 | Kakao Maps JavaScript SDK (services 라이브러리) |
| Transit | SK T맵 대중교통 API |
| Static | WhiteNoise |
| Infra | Vercel |

## 동작 방식

1. 입력한 출발지들을 카카오맵 SDK로 좌표로 바꾸고, 좌표의 평균을 중간 지점으로 삼습니다.
2. 중간 지점 반경 10km 안에서 지하철역, 기차역, 버스터미널 순서로 검색해 처음 찾은 곳을 만날 장소로 정합니다.
3. 출발지별 경로를 T맵 대중교통 API에 `Promise.all`로 동시에 요청해 기다리는 시간을 줄이고, 소요 시간·요금과 경로를 지도에 표시합니다.

Django는 지도 페이지를 렌더링하고, 환경변수의 API 키를 템플릿에 `window.MIDPOINT_CONFIG`로 넘기는 역할을 합니다.
배포는 Vercel 서버리스 함수 위에서 이루어지며, 정적 파일도 WhiteNoise가 함께 서빙합니다.

## 로컬 실행

### 1. 가상환경과 의존성

macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. 환경변수

`.env.example`에 필요한 변수가 정리되어 있습니다.

| 변수 | 설명 |
|---|---|
| `SECRET_KEY` | Django 시크릿 키입니다. 운영(`DEBUG=False`)에서는 반드시 필요합니다. |
| `DEBUG` | 로컬에서는 `True`로 둡니다. `True`이면 `SECRET_KEY`가 없어도 개발용 키로 실행됩니다. |
| `KAKAO_JS_KEY` | 카카오 디벨로퍼스의 JavaScript 키입니다. 앱 설정의 Web 플랫폼에 `http://localhost:8000`을 등록해야 지도가 뜹니다. |
| `TMAP_APP_KEY` | SK open API의 T맵 대중교통 appKey입니다. |

macOS / Linux

```bash
export DEBUG=True
export KAKAO_JS_KEY=발급받은_JavaScript_키
export TMAP_APP_KEY=발급받은_T맵_appKey
```

Windows (PowerShell)

```powershell
$env:DEBUG="True"
$env:KAKAO_JS_KEY="발급받은_JavaScript_키"
$env:TMAP_APP_KEY="발급받은_T맵_appKey"
```

### 3. 서버 실행

```bash
python manage.py runserver
```

`http://localhost:8000`에 접속하면 지도 화면으로 이동합니다.

## 배포 (Vercel)

- `vercel.json`이 `myproject/wsgi.py`를 Python 함수로 빌드하고 모든 요청을 그쪽으로 보냅니다.
- Vercel 프로젝트의 Settings → Environment Variables에 `SECRET_KEY`, `KAKAO_JS_KEY`, `TMAP_APP_KEY`를 등록합니다.
- `collectstatic` 결과물은 저장소에 넣지 않습니다. `WHITENOISE_USE_FINDERS = True` 설정으로 WhiteNoise가 앱의 `static/` 폴더에서 바로 서빙합니다.

## 구조

```
.
├── maps/
│   ├── static/
│   │   ├── js/
│   │   │   ├── midpoint.js   # 지도 초기화, 중간지점 계산, 경로 탐색
│   │   │   ├── address.js    # 출발지 입력 관리, 모달 검색, 현재 위치
│   │   │   └── search.js     # 사이드바 장소 검색
│   │   └── css/
│   │       └── styles.css
│   ├── templates/maps/
│   │   └── kakao_maps.html
│   └── context_processors.py # 환경변수의 API 키를 템플릿에 전달
├── myproject/
│   └── settings.py
├── .env.example
└── vercel.json
```
