"""Tests for the main module."""

import pytest
from unittest.mock import patch, MagicMock

from src.main import main


def test_main_runs_without_error():
    """Test that main function runs without raising exceptions."""
    with patch("src.main.logger") as mock_logger:
        main()
        assert mock_logger.info.called


def test_main_logs_start_and_finish():
    """Test that main function logs appropriate messages."""
    with patch("src.main.logger") as mock_logger:
        main()
        mock_logger.info.assert_any_call("Starting application...")
        mock_logger.info.assert_any_call("Application finished.")
