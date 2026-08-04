# 초보자용 Streamlit 멀티페이지 앱

설치와 실행은 [setup.md](setup.md)를 참고하세요.

왼쪽 메뉴를 누르면 가운데 영역에 선택한 화면이 표시되는 간단한 예제입니다.
로그인, 로그아웃, 데이터베이스 연결 기능은 없습니다.

## 폴더 구조

```text
mini__frontend_02/
├─ app.py
├─ requirements.txt
└─ app_pages/
   ├─ 01_home.py
   ├─ 02_signup.py
   ├─ 03_log_view.py
   ├─ 04_chat.py
   └─ 05_database_view.py
```

## 실행 방법

PowerShell에서 현재 폴더로 이동한 뒤 아래 명령어를 차례로 실행합니다.

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

실행 후 브라우저가 열리면 왼쪽 메뉴에서 원하는 화면을 선택합니다.
