"""Tests for memory command detection."""

from src.core.memory.commands import detect_memory_command, MemoryCommand


def test_detect_forget_spanish():
    assert detect_memory_command("OLVIDA MIS DATOS") == MemoryCommand.FORGET


def test_detect_forget_lowercase():
    assert detect_memory_command("olvida mis datos") == MemoryCommand.FORGET


def test_detect_forget_french():
    assert detect_memory_command("oublie mes donnees") == MemoryCommand.FORGET


def test_detect_optin_yes_spanish():
    assert detect_memory_command("si") == MemoryCommand.OPT_IN_YES


def test_detect_optin_yes_spanish_accent():
    assert detect_memory_command("sí") == MemoryCommand.OPT_IN_YES


def test_detect_optin_no_spanish():
    assert detect_memory_command("no") == MemoryCommand.OPT_IN_NO


def test_detect_none_normal_text():
    assert detect_memory_command("como pido el paro") is None


def test_detect_none_long_text():
    assert detect_memory_command("si, me gustaria saber sobre el imv") is None
