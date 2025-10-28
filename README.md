# PyAPI-RTS

**RSCAD 드래프트 파일을 읽고 조작하는 Python 라이브러리**

API 미리보기는 <a href="examples/simple_example/simple_example.ipynb">examples/simple_example/simple_example.ipynb</a>를 참조하시거나 <a href="docs/pyapi_rts.pdf">문서</a>를 확인하세요.

## 설치

이 프로젝트를 설치하려면 다음 단계를 수행하세요:

1. 프로젝트 클론
2. 클론한 디렉토리로 `cd` 이동
3. `pip install poetry` 실행
4. `poetry install` 실행

## RSCAD 컴포넌트로부터 클래스 생성

프로젝트를 처음 사용하기 전에, RSCAD 마스터 라이브러리의 컴포넌트에 대한 클래스를 생성해야 합니다.

1. `COMPONENTS` 디렉토리의 파일들을 `pyapi_rts/pyapi_rts/class_extractor/COMPONENTS`로 복사합니다.

2. `poetry run python ./pyapi_rts/class_extractor/main.py` 실행

클래스 생성을 위한 추가 옵션:

- \-d: 새 클래스 생성 전에 출력 폴더 삭제
- \-o: OBSOLETE 폴더를 생성에 포함 (구버전에서 변환된 .dfx 파일 사용 시 권장)
- \-p: COMPONENTS 폴더 경로 설정
- \-t: 파일 파싱에 사용할 스레드 수 설정. 기본값: 8

! 생성 중 적용되는 최적화로 인해 진행률 표시줄이 정확하지 않습니다.

## 테스트 실행

`poetry run pytest`

## Workshop 프로젝트

`workshop/` 디렉토리에는 PyAPI-RTS로 구축된 예제 구현 및 프로젝트가 포함되어 있습니다:

### IEEE 13 Node Test Feeder

IEEE 13 버스 배전 테스트 시스템의 완전한 구현입니다. 이 프로젝트는 PyAPI-RTS를 사용하여 표준 벤치마크 배전 시스템을 구축하는 방법을 보여줍니다.

**위치**: `workshop/ieee_13_bus/`

**기능**:
- 완전한 시스템 구성 데이터 (13개 노드, 12개 선로 구간)
- RSCAD 모델 생성을 위한 자동화된 빌더 클래스
- 부하 분석 및 검증 유틸리티
- 네트워크 토폴로지 시각화
- 포괄적인 문서

**빠른 시작**:
```python
from workshop.ieee_13_bus import IEEE13BusBuilder

builder = IEEE13BusBuilder()
print(builder.get_summary())

# .dfx 파일 생성 (RSCAD 컴포넌트 클래스 필요)
# draft = builder.build()
# draft.write_file("ieee_13_bus.dfx")
```

**문서**: 자세한 정보는 `workshop/ieee_13_bus/README.md`를 참조하세요.

**시스템 사양**:
- 정격 전압: 4.16 kV
- 총 부하: 3,466 kW + 2,102 kVAr
- 구성요소: 전압 조정기 1개, 변압기 2개, 집중 부하 8개, 커패시터 뱅크 2개
- 가공 및 지중 혼합 선로
- 여러 부하 모델(PQ, I, Z)을 사용한 불평형 부하

더 많은 workshop 프로젝트와 예제는 `workshop/README.md`를 참조하세요.

## 인용

> M. Weber, J. Enzinger, H. K. Çakmak, U. Kühnapfel and V. Hagenmeyer, "PyAPI-RTS: A Python-API for RSCAD Modeling," 2023 Open Source Modelling and Simulation of Energy Systems (OSMSES), Aachen, Germany, 2023, pp. 1-7, doi: [10.1109/OSMSES58477.2023.10089671](https://doi.org/10.1109/OSMSES58477.2023.10089671).
