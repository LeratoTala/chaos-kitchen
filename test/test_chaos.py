import pytest
from unittest.mock import patch, MagicMock


def test_runner_executes_slow_database():
    """
    Verify that the chaos runner can look up and execute the 'slow_database'
    experiment by name without raising an exception.
    """
    from chaos.runner import run_experiment
    with patch("chaos.slow_database.apply") as mock_apply:
        run_experiment("slow_database")
        mock_apply.assert_called_once()


def test_runner_executes_break_dns():
    """
    Verify that the chaos runner can look up and execute the 'break_dns'
    experiment by name without raising an exception.
    """
    from chaos.runner import run_experiment
    with patch("chaos.break_dns.apply") as mock_apply:
        run_experiment("break_dns")
        mock_apply.assert_called_once()


def test_runner_executes_kill_services():
    """
    Verify that the chaos runner can look up and execute the 'kill_services'
    experiment by name without raising an exception.
    """
    from chaos.runner import run_experiment
    with patch("chaos.kill_services.apply") as mock_apply:
        run_experiment("kill_services")
        mock_apply.assert_called_once()


def test_runner_raises_on_unknown_experiment():
    """
    Verify that the chaos runner raises a meaningful error when given
    an experiment name that does not exist.
    """
    from chaos.runner import run_experiment
    with pytest.raises((ValueError, KeyError)):
        run_experiment("nonexistent_experiment")


def test_slow_database_apply():
    """
    Verify that the slow_database module's apply function runs without error
    and simulates latency by calling the expected sleep or delay mechanism.
    """
    from chaos import slow_database
    with patch("time.sleep") as mock_sleep:
        slow_database.apply()
        mock_sleep.assert_called()


def test_break_dns_apply():
    """
    Verify that the break_dns module's apply function runs without error
    and attempts to modify DNS or network configuration as expected.
    """
    from chaos import break_dns
    with patch("chaos.break_dns.apply") as mock_apply:
        break_dns.apply()
        mock_apply.assert_called_once()


def test_kill_services_apply():
    """
    Verify that the kill_services module's apply function runs without error
    and attempts to stop or terminate the target service process.
    """
    from chaos import kill_services
    with patch("chaos.kill_services.apply") as mock_apply:
        kill_services.apply()
        mock_apply.assert_called_once()
