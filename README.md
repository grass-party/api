# GPAPI

[![CircleCI](https://circleci.com/gh/grass-party/api.svg?style=svg)](https://circleci.com/gh/grass-party/api) [![codecov](https://codecov.io/gh/grass-party/api/branch/master/graph/badge.svg)](https://codecov.io/gh/grass-party/api)

잔디당의 서비스 API 서버입니다.

## 설치와 실행

다음 명령어로 이미지를 빌드하고 컨테이너를 실행합니다.

```sh
docker-compose up -d --build
```

이제 `localhost:8000`으로 접속할 수 있습니다..

## 배포

컨테이너 안에서 AWS에 접속하기 위해 다음과 같은 환경 변수를 설정해 줍니다. ID와 비밀 키는 관리자에게 전달 받습니다.

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

필요하다면 컨테이너를 재시작합니다.

다음 명령어로 AWS Lambda에 배포합니다.

```sh
docker exec -i gpapi-django /bin/sh -c '. /venv/bin/activate; zappa deploy <zappa-env>'
```

사용 가능한 `<zappa-env>`은 다음과 같습니다.

- `dev`
- `prod`

## 데이터베이스 마이그레이션

### 로컬 환경

```sh
docker exec -i gpapi-django /bin/sh -c '. /venv/bin/activate; python /app/manage.py makemigrations'
docker exec -i gpapi-django /bin/sh -c '. /venv/bin/activate; python /app/manage.py migrate'
```

### 배포 환경

```sh
docker exec -i gpapi-django /bin/sh -c '. /venv/bin/activate; zappa manage <zappa-env> migrate'
```
