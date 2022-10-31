# fastapi-tutorial

- Python 3.10.8 사용
- FastAPI 서버에서 웹소켓 + 멀티프로세싱
- 웹소켓을 통해 서버에 작업 명령 할당, 클라이언트에 작업 상태 전달
- ProcessPoolExecutor를 통한 멀티프로세싱 처리

## 실행
- 서버 실행: `uvicorn main:app`
- `client/task_manager.html` 통해 접속
