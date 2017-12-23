# GPAPI

잔디당의 서비스 API 서버입니다.

## 설치와 실행

먼저 `SECRET_KEY` 환경 변수의 등록이 필요합니다.

```sh
export SECRET_KEY=<your-secret-key>
```

> 임의의 키는 [이곳](https://www.miniwebtool.com/django-secret-key-generator/)에서 생성할 수 있습니다.

다음 명령어로 모든 컨테이너들을 실행합니다.

```sh
docker-compose up -d --build
```
