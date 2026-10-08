uv run python -c "
from sentinel_platform.config.settings import get_settings, resolve_settings_file
import os
s = get_settings()
print('settings file resolved:', s.settings_file)
print('missing required:', s.missing_required())
print('process env DOC_STORE_DIR:', repr(os.environ.get('DOC_STORE_DIR')))
print('env names present:', [n for n in ('MODEL_SERVICE_ENDPOINT','MODEL_CHAT_DEPLOYMENT','MODEL_API_VERSION','MODEL_EMBEDDINGS_DEPLOYMENT','DOCINTEL_ENDPOINT') if (os.environ.get(n) or '').strip()])
"
