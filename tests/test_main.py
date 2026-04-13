import sys
from unittest.mock import MagicMock, patch
from datetime import datetime

# Mock dependencies before importing transcripter.main
mock_tinydb = MagicMock()
mock_groq = MagicMock()
mock_sounddevice = MagicMock()
mock_soundfile = MagicMock()
mock_pytubefix = MagicMock()
mock_questionary = MagicMock()
mock_rich = MagicMock()
mock_agno = MagicMock()
mock_dotenv = MagicMock()
mock_numpy = MagicMock()

sys.modules['tinydb'] = mock_tinydb
sys.modules['groq'] = mock_groq
sys.modules['sounddevice'] = mock_sounddevice
sys.modules['soundfile'] = mock_soundfile
sys.modules['pytubefix'] = mock_pytubefix
sys.modules['questionary'] = mock_questionary
sys.modules['rich'] = mock_rich
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.table'] = MagicMock()
sys.modules['agno'] = mock_agno
sys.modules['agno.agent'] = MagicMock()
sys.modules['agno.models.openai'] = MagicMock()
sys.modules['dotenv'] = mock_dotenv # main.py uses 'from dotenv import load_dotenv'
sys.modules['numpy'] = mock_numpy

# Now import the module under test
import transcripter.main as main

def test_salvar_transcricao():
    origem = "teste_origem"
    titulo = "teste_titulo"
    texto = "teste_texto"

    # Fixed datetime for testing
    fixed_now = datetime(2023, 10, 27, 12, 0, 0)

    with patch('transcripter.main.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_now

        main.salvar_transcricao(origem, titulo, texto)

        main.db.insert.assert_called_once_with({
            "origem": origem,
            "titulo": titulo,
            "texto": texto,
            "data": "2023-10-27 12:00:00"
        })
