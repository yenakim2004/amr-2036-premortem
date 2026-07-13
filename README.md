# 2036 프리모템: AI 신약설계의 화학공간 붕괴

> "모델이 좁아진 것이 아니라, 모델에 이의를 제기하는 사람이 먼저 좁아졌다.
> 그리고 그 좁아짐은 우리가 AI를 가장 신뢰하던 순간에 시작됐다."

2026 KAIST AI x 실패 아이디어 공모전 제출작의 보완 자료 저장소.
1페이지 제안서(`draft_proposal_pharma.md`)에서 인용한 모든 수치를 원자료 CSV로부터
직접 재현할 수 있도록 분석 코드와 데이터를 공개한다.

## 요약

AI 신약설계 파이프라인이 화학자의 반박 없는 검토("검토는 하되 반박하지 않는다")와
실패 데이터 미공유가 10년간 누적되며 재귀적 재학습을 거쳐 화학공간이 점점
좁아지고, 그 결과 2036년 다제내성균(AMR) 대응에 필요한 신규 계열 항생제
후보가 고갈된다는 프리모템(premortem) 시나리오.

## 폴더 구조

```
github_supplement/
├── README.md                          — 이 문서
├── analysis.py                        — 전체 계산 재현 스크립트
├── data/
│   ├── who_pipeline.csv                — WHO 임상 파이프라인 규모 (2023, 2025)
│   ├── new_entrants_class_composition.csv — 신규 진입 후보의 계열 구성
│   ├── gram_amr_mortality.csv          — AMR 직접 기인 사망자 수 (2021 실측, 2050 전망)
│   ├── gram_amr_cumulative_forecast.csv — 2025-2050 누적 사망 전망
│   ├── scaffold_coverage_benchmark.csv — 생성모델 스캐폴드 커버리지 벤치마크
│   └── sensitivity_analysis.csv        — 연간 감소율 민감도 분석 결과
└── figures/
    ├── sensitivity_analysis.png        — 민감도 분석 그래프
    └── mode_collapse_comparison.png    — 타 도메인 model/mode collapse 비교표
```

## 재현 방법

```bash
pip install pandas numpy
python analysis.py
```

`analysis.py`는 `data/who_pipeline.csv`의 실측치(2023년 97개 → 2025년 90개)로부터
연간 감소율을 계산하고, 이를 2036년까지 고정 외삽해 제안서에 인용된 수치
(파이프라인 약 60개, 혁신 후보 약 10개)를 그대로 재현한다.

## 수치 산정 방법 및 한계

- **연간 감소율**: 2023→2025 실측치(97개→90개)로부터 `(90/97)^(1/2) - 1 ≈ -3.68%/yr`로
  계산 (2년 기준 clean CAGR).
- **2036년 외삽**: 위 감소율과 2025년 혁신 후보 비율(15/90 = 16.7%)을 그대로
  고정해 11년 외삽. **model/mode collapse로 인한 추가적인 다양성 손실은
  반영하지 않은 보수적 추정치**다 — 즉 실제 시나리오는 이 추정보다 더
  나쁠 수 있다.
- **민감도 분석**(`data/sensitivity_analysis.csv`, `figures/sensitivity_analysis.png`):
  가정한 연간 감소율을 실측치 기준 ±2%p 범위에서 흔춰봐도, 2036년 혁신 후보
  수는 가장 낙관적인 가정(-1.68%/yr)에서도 2025년 실측치(15개)에 못 미친다 —
  결론이 특정 감소율 가정 하나에 취약하게 의존하지 않음을 보여준다.
- **일반 소분자 생성 벤치마크**(스캐폴드 커버리지 2,900/15,851 ≈ 18.3%)는
  항생제에 특화된 연구가 아니라 일반 de novo 분자 생성 벤치마크이며,
  화학공간 편중의 정성적 유비(analogy)로만 사용했다.

## 출처

- WHO. *Analysis of antibacterial agents in clinical and preclinical development: overview and analysis 2025.*
- WHO / The Lancet Microbe (2024). *Antibacterial agents in preclinical and clinical development.*
- Naghavi, M. et al. (2024). *Global burden of bacterial antimicrobial resistance 1990–2021: a systematic analysis with forecasts to 2050.* The Lancet (GRAM Project).
- Sheffield 대학 연구진 인터뷰, Drug Discovery World (2025) — 의약화학자 창의성 침식 체감.
- Nature 기사 — King's College London, Miraz Rahman 사례 (출판 편향/음성 결과 미공유).
- Model/mode collapse 문헌 (예: Shumailov et al., Nature 2023/2024) — 생성 AI 재귀적 자기학습에 의한 다양성 손실.

## 타 도메인 비교 (`figures/mode_collapse_comparison.png`)

이미지 생성(diffusion/GAN의 model collapse), 추천 시스템(필터 버블),
LLM 합성데이터 학습에서 이미 관찰된 것과 동일한 "생성물로 다음 세대를
재학습 → 다양성 수렴" 메커니즘이 신약설계 파이프라인에도 적용됨을
보여주는 비교표. 세부 출처는 위 문헌 목록 참고.

## 관련 자료

- 1페이지 제안서: `draft_proposal_pharma.md`
- 보완 슬라이드 덱(8장): `supplementary_deck.pdf`
