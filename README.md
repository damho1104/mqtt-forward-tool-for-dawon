# MQTT forward tool
- 내부 MQTT broker 의 특정 장치를 외부 MQTT broker 로 포워딩하기 위한 도구
- 실행 전 config.json 을 실행파일과 동일한 경로에 만들어야 함
## Release note
### v1.0.3
- topic 처리 버그 수정
### v1.0.2
- subscribe/publish re-connect 기능 추가
### v1.0.1
- 루트 인증서 추가 기능 추가
### v1.0.0
- 내부 MQTT broker 의 특정 장치를 외부 MQTT broker 로 포워딩 기능 추가
- config.json 을 통한 설정 기능 추가
## Description of 'config.json'
```json
{
  "info": {
    "mqtt_device_name": "[SUBSCRIBE 장치명]",
    "device_name": "PM-B540-W[실제 장치명]",
    "device_id": "[실제 DEVICE ID]",
    "topic": "[TOPIC]",
    "subscribe": {
      "use_cert": false,
      "ip": "[내부 IP]",
      "port": [내부 PORT, int값],
      "password": "[장치 비밀번호]"
    },
    "publish": {
      "use_cert": true,
      "ip": "[외부 도메인, 외부 IP]",
      "port": 8883[외부 PORT, int값, SSL 포트로 하는 것을 권장],
      "password": "[장치 비밀번호]"
    }
  },
  "certs": {
    "root_cert_path": "[ROOT_인증서.crt 경로]",
    "client_cert_path": "[클라이언트_인증서.crt 경로]",
    "client_cert_key_path": "[클라이언트_인증서.key 경로]"
  }
}
```

## Example of 'config.json'
### - Windows
```json
{
  "info": {
    "mqtt_device_name": "[SUBSCRIBE 장치명]",
    "device_name": "PM-B540-W",
    "device_id": "wg21442dsfg20b",
    "topic": "dwd.v1",
    "subscribe": {
      "use_cert": false,
      "ip": "192.168.1.3",
      "port": 1803,
      "password": "password"
    },
    "publish": {
      "use_cert": true,
      "ip": "pm.example.com",
      "port": 8883,
      "password": "password"
    }
  },
  "certs": {
    "root_cert_path": "C:\\PowerManager\\certificate\\ca.crt",
    "client_cert_path": "C:\\PowerManager\\certificate\\C.crt",
    "client_cert_key_path": "C:\\PowerManager\\certificate\\private\\C.key"
  }
}
```
### - Linux
```json
{
  "info": {
    "mqtt_device_name": "[SUBSCRIBE 장치명]",
    "device_name": "PM-B540-W",
    "device_id": "wg21442dsfg20b",
    "topic": "dwd.v1",
    "subscribe": {
      "use_cert": false,
      "ip": "192.168.1.3",
      "port": 1803,
      "password": "password"
    },
    "publish": {
      "use_cert": true,
      "ip": "pm.example.com",
      "port": 8883,
      "password": "password"
    }
  },
  "certs": {
    "root_cert_path": "/usr/PowerManager/certificate/ca.crt",
    "client_cert_path": "/usr/PowerManager/certificate/C.crt",
    "client_cert_key_path": "/usr/PowerManager/certificate/private/C.key"
  }
}
```