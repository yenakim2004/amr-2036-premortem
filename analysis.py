"""
analysis.py — 2036 프리모템: AI 신약설계 화학공간 붕괴 시나리오
재현 가능한 분석 스크립트

이 스크립트는 제안서(draft_proposal_pharma.md) 및 보완자료 슬라이드에 사용된
모든 수치를 data/ 폴더의 원자료 CSV로부터 그대로 재계산한다.
임의로 지어낸 수치는 없으며, 모든 값은 아래 출처에서 실측되었거나
(외삽/민감도 분석의 경우) 실측치로부터 명시된 방법으로 계산되었다.

실행: python analysis.py
"""
import pandas as pd
import numpy as np
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_who_pipeline():
    return pd.read_csv(os.path.join(DATA_DIR, "who_pipeline.csv"))


def project_pipeline_to_2036(who_df: pd.DataFrame, target_year: int = 2036) -> dict:
    """WHO 2023->2025 실측 파이프라인 규모로부터 연간 감소율을 구하고,
    2025년 혁신 후보 비율(16.7%)을 고정한 채 target_year까지 외삽한다.

    이 외삽은 model/mode collapse로 인한 추가적인 다양성 손실을 반영하지
    않은 보수적 추정치임을 명시한다 (draft_proposal_pharma.md 참고).
    """
    n_2023 = who_df.loc[who_df.year == 2023, "total_clinical_candidates"].iloc[0]
    n_2025 = who_df.loc[who_df.year == 2025, "total_clinical_candidates"].iloc[0]
    innov_frac_2025 = who_df.loc[who_df.year == 2025, "innovative_fraction"].iloc[0]

    annual_rate = (n_2025 / n_2023) ** (1 / 2) - 1  # clean 2-year basis
    total_proj = n_2025 * (1 + annual_rate) ** (target_year - 2025)
    innov_proj = total_proj * innov_frac_2025

    return {
        "annual_rate": annual_rate,
        "total_pipeline_proj": total_proj,
        "innovative_candidates_proj": innov_proj,
        "innovative_fraction_held": innov_frac_2025,
    }


def sensitivity_analysis(who_df: pd.DataFrame, target_year: int = 2036,
                          delta_pp_range=(-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2)) -> pd.DataFrame:
    """연간 감소율 가정을 measured rate 주변 +/- delta_pp(percentage points)만큼
    흔들었을 때 target_year 파이프라인/혁신후보 수가 어떻게 바뀌는지 계산.
    """
    n_2025 = who_df.loc[who_df.year == 2025, "total_clinical_candidates"].iloc[0]
    innov_frac_2025 = who_df.loc[who_df.year == 2025, "innovative_fraction"].iloc[0]
    base = project_pipeline_to_2036(who_df, target_year)
    rate_center = base["annual_rate"]

    rows = []
    for d_pp in delta_pp_range:
        r = rate_center + d_pp / 100
        tp = n_2025 * (1 + r) ** (target_year - 2025)
        ip = tp * innov_frac_2025
        rows.append({
            "delta_pp": d_pp,
            "annual_rate_pct": r * 100,
            "total_pipeline_2036": tp,
            "innovative_candidates_2036": ip,
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    who = load_who_pipeline()
    proj = project_pipeline_to_2036(who)
    print(f"연간 감소율 (2023->2025 실측 기준): {proj['annual_rate']:.4%}")
    print(f"2036년 전체 파이프라인 추정: {proj['total_pipeline_proj']:.1f}개")
    print(f"2036년 혁신 후보 추정: {proj['innovative_candidates_proj']:.1f}개 "
          f"(2025년 혁신 비율 {proj['innovative_fraction_held']:.1%} 고정)")

    print()
    sens = sensitivity_analysis(who)
    print("민감도 분석 (연간 감소율 ±2%p):")
    print(sens.round(2).to_string(index=False))
