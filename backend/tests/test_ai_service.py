from services.ai_service import ai_service


def test_ai_service_evaluate_bounds():
    result = ai_service.evaluate(
        amount_eth=1.2,
        tx_count_last_hour=4,
        mean_interval_seconds=540.0,
        wallet_activity_ratio=0.4,
    )
    assert 0 <= result.risk_score <= 100
    assert isinstance(result.anomaly_flag, bool)
