# fastapi-tutorial

- Python 3.10.8 사용
- FastAPI 서버에서 웹소켓 + 멀티프로세싱
- 웹소켓을 통해 서버에 작업 명령 할당, 클라이언트에 작업 상태 전달
- Timeout 기능 추가

## 실행 방법
- 서버 실행
    ```
    > python -m venv venv
    > source venv/bin/activate
    (venv) > pip install -r requirements.txt
    (venv) > uvicorn main:app
    ```
- `client/task_manager.html` 통해 접속

## 실행 예시
![image](https://user-images.githubusercontent.com/54832818/199403123-57dcf626-5d3a-4025-ba58-ab5952e79cb5.png)
- (Size, Size) X (Size, Size) 행렬곱 연산을 timeout 시간 내에 수행하고 결과를 클라이언트에 전달
- Task마다 실행 시각 기반의 task id 부여
- Running, Success, Fail 3가지 상태를 진행 상태에 따라 웹소켓으로 업데이트
