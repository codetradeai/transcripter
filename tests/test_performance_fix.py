import sys
from unittest.mock import MagicMock, patch

# Mock all dependencies that might be missing or trigger I/O/UI
mock_modules = [
    'tinydb', 'groq', 'sounddevice', 'soundfile', 'pytubefix',
    'numpy', 'questionary', 'rich', 'rich.console', 'rich.table',
    'agno', 'agno.agent', 'agno.models.openai', 'dotenv'
]

for module_name in mock_modules:
    sys.modules[module_name] = MagicMock()

import transcripter.main as main

def test_analise_transcricoes_caching():
    # Setup mocks
    main.db = MagicMock()
    main.console = MagicMock()
    main.questionary = MagicMock()

    # Mock data
    mock_item = MagicMock()
    mock_item.doc_id = 1
    mock_item.__getitem__.side_effect = lambda x: "test_text" if x == "texto" else "test_val"
    mock_item.get.side_effect = lambda x, default="": "test_val"

    mock_transcricoes = [mock_item]
    main.db.all.return_value = mock_transcricoes

    # Mock questionary flow:
    # 1. Action selection (Select "4. Voltar" to exit loop)
    main.questionary.select().ask.return_value = "4. Voltar"

    with patch('builtins.input', return_value=''):
        main.analise_transcricoes()

    # Verify db.all() was called exactly once before the loop
    assert main.db.all.call_count == 1

def test_analise_transcricoes_refresh_on_delete():
    # Setup mocks
    main.db = MagicMock()
    main.console = MagicMock()
    main.questionary = MagicMock()

    # Mock data
    mock_item = MagicMock()
    mock_item.doc_id = 1
    mock_item.__getitem__.side_effect = lambda x: "test_text" if x == "texto" else "test_val"
    mock_item.get.side_effect = lambda x, default="": "test_val"

    main.db.all.return_value = [mock_item]

    # Sequence of actions:
    # 1. Select "3. Deletar transcrição"
    # 2. Enter index "1"
    # 3. Select "4. Voltar" to exit
    main.questionary.select().ask.side_effect = ["3. Deletar transcrição", "4. Voltar"]
    main.questionary.text().ask.return_value = "1"

    with patch('builtins.input', return_value=''):
        main.analise_transcricoes()

    # db.all() should be called twice: once initially, and once after deletion
    assert main.db.all.call_count == 2
    main.db.remove.assert_called_once()

if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__]))
